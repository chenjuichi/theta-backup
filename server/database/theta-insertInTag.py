from tables import Grid, InTag, association_grid_intag_table, Session

import pymysql
from sqlalchemy import exc
from sqlalchemy import func

# --------------------------

s = Session()

#新增 intag資料
new_intag = InTag(work_id='20240320111', user_id=4, spindle_id=1, date='113/04/02', period='113/05/11')  #1
s.add(new_intag)
new_intag = InTag(work_id='20240315111', user_id=4, spindle_id=2, date='113/04/02', period='113/05/12')  #2
s.add(new_intag)
new_intag = InTag(work_id='20240310111', user_id=4, spindle_id=3, date='113/04/02', period='113/05/15')  #3
s.add(new_intag)
new_intag = InTag(work_id='20240410111', user_id=4, spindle_id=1, date='113/04/10', period='113/05/20')  #4
s.add(new_intag)
new_intag = InTag(work_id='20240410121', user_id=4, spindle_id=16, date='113/04/11', period='113/05/21')  #5
s.add(new_intag)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

print("insert intag data is ok...")

# --------------------------


intag_records = s.query(InTag).all()
grid_records = s.query(Grid).all()

grid_records[0]._intags_g_i.extend([intag_records[0], intag_records[1]])  #spindle1~2入庫到grid1
grid_records[7]._intags_g_i.extend([intag_records[2]])                    #spindle3入庫到grid8
grid_records[0]._intags_g_i.extend([intag_records[3]])                    #spindle1入庫到grid1
grid_records[15]._intags_g_i.extend([intag_records[4]])                  #spindle16入庫到grid116

grid_records[0].total_size=3
grid_records[7].total_size=1
grid_records[15].total_size=1

s.add_all([grid_records[0], grid_records[1]])

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

print("grid and spind combine ok...")

#grid_records = s.query(Grid).all()

'''
grid_records = s.query(Grid).all()
for grid in grid_records:
  if not grid._spindles:
    print("grid id", grid.id, 'nothing...')
    continue
  spindle_ids = ', '.join(str(spindle.id) for spindle in grid._spindles)
  print("grid id", grid.id, 'total spindle: ', len(grid._spindles), 'spind id', spindle_ids)
'''
for grid in grid_records:
    intag_count = s.query(func.count(association_grid_intag_table.c.intag_id)).filter_by(grid_id=grid.id).scalar()
    if intag_count != 0:
      print(f"Grid id {grid.id} has {intag_count} associated intags.")

for grid in grid_records:

    associated_intags = grid._intags_g_i
    if associated_intags:
      print(f"Grid id {grid.id} is associated with the following InTag IDs:")
      for intag in associated_intags:
        print(f"- InTag id {intag.id}")


s.close()