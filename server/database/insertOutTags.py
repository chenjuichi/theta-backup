from tables import User, Setting, OutTag, InTag, Reagent, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash

# --------------------------

#           1,  2,  3,  4,  5,  6,  7,  8,  9
inTag_id = [20, 21, 22, 23, 24, 25, 26, 27, 28,
            25, 26,  # for 已列印(2筆)
            26, 27,   # for 已出庫(2筆)
            29,
            ]
#         1, 2, 3, 4, 5, 6, 7, 8, 9
userID = [2, 3, 4, 5, 5, 6, 2, 3, 4,
          6, 7,  # for 已列印(2筆)
          6, 7,  # for 已出庫(2筆)
          7,
          ]
#          1, 2,  3, 4,  5,  6,  7,  8, 9
reagent = [1, 6,  6, 6,  6,  7,  7,  9, 9,
           7, 7,  # for 已列印(2筆)
           7, 9,  # for 已出庫(2筆)
           6,
           ]
#        1, 2, 3, 4, 5, 6, 7, 8, 9
count = [1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1,  # for 已列印(2筆)
         1, 1,  # for 已出庫(2筆)
         1,
         ]
'''
#         1,   2,    3,    4,    5,    6,    7,   8,    9
unit = ['組', '組', '組', '組', '組', '組', '組', '組', '組',
        '組', '組',   # for 已列印(2筆)
        '組', '組',   # for 已入庫(2筆)
        '組',
        ]
'''
outtag_date = ['111/11/30', '111/11/30', '111/12/15', '111/11/30', '111/11/30', '111/12/15', '111/11/20', '111/12/15', '111/12/15',
                '111/12/30', '111/12/30',  # for 已列印(2筆)
                '111/12/25', '112/1/10',  # for 已入庫(2筆)
                '111/12/28',
              ]

alpha = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
         'a', 'b',  # for 已列印(2筆)
         'a','a',  # for 已入庫(1筆)
         'a',
         ]

printMark = [False, False, False, False, False, False, False, False, False,
             True, True,  # for 已列印(2筆)
             False, False,  # for 已入庫(1筆)
             True,
             ]

stockoutMark = [False, False, False, False, False, False, False, False, False,
                False, False,  # for 已列印(2筆)
                True, True,  # for 已入庫(1筆)
                False,
              ]

s = Session()
_results = []

temp_outtag_size = len(outtag_date)
print("insert stockout data total: ", temp_outtag_size)
for i in range(temp_outtag_size):
    in_tag = s.query(InTag).filter_by(id=inTag_id[i]).first()
    reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

    _obj = OutTag(intag_id=inTag_id[i], user_id=userID[i], count=count[i] * reagent.reag_scale, stockOut_alpha=alpha[i],
                  #unit=reagent.reag_Out_unit,
                  outtag_date=outtag_date[i], isPrinted=printMark[i], isStockout=stockoutMark[i])
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
