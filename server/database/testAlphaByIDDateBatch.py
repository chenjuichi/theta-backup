
from flask import Blueprint, jsonify, request

from tables import Reagent, InTag, Session


s = Session()
#records = s.query(InTag).filter(InTag.id > 1321).all()
records = s.query(InTag).all()
_blocks = [u.__dict__ for u in records]
id_len=len(_blocks)
print("total records: ", id_len)
'''
#解析, 讀取並排序id資料
#stockinIDs = [ sub['id'] for sub in _blocks ]
#id_len=len(stockinIDs)
#stockinIDs.sort()
#print("data id: ", stockinIDs)

reagentIDs = []
batchs=[]
intagDates=[]

#排序入庫的reagent_id資料(=reagentIDs)
reagentIDs = [ sub['reagent_id'] for sub in _blocks ]
reagentIDs = list(dict.fromkeys(reagentIDs))
#reagentIDs.sort()

#入庫的批次資料(=batchs)

#排序入庫的入庫日期資料(=batchs)
allDatas = s.query(InTag).filter(InTag.reagent_id.in_(reagentIDs))

_datas = [u.__dict__ for u in allDatas]

batchs = [ sub['batch'] for sub in _datas ]
batchs = list(dict.fromkeys(batchs))
#batchs.sort()
intagDates = [ sub['intag_date'] for sub in _datas ]
intagDates = list(dict.fromkeys(intagDates))
intagDates.sort()

i=0
for reagentID in reagentIDs:
  maxAlphaObjectsOrder = s.query(InTag).filter(InTag.reagent_id == reagentID, InTag.isRemoved == True, InTag.isStockin == True).order_by(InTag.stockIn_alpha.asc()).all()
  myCreateAt=max(node.create_at for node in maxAlphaObjectsOrder)
  kks = [u.__dict__ for u in maxAlphaObjectsOrder]
  _index = next((index for (index, d) in enumerate(kks) if d["create_at"] == myCreateAt), None)
  myAlpha=kks[_index]['stockIn_alpha']
  print(reagentID, ":", "myAlpha: ", myCreateAt, myAlpha, kks[_index]['create_at'])

  #for i, j in enumerate(maxAlphaObjectsOrder):
  #  print("index",i)
  #  print(j)

'''
s.close()



