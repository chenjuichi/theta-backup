from tables import User, Setting, InTag, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash

# --------------------------
user = [2, 2, 3, 3, 4,
        5, 6, 7, 7, 7,
        5, 6, 7, 7, 7,  # for 已列印(5筆)
        1, 6, 6, 6,
        1, 6, 6, 6, 2, 2, 2, 2, 4, 6, # for 已入庫(9筆)
        ]
#          1,  2,  3,  4,  5, 6, 7, 8, 9, 10
reagent = [14, 12, 12, 9, 11, 5, 6, 8, 8, 1,
            5,  6,  8, 8,  1, 1, 6, 6, 6, 1,# for 已列印(5筆)
            6,  6,  6, 1,  6, 6, 6, 6, 7, 7,
            9,  9, 39,# for 已入庫(9筆)
           ]

#        1, 2, 3,  4, 5, 6, 7, 8,  9, 10
count = [1, 1, 1,  1, 1, 1, 1, 1, 1, 1,
         1, 4, 1,  2, 1,  # for 已列印(5筆)
         1, 1, 1,  1,
         1, 1, 1,  1, 1, 1, 1, 1, 1, 1, # for 已入庫(9筆)
         ]

temp_cnt = [
            #1, 1, 1, 1, 2,
            #1, 1, 0, 0, 0,
            #1, 1, 0, 0, 0,  # for 已列印(5筆)
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,  0, 0, 0, 0, 0, 0, # for 已入庫(9筆)
            ]
batch = ['111001', '111002', '111003', '111004', '111004',
         '111005', '111005', '111005', '111005', '111005',
         # for 已列印(5筆)
         '111011', '111012', '111012', '111013', '111014',
         '111014', '111015', '111016', '111017',

         '111020', '111021', '111021', '111021',  # for 入庫
         '111021', '111022', '111023', '111023',
         '111024', '1120112',
         ]
# 2022-12-12新增
reag_period = ['112/10/31', '112/12/31', '112/12/31', '113/6/30', '113/6/30',
               '113/6/30',  '112/8/31',  '112/8/31', '112/8/31', '112/01/10',
               # for 已列印(5筆)
               '113/6/30',  '112/8/31',  '112/8/31', '112/8/31', '112/01/10',
               '112/01/10', '112/10/31', '112/10/31',  '112/01/10',
               # for 已入庫(4筆)
               '112/01/10', '112/10/31', '112/10/31',  '112/01/10',
               '112/10/31', '112/10/31',  '112/01/10', '112/8/31', '112/8/31',
               '115/1/31',
               ]

intag_date = ['111/05/01', '111/05/01', '111/05/01', '111/04/01', '111/04/01',
              '111/04/01', '111/06/01', '111/06/01', '111/08/01', '111/08/01',
              # for 已列印(5筆)
              '111/11/01', '111/11/01', '111/12/01', '111/11/01', '111/12/01',
              '111/08/01', '111/10/20', '111/10/20', '110/10/20',
              # for 已入庫(9筆)
              '111/08/01', '111/10/20', '111/10/20', '110/10/20',
              '111/08/01', '111/10/20', '111/10/20', '110/10/20', '110/10/20',
              '112/01/10',
              ]
alpha = [' ', ' ', ' ', ' ', ' ',
         ' ', ' ', ' ', ' ', ' ',
         'D', 'C', 'B', 'A', 'B',  # for 已列印(5筆)
         ' ', ' ', ' ', ' ',
         'A', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'A',# for 已入庫(9筆)
         ]

printMark = [False, False, False, False, False, False, False, False, False, False,
             True,  True,  True,  True,  True,  # for 已列印(5筆)
             False, False, False, False,
             False, False, False, False, False, False, False, False, False, False,# for 已入庫(4筆)
            ]
stockinMark = [False, False, False, False, False,
               False, False, False, False, False,
               False, False, False, False, False,  # for 已列印(5筆)
               False, False, False, False,
               True,  True,  True,  True,  True,  True,  True,  True,  True, True,# for 已入庫(9筆)
              ]

s = Session()
_results = []
temp_intag_size = len(intag_date)
for i in range(temp_intag_size):
    #_obj = InTag(user_id=user[i], reagent_id=reagent[i], grid_id=grid[i],  # 2013-01-13 mark
    _obj = InTag(user_id=user[i], reagent_id=reagent[i],  # 2023=01=13 modify
                 count=count[i],  stockIn_alpha=alpha[i],
                 reag_period=reag_period[i],
                 stockOut_temp_count=temp_cnt[i], batch=batch[i],
                 intag_date=intag_date[i], isPrinted=printMark[i], isStockin=stockinMark[i])
    _results.append(_obj)

s.bulk_save_objects(_results)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

s.close()

print("insert 14+5+4+5 inTag data is ok...")
