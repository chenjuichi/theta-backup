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

reagentIDs = []
batchs=[]
intagDates=[]
stockinIDs=[]
selectedReagentIDs=[39, 41, 172, 154]
intag_objects = s.query(InTag).filter(InTag.reagent_id.in_(selectedReagentIDs))

#intag_objects = s.query(InTag).all()
intags = [u.__dict__ for u in intag_objects]

for intag in intags:
  if (intag['isRemoved'] and intag['isStockin']):
    reagentIDs.append(intag['reagent_id'])
    batchs.append(intag['batch'])
    intagDates.append(intag['intag_date'])
reagentIDs = list(dict.fromkeys(reagentIDs))
reagentIDs.sort()
batchs = list(dict.fromkeys(batchs))
batchs.sort()
intagDates = list(dict.fromkeys(intagDates))
intagDates.sort()
'''
print("reagentIDs: ", reagentIDs)
print("======")
print("batchs: ", batchs)
print("======")
print("intagDates: ", intagDates)
'''

myBatch=""
myDate=""

i=1
for reagentID in reagentIDs:
  myAlpha="A"
  for batch in batchs:
    for intagDate in intagDates:
        _objects=s.query(InTag).filter_by(
          reagent_id=reagentID,
          batch=batch,
          intag_date=intagDate,
          isRemoved=True,
          isStockin=True
        ).all()
        if _objects:
          for myIntag in _objects:
            myIntag.stockIn_alpha=myAlpha
            #s.query(InTag).filter(InTag.id == myIntag.id).update({'stockIn_alpha': myAlpha})
            print(i,":", myIntag)
            i=i+1
          myAscii=ord(myAlpha)
          if myAscii==ord("Z"):
            myAlpha="A"
          else:
            myAlpha=chr(ord(myAlpha) + 1)

'''
#update
s.commit()
'''
s.close()

#print("Ready insert inTag data(stockIn_alpha) is ok...")