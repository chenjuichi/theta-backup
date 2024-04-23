import math

from tables import User, Setting, Reagent, InTag, OutTag, Session

import pymysql
from sqlalchemy import exc, func

from werkzeug.security import generate_password_hash

# --------------------------

s = Session()
_results = []

intag_objects = s.query(InTag).all()
intags = [u.__dict__ for u in intag_objects]
i = 1
for intag in intags:
  if (intag['isRemoved'] and intag['isStockin'] and not intag['isPrinted']):
  #if (intag['isRemoved'] and intag['isStockin'] and not intag['isPrinted'] and not (intag['reagent_id'] in _results)):
    #_results.append(intag['reagent_id'])
    cursor = s.query(func.sum(OutTag.count)).filter(
      OutTag.intag_id == intag['id'] and
      OutTag.isRemoved and
      not OutTag.isPrinted and
      OutTag.isStockout
    )
    out_total = cursor.scalar()

    qry = s.query(func.count(OutTag.id)).filter(
      OutTag.intag_id == intag['id'] and OutTag.isRemoved and not OutTag.isPrinted and OutTag.isStockout
    )
    out_qry = qry.scalar()

    isUpdate=False
    if (intag['count'] !=0 or out_total):
      reagent = s.query(Reagent).filter_by(id=intag['reagent_id']).first()
      if (reagent.reag_In_unit==reagent.reag_Out_unit and out_total):
        total=intag['count'] + out_total
        myInCount=total
        print(i, out_qry, " 在庫: ", reagent.reag_id, intag['id'], intag['reagent_id'], intag['count'], reagent.reag_In_unit, out_total, reagent.reag_Out_unit, " 入庫原始總數: ", myInCount)
        isUpdate=True
      if (reagent.reag_In_unit==reagent.reag_Out_unit and not out_total):
        myInCount=intag['count']
        print(i, out_qry, " 在庫: ", reagent.reag_id, intag['id'], intag['reagent_id'], intag['count'], reagent.reag_In_unit, " 入庫原始總數: ", myInCount)
        isUpdate=True
      if (reagent.reag_In_unit!=reagent.reag_Out_unit and not out_total):
        myInCount=intag['count']
        if myInCount < 1:
          print(i, out_qry, " 在庫: ", reagent.reag_id, intag['id'], intag['reagent_id'], intag['count'], reagent.reag_In_unit, '\033[46m' +" ,暫時沒有出庫數!(異常)" + '\033[0m')
        else:
          print(i, out_qry, " 在庫: ", reagent.reag_id, intag['id'], intag['reagent_id'], intag['count'], reagent.reag_In_unit, " 暫時沒有出庫數!")
        isUpdate=True
      if (reagent.reag_In_unit!=reagent.reag_Out_unit and out_total):
        myInCount=out_total / reagent.reag_scale
        myInCount= intag['count'] + myInCount
        myInCount=math.floor(myInCount*1000)  # 取小數點3位
        myInCount=round(myInCount/1000, 0)
        print(i, out_qry, " 在庫: ", reagent.reag_id, intag['id'], intag['reagent_id'], intag['count'], reagent.reag_In_unit, out_total, reagent.reag_Out_unit, " 入庫原始總數: ", myInCount, reagent.reag_In_unit, " 入出庫單位不同!")
        isUpdate=True

      #update
      '''
      if isUpdate:
        kk=intag['id']
        s.query(InTag).filter(InTag.id == kk).update({'ori_count': myInCount})
        #s.commit()
        print("intag table,第", kk, "筆的 ori_count 以更改為", myInCount)
      '''
    i=i+1

#s.commit()
s.close()

print("Ready insert inTag data(ori_count) is ok...")