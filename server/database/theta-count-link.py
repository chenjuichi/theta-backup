from tables import Spindle, Grid, association_table, Session

import pymysql
from sqlalchemy import exc

from sqlalchemy import func

s = Session()

#spindle_records = s.query(Spindle).all()
#grid_records = s.query(Grid).all()
'''
for grid in grid_records:
  if not grid._spindles:
    print("grid id", grid.id, 'nothing...')
    continue
  #print("grid id", grid.id, 'total spindle: ', len(grid._spindles))
  #for spindle in grid._spindles:
  #  print("spind id", spindle.id)
  spindle_ids = ', '.join(str(spindle.id) for spindle in grid._spindles)
  print("grid id", grid.id, 'total spindle: ', len(grid._spindles), 'spind id', spindle_ids)
'''

'''
for grid in grid_records:
    if not grid._spindles:
        print("grid id", grid.id, 'nothing...')
        continue
    spindle_ids = ', '.join(str(spindle.id) for spindle in grid._spindles)
    print("grid id", grid.id, 'total spindle: ', len(grid._spindles), 'spind id', spindle_ids)
'''

'''
# 遍历每个网格记录
for grid in grid_records:
    if grid._spindles:  # 如果网格有主轴关联
        # 获取该网格的主轴ID列表，并按照升序排序
        spindle_ids = sorted(spindle.id for spindle in grid._spindles)
        # 将主轴ID列表转换为逗号分隔的字符串形式
        spindle_ids_str = ', '.join(str(spindle_id) for spindle_id in spindle_ids)
        # 输出网格ID和关联的主轴ID列表
        print(f"grid id {grid.id} total spindle: {len(grid._spindles)} spind id {spindle_ids_str}")
    else:
        # 如果网格没有关联的主轴，则输出提示信息
        print(f"grid id {grid.id} has no associated spindles.")
'''
'''
# 遍历每个网格记录
for grid in grid_records:
    if grid._spindles:  # 如果网格有主轴关联
        # 获取该网格的主轴ID列表，并按照升序排序
        spindle_ids = sorted(spindle.id for spindle in grid._spindles)
        # 将主轴ID列表转换为逗号分隔的字符串形式
        spindle_ids_str = ', '.join(str(spindle_id) for spindle_id in spindle_ids)
        # 输出网格ID和关联的主轴ID列表
        print(f"grid id {grid.id} total spindle: {len(grid._spindles)} spind id {spindle_ids_str}")
    else:
        # 如果网格没有关联的主轴，则输出提示信息
        print(f"grid id {grid.id} has no associated spindles.")
'''

'''
grid_records = s.query(Grid).all()
for grid in grid_records:
    spindle_count = s.query(Grid._spindles).filter_by(id=grid.id).count()
    print(f"Grid id {grid.id} has {spindle_count} associated spindles.")
'''

'''
for grid in grid_records:
    spindle_count = s.query(func.count(association_table.c.spindle_id)).filter_by(grid_id=grid.id).scalar()
    print(f"Grid id {grid.id} has {spindle_count} associated spindles.")
'''

'''
#sol1:
grid_records = s.query(Grid).all()
for grid in grid_records:
    # 查询与当前 Grid 相关联的 Spindle 记录的数量
    spindle_count = s.query(func.count(association_table.c.spindle_id)).filter_by(grid_id=grid.id).scalar()

    # 查询与当前 Grid 相关联的 Spindle 记录的 ID
    #spindle_ids = s.query(association_table.c.spindle_id).filter_by(grid_id=grid.id).all()
    #spindle_ids = [spindle_id[0] for spindle_id in spindle_ids]
    spindle_ids = s.query(association_table.c.spindle_id.label('id')).filter_by(grid_id=grid.id).all()
    spindle_ids = [spindle_id.id for spindle_id in spindle_ids]


    print(f"Grid id {grid.id} has {spindle_count} associated spindles:")
    for spindle_id in spindle_ids:
        print(f"- Spindle id {spindle_id}")
'''
#sol2
grid_records = s.query(Grid).all()
for grid in grid_records:
  # 查詢與目前 Grid 關聯的 Spindle 記錄的數量
  spindle_count = s.query(func.count(association_table.c.spindle_id)).filter_by(grid_id=grid.id).scalar()

  # 查詢與目前 Grid 關聯的 Spindle 記錄
  spindles = s.query(Spindle).join(association_table).filter(association_table.c.grid_id == grid.id).all()

  print(f"Grid id {grid.id} has {spindle_count} associated spindles:")
  for spindle in spindles:
    print(spindle.id)  # 列印 Spindle 物件的完整內容

s.close()