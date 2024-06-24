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

# --------------------------

#新增SPINDLE資料
#                  1  2  3  4  5  6
_l_spindle_type = [1, 1, 1, 2, 2, 3,
#                  7  8  9  10
                   1, 1, 2, 3,
#                  11
                   2,
#                  12 13 14
                   3, 2, 2,
#
#                  15 16 17 18 19 20
                   1, 1, 1, 1, 1, 1,
#                  21 22 23 24 25
                   2, 2, 2, 2, 2,
#                  26 27 28 29 30
                   3, 3, 3, 3, 3, 3, 3,
                   1, 2,
                   1, 1, 1, 1, 1,
                  ]

_l_spindle_cat =  ['THZ-62.03', 'TH-120.08', 'THS-255.01', 'THG-80.01', 'THG-170.01', 'THGA-60.01',
                   'TH-120.11', 'TT-120.04', 'THGN-170.01', 'THSG-150',
                   'THG-150.01',
                   'THSG-110', 'THGA-220.06', 'THGA-220.05',
#
                   'TH-150', 'TH-170.03', 'TH-190.04', 'TH-210.01', 'TH-230.23', 'THS-255.01',
                   'THG-100.03', 'THG-120.15', 'THG-150.03', 'THG-170.02', 'THGS-240.02',
                   'THGA-V50.01', 'THGA-60.01', 'THGL-60.01', 'THGZ-72', 'THGZ-72.01', 'THGZ-72.02', 'TTGD-110.01',
                   'TH-120.02', 'THG-120.01',
                   'TH-120.01', 'TH-150.01', 'TH-150.02', 'THN-170.02', 'THN-170.03',
                  ]

_l_spindle_outer =['61.91', '120', '255', '80', '170', '49.5',
                   '120', '120', '170', '150',
                   '150',
                   '110', '220', '220',
#
                   '150', '170', '190', '210', '230', '255',
                   '100', '120', '150', '170', '240',
                   '49.5', '60', '60', '72', '72', '72', '110',
                   '120', '120',
                   '120', '150', '150', '170', '170',
                  ]

_l_spindle_inner =['17','40', '70', '12', '65', 'N/A',
                   '40', '40', '70', '70',
                   '50',
                   '40', '90', '90',
#
                   '50', '65', '70', '70', '100', '70',
                   '25', '40', '50', '65', '110',
                   '', '', '', '', '', '', '',
                   '40', '40',
                   '40', '50', '50', '70', '70',
                  ]

_l_spindle_rpm =['70000', '40000', '12000', '120000', '24000', '18000',
                 '30000', '12000', '20000', '5000',
                 '13500',
                 '5000',  '6000',  '6000',
#
                 '36000', '20000', '15000', '18000', '12000', '12000',
                 '60000', '36000', '36000', '24000', '5000',
                 '18000', '24000', '12000', '12000', '6000', '12000', '9000',
                 '17600', '35700',
                 '17600', '13500', '13500', '20000', '20000',
                ]

_l_spindle_motor =['', 'FANUC BiI 40M/70000', '', '', '', '',
                  'BiI 50L/30000', 'BiI 56L2/15000-B', '', '',
                  '',
                  '', '', '',
#
                  '', '', '', '', '', '',
                  '', '', '', '', '',
                  '感應馬達', '感應馬達', '感應馬達', '感應馬達', '感應馬達', '同步馬達', '同步馬達',
                  '', '',
                  '', '', '', '', '',
                  ]

_l_spindle_kw=['1.5', '3.0', '16', '1', '18', '0.1',
               '7.5', '10',  '18', '',
               '15',
               '',    '24',  '16',
#
               '15', '30', '16', '15', '18.5/22', '16',
               '6.4', '4.6', '15', '18', '23.6',
               '0.1', '0.45', '0.26', '1.2', '1.8', '1', '1.8',
               '10', '13',
               '10', '15', '15', '18', '18',
              ]

_l_spindle_nm=['0.20', '0.95', '47.8', '0.08', '29.3', '0.05',
               '4.77', '12.7', '29.3', '',
               '10.6',
               '', '76.4', '102',
#
               '10.6', '29.1', '47.8', '71.6', '177/70', '47.8',
               '1.7', '4.5', '10.6', '29.3', '66',
               '0.05', '0.21', '0.21', '0.96', '3', '1', '2.9',
               '5.4', '3.5',
               '5.4', '10.6', '10.6', '29.3', '29.3',
              ]

_l_spindle_lubrication =[2, 1, 1, 1, 1, 1,
                         1, 1, 1, 2,
                         1,
                         0, 1, 1,
#
                         1, 1, 1, 1, 1, 1,
                         1, 1, 1, 1, 1,
                         1, 1, 2, 2, 2, 2, 2,
                         1, 1,
                         1, 1, 1, 1, 1,
                        ] #0: N/A, 1:油氣潤滑, 2:油脂潤滑

_l_spindle_handle = ['WT-5(Collet 1~6mm)', 'HSK-E32', 'HSK-A63 BBT-40', 'D6/12', 'D36/63 HSK-C50', 'N/A',
                     'HSK-E40 BBT-30', 'HSK-E40 HSK-F50', 'D36/63 HSK-C63', '客製化',
                     'D28/43 HSK-C40',
                     '客製化', '客製化','客製化',
#
                     'HSK-E50 HSK-F63', 'BT-40 BBT-40', 'HSK-C63 HSK-A63 BBT-40', 'HSK-A63 BBT-40', 'HSK-A100 BBT-50', 'HSK-T63 Capto C6',
                     'D14/23', 'D22/38 HSK-C32', 'D28/43 HSK-C40', 'D36/63 HSK-C50', '客製化',
                     '', '', '', '', '', '', '',
                     'HSK-E40 HSK-F50', 'D22/38 HSK-C32',
                     'HSK-E40 HSK-F50', 'HSK-E50 HSK-F63', 'HSK-E50 HSK-F63', 'HSK-A63 BBT-40', 'HSK-A63 BBT-40',
                    ]

_l_spindle_cooling =[3, 3, 3, 3, 3, 0,
                     3, 3, 3, 0,
                     3,
                     0, 3, 3,
#
                     3, 3, 3, 3, 3, 3,
                     3, 3, 3, 3, 3,
                     0, 0, 0, 0, 0, 0, 0,
                     3, 3,
                     3, 3, 3, 3, 3,
                    ] #冷卻方式, 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷

spindles_total_size = len(_l_spindle_type)
_objects = []
tt = 0
for x in range(spindles_total_size):
  u = Spindle(
    spindle_type = _l_spindle_type[x],      #類別, 1~3
    spindle_cat = _l_spindle_cat[x],        #型號
    spindle_outer = _l_spindle_outer[x],    #外徑
    spindle_inner = _l_spindle_inner[x],    #軸承內徑, 主軸內藏馬達有可能為 空白
    spindle_rpm = _l_spindle_rpm[x],        #最高轉速
    spindle_motor = _l_spindle_motor[x],    #馬達規格
    spindle_kw = _l_spindle_kw[x],          #馬達功率S1
    spindle_nm = _l_spindle_nm[x],          #馬達扭力S1
    spindle_lubrication = _l_spindle_lubrication[x],  #潤滑方式, 1:油氣潤滑, 2:油脂潤滑
    spindle_cooling = _l_spindle_cooling[x],          #冷卻方式, 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷
    spindle_handle = _l_spindle_handle[x],            #刀把介面
  )
  _objects.append(u)

s.bulk_save_objects(_objects)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

print("insert " + str(spindles_total_size) + " spindles is ok...")

# --------------------------

spindle_records = s.query(Spindle).all()
grid_records = s.query(Grid).all()

spindle_records[0].isAll=False
spindle_records[1].isAll=False
spindle_records[2].isAll=False
spindle_records[3].isAll=False
spindle_records[4].isAll=False
#spindle_records[5].isAll=False
spindle_records[6].isAll=False
spindle_records[7].isAll=False
#spindle_records[8].isAll=False
#spindle_records[9].isAll=False
spindle_records[10].isAll=False

grid_records[0]._spindles.extend([spindle_records[0], spindle_records[1], spindle_records[2]])  #st1
grid_records[1]._spindles.extend([spindle_records[3], spindle_records[4]])  #st1
grid_records[2]._spindles.extend([spindle_records[6]])  #st1
grid_records[3]._spindles.extend([spindle_records[7]])  #st1
grid_records[4]._spindles.extend([spindle_records[0]])  #st1

grid_records[6]._spindles.extend([spindle_records[5], spindle_records[10]]) #st2
grid_records[7]._spindles.extend([spindle_records[2]])  #st2

grid_records[10]._spindles.extend([spindle_records[8], spindle_records[9]]) #st3

s.add_all([grid_records[0], grid_records[1], grid_records[2], grid_records[3],
           grid_records[4], grid_records[6], grid_records[7], grid_records[10]])

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

print("grid and spind combine ok...")
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
    spindle_count = s.query(func.count(association_table.c.spindle_id)).filter_by(grid_id=grid.id).scalar()
    print(f"Grid id {grid.id} has {spindle_count} associated spindles.")

s.close()