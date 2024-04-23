from datetime import datetime

from sqlalchemy import Table, Column, Float, Integer, String, DateTime, Boolean, func, text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

# 宣告一個映射, 建立一個基礎類別
BASE = declarative_base()

# ------------------------------------------------------------------

class Worker(BASE):
  __tablename__ = 'worker'

  id = Column(Integer, primary_key=True, autoincrement=True)
  emp_id = Column(String(4), nullable=False)              #員工編號 4碼
  emp_name = Column(String(10), nullable=False)           #員工姓名

  create_at = Column(DateTime, server_default=func.now())

  def __repr__(self):  # 定義變數輸出的內容
    return "id={}, emp_id={}, emp_name={}, ".format(
      self.id,
      self.emp_id,
      self.emp_name,
    )

  # 定義class的dict內容
  def get_dict(self):
    return {
      'id': self.id,
      'emp_id': self.emp_id,
      'emp_name': self.emp_name,
    }

# ------------------------------------------------------------------

# 建立連線
engine = create_engine("mssql+pyodbc://sa:77974590@192.168.32.154:1433/wujii?driver=ODBC+Driver+17+for+SQL+Server")

# 將己連結的資料庫engine綁定到這個session
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
  inspector = inspect(engine)
  if not inspector.has_table('worker', schema='wujii'):
      BASE.metadata.create_all(engine)     # 在資料庫中建立表格, 及映射表格內容
      print("Table 'worker' created.")
  else:
      print("Table 'worker' already exists.")