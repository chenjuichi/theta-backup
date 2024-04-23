import os

os.environ['SQLALCHEMY_WARN_20'] = '0'    # 設置環境變數來顯示所有與SQLAlchemy 2.0相關的警告
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '0'   # 設置環境變數來靜音指定的警告

from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, func, ForeignKey, create_engine
from sqlalchemy import text
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()   # 宣告一個映射, 建立一個基礎類別


# ------------------------------------------------------------------


class User(BASE):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, autoincrement=True)
  emp_id = Column(String(4), nullable=False)              #員工編號 4碼
  emp_name = Column(String(10), nullable=False)           #員工姓名
  password = Column(String(255))                          #default a1234
  perm_id = Column(Integer, ForeignKey('permission.id'))  # 一對多(多)
  setting_id = Column(Integer, ForeignKey('setting.id'))  # 一對多(多)
  isRemoved = Column(Boolean, default=True)               # false:已經刪除資料
  isOnline = Column(Boolean, default=False)               # false:user不在線上(logout)
  _instocks = relationship('InTag', backref="user")                 # 一對多(一)
  _outstocks = relationship('OutTag', backref="user")               # 一對多(一)
  _spindle_runin = relationship('SpindleRunIn', backref="user")     # 一對多(一)
  create_at = Column(DateTime, server_default=func.now())

  def __repr__(self):  # 定義變數輸出的內容
    '''
    return "id={}, emp_id={}, emp_name={}, password={}, perm_id={}, setting_id={}, isRemoved={}".format(
          self.id, self.emp_id, self.emp_name, self.password, self.perm_id, self.setting_id, self.isRemoved)
    '''
    #fields = ['{0}={1}'.format(k, getattr(self, k)) for k in self._sa_class_manager.keys()]
    #return "{}({})".format(self.__class__.__tablename__, ", ".join( fields  ))
    # 使用反射獲取所有欄位及其值
    fields = ', '.join([f"{name}={getattr(self, name)}" for name in self.__mapper__.columns.keys()])
    return f"<LargeTable({fields})>"

  # 定義class的dict內容
  def get_dict(self):
    '''
    return {
      'id': self.id,
      'emp_id': self.emp_id,
      'emp_name': self.emp_name,
      'password': self.password,
      #'dep_id': self.dep_id,
      'perm_id': self.perm_id,
      'setting_id': self.setting_id,
      'isRemoved': self.isRemoved,
    }
    '''
    # 使用反射獲取所有欄位及其值並轉換為字典
    return {name: getattr(self, name) for name in self.__mapper__.columns.keys()}


# ------------------------------------------------------------------


class Permission(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 1:none, 2:system, 3:admin, 4:member
    auth_code = Column(Integer, default=0)
    # 10:none, 2:system, 32:admin, 4:member
    auth_name = Column(String(10), default='none')
    # 一對多(一)
    # 設定cascade後,可刪除級關連
    # 不設定cascade, 則perm_id為空的, 但沒刪除級關連
    _user = relationship('User', backref='permission')  #一對多(一)
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, auth_code={}".format(self.id, self.auth_code)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'auth_code': self.auth_code,
        }


# ------------------------------------------------------------------


class Setting(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    items_per_page = Column(Integer, default=10)
    isSee = Column(String(1), default=text("0"))      # 0:user沒有看公告資料
    message = Column(String(30))
    _user = relationship('User', backref='setting')   # 一對多(一 )
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, items_per_page={}, isSee={}, message={}".format(self.id, self.items_per_page, self.isSee, self.message)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'items_per_page': self.items_per_page,
            'isSee': self.isSee,
            'message': self.message,
        }


# ------------------------------------------------------------------


association_table = Table('association', BASE.metadata,
    Column('grid_id', Integer, ForeignKey('grid.id')),
    Column('spindle_id', Integer, ForeignKey('spindle.id'))
)

association_grid_intag_table = Table('association_grid_intag_table', BASE.metadata,
  Column('grid_id', Integer, ForeignKey('grid.id')),
  Column('intag_id', Integer, ForeignKey('intag.id'))
)


# ------------------------------------------------------------------


class Grid(BASE):
    __tablename__ = 'grid'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station = Column(Integer, nullable=False)     #1~4
    layout = Column(Integer, nullable=False)
    total_size = Column(Integer, default=0)      #目前該儲位存放總數
    max_size = Column(Integer, default=5)        #目前存放總數
    _spindles = relationship("Spindle", secondary=association_table, back_populates="_grids")
    _intags_g_i = relationship("InTag", secondary=association_grid_intag_table, back_populates="_grids_g_i")
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
      return "id={}, station={}, layout={}, total_size={}, max_size={}, \
        isRemoved={}, create_at={}".format(
        self.id, self.station, self.layout, self.total_size, self.max_size,
        self.isRemoved, self.create_at
      )

    # 定義class的dict內容
    def get_dict(self):
      return {
        'id': self.id,
        'station': self.station,
        'layout': self.layout,
        'total_size': self.total_size,
        'max_size': self.max_size,
        'isRemoved': self.isRemoved,
        'create_at': self.create_at,
      }


# ------------------------------------------------------------------


class Spindle(BASE):
  __tablename__ = 'spindle'

  id = Column(Integer, primary_key=True, autoincrement=True)
  _spindle_runin = relationship('SpindleRunIn', backref="spindle")  #跑合資料tab, 一對多(一)
  spindle_type = Column(Integer, nullable=False)      #類別, 1~3
  spindle_cat = Column(String(30), nullable=False)    #型號

  spindle_outer = Column(String(10))    #外徑
  spindle_inner = Column(String(10))    #軸承內徑, 主軸內藏馬達有可能為 空白
  spindle_rpm = Column(String(10))      #最高轉速

  spindle_motor = Column(String(30), default='')    #馬達規格
  spindle_kw = Column(String(10))       #馬達功率S1
  spindle_nm = Column(String(10))       #馬達扭力S1

  spindle_lubrication = Column(Integer, default=1)  #潤滑方式, 0: N/A, 1:油氣潤滑, 2:油脂潤滑
  spindle_cooling = Column(Integer, default=1)      #冷卻方式, 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷
  spindle_handle = Column(String(30))               #刀把介面

  ##grid_id = Column(Integer, ForeignKey('grid.id'))  #儲位資料, 一對多(多)
  _grids = relationship("Grid", secondary=association_table, back_populates="_spindles")
  isRemoved = Column(Boolean, default=True)   # false:已經刪除資料
  isAll = Column(Boolean, default=True)   # true:spindle可以放再任意格位
  _instocks = relationship('InTag', backref="spindle")  # 一對多中的 "一"
  create_at = Column(DateTime, server_default=func.now())

  def __repr__(self):  # 定義變數輸出的內容
    return "id={}, spindle_type={}, spindle_cat={}, spindle_outer={}, spindle_inner={}, \
      spindle_rpm={}, spindle_motor={}, spindle_kw={}, spindle_nm={}, spindle_lubrication={}, \
      spindle_cooling={}, spindle_handle={}, isRemoved={}, create_at={}".format(
      self.id, self.spindle_type, self.spindle_cat, self.spindle_outer, self.spindle_inner,
      self.spindle_rpm, self.spindle_motor, self.spindle_kw, self.spindle_nm, self.spindle_lubrication,
      self.spindle_cooling, self.spindle_handle, self.isRemoved, self.create_at
    )

  def get_dict(self):       # 定義class的dict內容
    return {
      'id':self.id,
      'spindle_type':self.spindle_type,
      'spindle_cat':self.spindle_cat,
      'spindle_outer':self.spindle_outer,
      'spindle_inner':self.spindle_inner,
      'spindle_rpm':self.spindle_rpm,
      'spindle_motor':self.spindle_motor,
      'spindle_kw':self.spindle_kw,
      'spindle_nm':self.spindle_nm,
      'spindle_lubrication':self.spindle_lubrication,
      'spindle_cooling':self.spindle_cooling,
      'spindle_handle':self.spindle_handle,

      'isRemoved':self.isRemoved,
      'create_at':self.create_at,
    }


# ------------------------------------------------------------------


class SpindleRunIn(BASE):
  __tablename__ = 'spindlerunin'

  id = Column(Integer, primary_key=True, autoincrement=True)
  spindleRunIn_excel_file = Column(String(60))            #excel file name
  spindleRunIn_customer = Column(String(30))              #客戶
  spindleRunIn_work_id = Column(String(16))               #編  號
  spindleRunIn_spindle_id = Column(Integer, ForeignKey('spindle.id'))     #主軸
  spindleRunIn_employer = Column(Integer, ForeignKey('user.id'))          #員工
  spindleRunIn_date = Column(String(10))            #測試日期
  isRemoved = Column(Boolean, default=True)
  #層級刪除功能，當一個SpindleRunIn記錄被刪除時，與之相關的RunInData記錄也會自動刪除。
  _runin_data = relationship('RunInData', backref="spindlerunin", cascade="all, delete-orphan")
  create_at = Column(DateTime, server_default=func.now())

  def __repr__(self):  # 定義變數輸出的內容
    return "\
      id={}, \
      spindleRunIn_excel_file ={}, \
      spindleRunIn_customer ={}, \
      spindleRunIn_work_id ={}, \
      spindleRunIn_spindle_id ={}, \
      spindleRunIn_employer ={}, \
      spindleRunIn_date ={}, \
      isRemoved={}, \
      create_at ={}".format(
        self.id,
        self.spindleRunIn_excel_file,
        self.spindleRunIn_customer,
        self.spindleRunIn_work_id,
        self.spindleRunIn_spindle_id,
        self.spindleRunIn_employer,
        self.spindleRunIn_date,
        self.isRemoved,
        self.create_at,
      )

  def get_dict(self):     # 定義class的dict內容
    return {
      'id':self.id,
      'spindleRunIn_excel_file': self.spindleRunIn_excel_file,
      'spindleRunIn_customer': self.spindleRunIn_customer,
      'spindleRunIn_work_id': self.spindleRunIn_work_id,
      'spindleRunIn_spindle_id': self.spindleRunIn_spindle_id,
      'spindleRunIn_employer':  self.spindleRunIn_employer,
      'spindleRunIn_date':  self.spindleRunIn_date,
      'isRemoved': self.isRemoved,
      'create_at':self.create_at,
    }


# ------------------------------------------------------------------


class RunInData(BASE):
  __tablename__ = 'runindata'

  id = Column(Integer, primary_key=True, autoincrement=True)
  spindleRunIn_id = Column(Integer, ForeignKey('spindlerunin.id'))
  spindleRunIn_period = Column(String(10))      #時間
  spindleRunIn_speed_level = Column(String(3))  #段速
  spindleRunIn_speed = Column(String(6))        #轉速
  spindleRunIn_stator_temp = Column(String(6))  #定子溫度
  spindleRunIn_inner_frontBearing_temp = Column(String(6))  #內部前軸承溫度
  spindleRunIn_inner_backBearing_temp = Column(String(6))   #內部後軸承溫度
  spindleRunIn_outer_frontBearing_temp = Column(String(6))  #外部前軸承溫度
  spindleRunIn_outer_backBearing_temp = Column(String(6))   #外部後軸承溫度
  spindleRunIn_room_temp = Column(String(6))        #室溫
  spindleRunIn_coolWater_temp = Column(String(6))   #冷卻機水溫
  spindleRunIn_Rphase_current = Column(String(6))   #R相電流
  spindleRunIn_Sphase_current = Column(String(6))   #S相電流
  spindleRunIn_Tphase_current = Column(String(6))   #T相電流
  spindleRunIn_cool_pipeline_flow = Column(String(6))             #冷卻機管路流量
  spindleRunIn_cool_pipeline_pressure = Column(String(6))         #冷卻機管路壓力
  spindleRunIn_frontBearing_vibration_speed1 = Column(String(6))  #前軸承震動速度-1
  spindleRunIn_frontBearing_vibration_acc1 = Column(String(6))    #前軸承震動加速度-1
  spindleRunIn_frontBearing_vibration_disp1 = Column(String(6))   #前軸承震動位移-1
  spindleRunIn_frontBearing_vibration_speed2 = Column(String(6))  #前軸承震動速度-2
  spindleRunIn_frontBearing_vibration_acc2 = Column(String(6))    #前軸承震動加速度-2
  spindleRunIn_frontBearing_vibration_disp2 = Column(String(6))   #前軸承震動位移-2
  spindleRunIn_backBearing_vibration_speed1 = Column(String(6))   #後軸承震動速度-1
  spindleRunIn_backBearing_vibration_acc1 = Column(String(6))     #後軸承震動加速度-1
  spindleRunIn_backBearing_vibration_disp1 = Column(String(6))    #後軸承震動位移-1
  spindleRunIn_backBearing_vibration_speed2 = Column(String(6))   #後軸承震動速度-2
  spindleRunIn_backBearing_vibration_acc2 = Column(String(6))     #後軸承震動加速度-2
  spindleRunIn_backBearing_vibration_disp2 = Column(String(6))    #後軸承震動位移-2

  def __repr__(self):  # 定義變數輸出的內容
    return "\
      id={}, \
      spindleRunIn_id ={}, \
      spindleRunIn_period ={}, \
      spindleRunIn_speed_level ={}, \
      spindleRunIn_speed ={}, \{}, \
      spindleRunIn_stator_temp ={}, \
      spindleRunIn_inner_frontBearing_temp ={}, \
      spindleRunIn_inner_backBearing_temp ={}, \
      spindleRunIn_outer_frontBearing_temp ={}, \
      spindleRunIn_outer_backBearing_temp ={}, \
      spindleRunIn_room_temp = {}, \
      spindleRunIn_coolWater_temp = {}, \
      spindleRunIn_Rphase_current = {}, \
      spindleRunIn_Sphase_current = {}, \
      spindleRunIn_Tphase_current = {}, \
      spindleRunIn_cool_pipeline_flow = {}, \
      spindleRunIn_cool_pipeline_pressure = {}, \
      spindleRunIn_frontBearing_vibration_speed1 = {}, \
      spindleRunIn_frontBearing_vibration_acc1 = {}, \
      spindleRunIn_frontBearing_vibration_disp1 = {}, \
      spindleRunIn_frontBearing_vibration_speed2 = {}, \
      spindleRunIn_frontBearing_vibration_acc2 = {}, \
      spindleRunIn_frontBearing_vibration_disp2 = {}, \
      spindleRunIn_backBearing_vibration_speed1 = {}, \
      spindleRunIn_backBearing_vibration_acc1 = {}, \
      spindleRunIn_backBearing_vibration_disp1 = {}, \
      spindleRunIn_backBearing_vibration_speed2 = {}, \
      spindleRunIn_backBearing_vibration_acc2 = {}, \
      spindleRunIn_backBearing_vibration_disp2 = {}".format(
        self.id,
        self.spindleRunIn_id,
        self.spindleRunIn_period,
        self.spindleRunIn_speed_level,
        self.spindleRunIn_speed,
        self.spindleRunIn_stator_temp,
        self.spindleRunIn_inner_frontBearing_temp,
        self.spindleRunIn_inner_backBearing_temp,
        self.spindleRunIn_outer_frontBearing_temp,
        self.spindleRunIn_outer_backBearing_temp,
        self.spindleRunIn_room_temp,
        self.spindleRunIn_coolWater_temp,
        self.spindleRunIn_Rphase_current,
        self.spindleRunIn_Sphase_current,
        self.spindleRunIn_Tphase_current,
        self.spindleRunIn_cool_pipeline_flow,
        self.spindleRunIn_cool_pipeline_pressure,
        self.spindleRunIn_frontBearing_vibration_speed1 ,
        self.spindleRunIn_frontBearing_vibration_acc1,
        self.spindleRunIn_frontBearing_vibration_disp1,
        self.spindleRunIn_frontBearing_vibration_speed2,
        self.spindleRunIn_frontBearing_vibration_acc2,
        self.spindleRunIn_frontBearing_vibration_disp2,
        self.spindleRunIn_backBearing_vibration_speed1,
        self.spindleRunIn_backBearing_vibration_acc1,
        self.spindleRunIn_backBearing_vibration_disp1,
        self.spindleRunIn_backBearing_vibration_speed2,
        self.spindleRunIn_backBearing_vibration_acc2,
        self.spindleRunIn_backBearing_vibration_disp2,
      )

  def get_dict(self):     # 定義class的dict內容
    return {
      'id': self.id,
      'spindleRunIn_id': self.spindleRunIn_id,
      'spindleRunIn_period': self.spindleRunIn_period,
      'spindleRunIn_speed_level': self.spindleRunIn_speed_level,
      'spindleRunIn_speed': self.spindleRunIn_speed,
      'spindleRunIn_stator_temp': self.spindleRunIn_stator_temp,
      'spindleRunIn_inner_frontBearing_temp': self.spindleRunIn_inner_frontBearing_temp,
      'spindleRunIn_inner_backBearing_temp':  self.spindleRunIn_inner_backBearing_temp,
      'spindleRunIn_outer_frontBearing_temp': self.spindleRunIn_outer_frontBearing_temp,
      'spindleRunIn_outer_backBearing_temp':  self.spindleRunIn_outer_backBearing_temp,
      'spindleRunIn_room_temp': self.spindleRunIn_room_temp,
      'spindleRunIn_coolWater_temp': self.spindleRunIn_coolWater_temp,
      'spindleRunIn_Rphase_current': self.spindleRunIn_Rphase_current,
      'spindleRunIn_Sphase_current': self.spindleRunIn_Sphase_current,
      'spindleRunIn_Tphase_current': self.spindleRunIn_Tphase_current,
      'spindleRunIn_cool_pipeline_flow': self.spindleRunIn_cool_pipeline_flow,
      'spindleRunIn_cool_pipeline_pressure': self.spindleRunIn_cool_pipeline_pressure,
      'spindleRunIn_frontBearing_vibration_speed1': self.spindleRunIn_frontBearing_vibration_speed1 ,
      'spindleRunIn_frontBearing_vibration_acc1':   self.spindleRunIn_frontBearing_vibration_acc1,
      'spindleRunIn_frontBearing_vibration_disp1':  self.spindleRunIn_frontBearing_vibration_disp1,
      'spindleRunIn_frontBearing_vibration_speed2': self.spindleRunIn_frontBearing_vibration_speed2,
      'spindleRunIn_frontBearing_vibration_acc2':   self.spindleRunIn_frontBearing_vibration_acc2,
      'spindleRunIn_frontBearing_vibration_disp2':  self.spindleRunIn_frontBearing_vibration_disp2,
      'spindleRunIn_backBearing_vibration_speed1':  self.spindleRunIn_backBearing_vibration_speed1,
      'spindleRunIn_backBearing_vibration_acc1':    self.spindleRunIn_backBearing_vibration_acc1,
      'spindleRunIn_backBearing_vibration_disp1':   self.spindleRunIn_backBearing_vibration_disp1,
      'spindleRunIn_backBearing_vibration_speed2':  self.spindleRunIn_backBearing_vibration_speed2,
      'spindleRunIn_backBearing_vibration_acc2':    self.spindleRunIn_backBearing_vibration_acc2,
      'spindleRunIn_backBearing_vibration_disp2':   self.spindleRunIn_backBearing_vibration_disp2,
    }


# ------------------------------------------------------------------


class InTag(BASE):
    __tablename__ = 'intag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(String(16), nullable=False)             #製令單號
    user_id = Column(Integer, ForeignKey('user.id'))        #入庫人員資料, 一對多中的 "多"
    spindle_id = Column(Integer, ForeignKey('spindle.id'))  #入庫主軸資料, 一對多中的 "多"
    _grids_g_i = relationship("Grid", secondary=association_grid_intag_table, back_populates="_intags_g_i")
    count = Column(Integer, default=1)                      # 該儲位的入庫數量
    period = Column(String(10), nullable=False)                 #效期
    date = Column(String(10), nullable=False)                   #入庫日期
    _outstocks = relationship('OutTag', backref="intag")        #一對多中的 "一"
    isRemoved = Column(Boolean, default=True)                   # true: 在庫, false:已經刪除資料
    isRunin = Column(Boolean, default=False)                    # false: 尚未跑合
    comment = Column(String(80), default='')                    # 在庫備註說明
    date_comment = Column(String(12))                        # 在庫備註說明的日期
    user_comment = Column(String(12))                     # 在庫備註說明的員工
    updated_at = Column(DateTime, onupdate=datetime.utcnow())   # 資料修改的時間
    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
      return "id={}, user_id={}, spindle_id={}, count={}, period={}, \
        date={}, isRemoved={}, isRunin={}, comment={}, date_inv_modify={}, \
        user_id_inv_modify={}, updated_at={}".format(
        self.id,
        self.user_id,
        self.spindle_id,
        self.count,
        self.period,
        self.date,
        self.isRemoved,
        self.isRunin,
        self.comment,
        self.date_inv_modify,
        self.user_id_inv_modify,
        self.updated_at
      )

    def get_dict(self):
      return {
        'id': self.id,
        'user_id': self.user_id,
        'spindle_id': self.spindle_id,
        'count': self.count,
        'period': self.period,
        'date': self.date,
        'isRemoved': self.isRemoved,
        'isRunin': self.isRunin,
        'comment': self.comment,
        'date_inv_modify': self.date_inv_modify,
        'user_id_inv_modify': self.user_id_inv_modify,
        'updated_at': self.updated_at,
      }


# ------------------------------------------------------------------


class OutTag(BASE):
    __tablename__ = 'outtag'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    intag_id = Column(Integer, ForeignKey('intag.id'))  #在庫資料, 一對多中的 "多"
    user_id = Column(Integer, ForeignKey('user.id'))    #人員資料, 一對多中的 "多"

    count = Column(Integer, default=1)            # 出庫數量,
    date = Column(String(10), nullable=False)     # 出庫日期

    isRemoved = Column(Boolean, default=True)     # true: 在庫, false:已領料, 且刪單

    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
      return "id={}, intag_id={}, user_id={}, count={}, date={}, isRemoved={}, updated_at={}".format(
        self.id,
        self.intag_id,
        self.user_id,
        self.count,
        self.date,
        self.isRemoved,
        self.updated_at
      )

    def get_dict(self):
      return {
        'id': self.id,
        'intag_id': self.intag_id,
        'user_id': self.user_id,
        'count': self.count,
        'date': self.date,
        'isRemoved': self.isRemoved,
        'updated_at': self.updated_at
      }


# ------------------------------------------------------------------


# 建立連線
###
# 中文字需要 4-bytes 來作為 UTF-8 encoding.
# MySQL databases and tables are created using a UTF-8 with 3-bytes encoding.
# To store 中文字, you need to use the utf8mb4 character set
###
# 2023-08-25 modify
#engine = create_engine(
#    "mysql+pymysql://root:77974590@localhost:3306/cmuhch?charset=utf8mb4", echo=False)
#engine = create_engine(
#    "mysql+pymysql://root:77974590@localhost:3306/theta?charset=utf8mb4", echo=False)
engine = create_engine("mysql+pymysql://root:77974590@localhost:3306/theta", echo=False)
engine.execute("ALTER DATABASE theta CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
engine.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")

# 將己連結的資料庫engine綁定到這個session
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
  BASE.metadata.create_all(engine)  # 在資料庫中建立表格, 及映射表格內容
  print("table creating is ok...")
