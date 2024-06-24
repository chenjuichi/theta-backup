from tables import Spindle, Grid, association_table, Session

import pymysql
from sqlalchemy import exc
from sqlalchemy import func

# --------------------------

s = Session()

#新增 grid資料
new_grid = Grid(station=1, layout=1)  #1 (3)
s.add(new_grid)
new_grid = Grid(station=1, layout=2)  #2 (0)
s.add(new_grid)
new_grid = Grid(station=1, layout=3)  #3 (0)
s.add(new_grid)
new_grid = Grid(station=1, layout=4)  #4 (0)
s.add(new_grid)
new_grid = Grid(station=1, layout=5)  #5 (0)
s.add(new_grid)
new_grid = Grid(station=1, layout=6)  #6
s.add(new_grid)


new_grid = Grid(station=2, layout=1)  #7 (0)
s.add(new_grid)
new_grid = Grid(station=2, layout=2)  #8 (1)
s.add(new_grid)
new_grid = Grid(station=2, layout=3)  #9
s.add(new_grid)
new_grid = Grid(station=2, layout=4)  #10
s.add(new_grid)
new_grid = Grid(station=2, layout=5)  #11
s.add(new_grid)
new_grid = Grid(station=2, layout=6)  #12
s.add(new_grid)

new_grid = Grid(station=3, layout=1)  #13
s.add(new_grid)
new_grid = Grid(station=3, layout=2)  #14
s.add(new_grid)
new_grid = Grid(station=3, layout=3)  #15
s.add(new_grid)
new_grid = Grid(station=3, layout=4)  #16
s.add(new_grid)
new_grid = Grid(station=3, layout=5)  #17
s.add(new_grid)
new_grid = Grid(station=3, layout=6)  #18
s.add(new_grid)

new_grid = Grid(station=4, layout=1)  #19
s.add(new_grid)
new_grid = Grid(station=4, layout=2)  #20
s.add(new_grid)
new_grid = Grid(station=4, layout=3)  #21
s.add(new_grid)
new_grid = Grid(station=4, layout=4)  #22
s.add(new_grid)
new_grid = Grid(station=4, layout=5)  #23
s.add(new_grid)
new_grid = Grid(station=4, layout=6)  #24
s.add(new_grid)


try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

print("insert grid data is ok...")

s.close()