import time
import datetime

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
  comment=intag['comment'].strip()
  #count=intag['count_inv_modify']
  #isCount=(False, True)[]
  if (intag['isRemoved'] and intag['isStockin'] and not intag['isPrinted'] and comment):
    #update
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts)
    tty=now.strftime('%Y')
    tty=str(int(tty)-1911)
    ttm=now.strftime('%m')
    ttd=now.strftime('%d')
    #intag.date_inv_modify=tty+"/"+ttm+"/"+ttd
    #intag.updated_at = now  # 資料修改的時間
    kk=intag['id']
    s.query(InTag).filter(InTag.id == kk).update({
      'user_id_inv_modify': 3,
      'date_inv_modify': tty+"/"+ttm+"/"+ttd,
      'updated_at': now
    })
    print("intag id: ", kk)
    i=i+1

s.commit()
s.close()

print("Ready insert inTag data(user_id_inventory) is ok...")