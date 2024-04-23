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
  mdfCnt=intag['count_inv_modify']
  #count=intag['count_inv_modify']
  #isCount=(False, True)[]
  if (mdfCnt==0 and not comment):
    #update
    kk=intag['id']
    s.query(InTag).filter(InTag.id == kk).update({'count_inv_modify': None})
    #print("intag id: ", kk)
    i=i+1

s.commit()
s.close()

print("Ready insert inTag data(user_id_inventory) is ok...")