
from flask import Blueprint, jsonify, request

from tables import Reagent, InTag, Session


s = Session()
#records = s.query(InTag).filter(InTag.id > 1321).all()
records = s.query(InTag).all()
_blocks = [u.__dict__ for u in records]
#id_len=len(_blocks)
#print("修正筆數: ", id_len)

reagentIDs = []
batchs=[]
intagDates=[]

#排序入庫的reagent_id資料(=reagentIDs)
reagentIDs = [ sub['reagent_id'] for sub in _blocks ]
reagentIDs = list(dict.fromkeys(reagentIDs))
reagentIDs.sort()
id_len=len(reagentIDs)
print("修正筆數: ", id_len)

#入庫的批次資料(=batchs)

#排序入庫的入庫日期資料(=batchs)
#allDatas = s.query(InTag).all()
'''
allDatas = s.query(InTag).filter(InTag.reagent_id.in_(reagentIDs))

_datas = [u.__dict__ for u in allDatas]

batchs = [ sub['batch'] for sub in _datas ]
batchs = list(dict.fromkeys(batchs))
#batchs.sort()
intagDates = [ sub['intag_date'] for sub in _datas ]
intagDates = list(dict.fromkeys(intagDates))
intagDates.sort()
'''
i=0
k=0
for reagentID in reagentIDs:
  i=i+1
  myAlpha="Z"
  reagent = s.query(Reagent).filter_by(id=reagentID).first()

  allDatas = s.query(InTag).filter(InTag.reagent_id==reagentID)
  _datas = [u.__dict__ for u in allDatas]

  batchs = [ sub['batch'] for sub in _datas ]
  batchs = list(dict.fromkeys(batchs))

  intagDates = [ sub['intag_date'] for sub in _datas ]
  intagDates = list(dict.fromkeys(intagDates))
  intagDates.sort()

  #以入庫日期及批次進行alpha更換
  for intagDate in intagDates:
    for batch in batchs:
      _objects=s.query(InTag).filter_by(
        reagent_id=reagentID,
        batch=batch,
        intag_date=intagDate,
      ).all()

      if _objects:
        myAscii=ord(myAlpha)
        if myAscii==ord("Z"):
          myAlpha="A"
        else:
          myAlpha=chr(ord(myAlpha) + 1)
        ###
        j=0
        for myIntag in _objects:
          s.query(InTag).filter(InTag.id == myIntag.id).update({'stockIn_alpha': myAlpha})
          j=j+1
          k=k+1
        #pad a string to a fixed length with spaces,
        t_alpha = batch.ljust(11) + myAlpha + " 共" + str(j) + "筆"
        print(k, "\t進度 "+str(i)+"/"+str(id_len)+": \t"+str(reagentID) + ": 試劑編號 " + str(reagent.reag_id) + "\t入庫日期 " + intagDate + ", 批次 " + t_alpha)
        #print(myIntag)

s.commit()

s.close()

print("update alpha is ok...")


