import time
import datetime
import pytz

from flask import Blueprint, jsonify, request
import pymysql
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import distinct

from database.tables import User, Spindle, Grid, Permission, OutTag, InTag, Setting, Session

from werkzeug.security import generate_password_hash

from operator import itemgetter, attrgetter   # 2023-08-27  add

updateTable = Blueprint('updateTable', __name__)

# ------------------------------------------------------------------

@updateTable.route("/updatePassword", methods=['POST'])
def update_password():
    print("updatePassword....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    newPassword = (request_data['newPassword'] or '')

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "" or newPassword == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    s.query(User).filter(User.emp_id == userID).update(
        {'password': generate_password_hash(
            newPassword, method='sha256')})
    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# update user's setting from user table some data
@updateTable.route("/updateSetting", methods=['POST'])
def update_setting():
    print("updateSetting....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    newSetting = (request_data['setting'] or '')

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "" or newSetting == "":
        return_value = False  # false: 資料不完全 註冊失敗
    # print("update setting value: ", newSetting, type(newSetting))
    s = Session()
    # 修改user的設定資料
    _user = s.query(User).filter_by(emp_id=userID).first()
    s.query(Setting).filter(Setting.id == _user.setting_id).update(
        {'items_per_page': newSetting})

    s.query(User).filter(User.emp_id == userID).update(
        {'isOnline': False})  # false:user已經登出(logout)

    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# from user table update some data by id
@updateTable.route("/updateUser", methods=['POST'])
def update_user():
    print("updateUser....")
    request_data = request.get_json()

    _emp_id = request_data['emp_id']
    _emp_name = request_data['emp_name']

    return_value = True  # true: 資料正確, 註冊成功
    if _emp_id == "" or _emp_name == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string

    s = Session()

    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    if return_value:
        s.query(User).filter(User.emp_id == _emp_id).update(
            {"emp_name": _emp_name, "dep_id": department.id})
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from spindle table update some data
@updateTable.route("/updateSpindle", methods=['POST'])
def update_spindle():
  print("updateSpindle....")

  request_data = request.get_json()
  print("request_data: ", request_data)

  _id = request_data['id']
  _spindle_type = int(request_data['spindle_type'])
  _spindle_cat = request_data['spindle_cat']
  _spindle_cooling = int(request_data['spindle_cooling'])
  _spindle_handle = request_data['spindle_handle']
  _spindle_outer = request_data['spindle_outer']
  _spindle_inner = request_data['spindle_inner']
  _spindle_rpm = request_data['spindle_rpm']
  _spindle_kw = request_data['spindle_kw']
  _spindle_nm = request_data['spindle_nm']
  _spindle_lubrication = request_data['spindle_lubrication']
  temp_str=request_data['spindle_motor']
  _spindle_motor = (temp_str, '')[temp_str == '空白']

  return_value = True
  return_message=''
  s = Session()

  #更新主軸資料
  s.query(Spindle).filter(Spindle.id == _id, Spindle.spindle_type==_spindle_type, Spindle.spindle_cat==_spindle_cat).update(
  {
    "spindle_outer" : _spindle_outer,     #外徑
    "spindle_inner" : _spindle_inner,     #軸承內徑, 主軸內藏馬達有可能為 空白
    "spindle_rpm" : _spindle_rpm,         #最高轉速
    "spindle_motor" : _spindle_motor,     #馬達規格
    "spindle_kw" : _spindle_kw,           #馬達功率S1
    "spindle_nm" : _spindle_nm,           #馬達扭力S1
    "spindle_lubrication" : _spindle_lubrication,   #潤滑方式, 1:油氣潤滑, 2:油脂潤滑
    "spindle_cooling" : _spindle_cooling,           #冷卻方式, 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷
    "spindle_handle" :_spindle_handle,              #刀把介面
  })

  try:
    s.commit()
    print("Spindle data updated successfully.")
  except Exception as e:
    s.rollback()
    print("Error:", str(e))
    return_message ='錯誤! 主軸資料更新沒有成功...'
    return_value = False

  s.close()

  return jsonify({
      'status': return_value,
      'message': return_message,
  })


# from grid table update some data
@updateTable.route("/updateGrid", methods=['POST'])
def update_grid():
  print("updateGrid....")

  request_data = request.get_json()
  print("request_data: ", request_data)

  _temp_id = request_data['id']
  #_s_id = request_data['s_id']
  _new_grid_type = int(request_data['grid_type'])
  _new_grid_cat = request_data['grid_cat']
  _grid_type_and_cat=request_data['grid_type_and_cat']
  _grid_max_size=request_data['grid_max_size']
  # 使用split方法将字符串分割成两部分
  tk1="_"
  _id, _temp_id2 = _temp_id.split(tk1)
  _id=int(_id)

  if (_grid_type_and_cat != ''):
    tk2 = " / "
    _tempT, _grid_cat = _grid_type_and_cat.split(tk2)
    _tempT = _tempT.strip()         # 去除空格
    _existing_grid_cat = _grid_cat.strip()
  else:
    _tempT = ''
    _existing_grid_cat = ''

  #_existing_grid_type = 1 if _tempT == '銑削/研磨主軸(自動換刀)' else (2 if _tempT == '研磨主軸(手動換刀)' else 3)
  _existing_grid_type = 0 if _tempT == '' else (1 if _tempT == '銑削/研磨主軸(自動換刀)' else (2 if _tempT == '研磨主軸(手動換刀)' else 3))

  print("_id, _existing_grid_type,  _existing_grid_cat, _new_grid_type,  _new_grid_cat: ", _id, _existing_grid_type,  _existing_grid_cat, _new_grid_type,  _new_grid_cat)

  return_value = True
  return_message=''
  s = Session()

  #找出儲位/主軸資料
  existing_grid = s.query(Grid).filter(Grid.id == _id).first()
  existing_spindle = s.query(Spindle).filter_by(spindle_type=_existing_grid_type, spindle_cat=_existing_grid_cat, grid_id=_id).first()
  new_spindle = s.query(Spindle).filter_by(spindle_type=_new_grid_type, spindle_cat=_new_grid_cat).first()
  #有spindle資料
  if new_spindle:
    print("updateGrid, step 1-1")

    ## 查詢與 existing_spindle 相同 id 的所有 Spindle
    #other_spindles = s.query(Spindle).filter(Spindle.id == existing_spindle.id).all()
    #_related_to_other_grids = any(other_spindle.grid_id != _id for other_spindle in other_spindles)

    other_grids_with_existing_spindle = s.query(Grid).join(Spindle).filter(Spindle.id == existing_spindle.id, Grid.id != _id).all()
    #existing_grid.max_size=_grid_max_size
    record_count = other_grids_with_existing_spindle.count()
    print("updateGrid, count: ", record_count)

    #existing_spindle没有與其他Grid相關聯
    if not other_grids_with_existing_spindle:
      print("updateGrid, step 1-1-1")

      existing_grid._spindles.remove(existing_spindle)
      existing_grid._spindles.append(new_spindle)
    #existing_spindle有與其他Grid相關聯
    else:
      print("updateGrid, step 1-1-2")

      # 建立新的Spindle
      clone_new_spindle = Spindle(
        spindle_type = _new_grid_type,                #類別, 1~3
        spindle_cat = _new_grid_cat,                  #型號
        spindle_outer = new_spindl.spindle_outer,     #外徑
        spindle_inner = new_spindl.spindle_inner,     #軸承內徑, 主軸內藏馬達有可能為 空白
        spindle_rpm = new_spindl.spindle_rpm,         #最高轉速
        spindle_motor = new_spindl.spindle_motor,     #馬達規格
        spindle_kw = new_spindl.spindle_kw,           #馬達功率S1
        spindle_nm = new_spindl.spindle_nm,           #馬達扭力S1
        spindle_lubrication = new_spindl.spindle_lubrication,   #潤滑方式, 1:油氣潤滑, 2:油脂潤滑
        spindle_cooling = new_spindl.spindle_cooling,           #冷卻方式, 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷
        spindle_handle = new_spindl.spindle_handle,             #刀把介面
      )

      s.add(clone_new_spindle)  # 添加新的 Spindle
      existing_grid._spindles.append(clone_new_spindle) # 關聯到 existing_grid

    try:
      s.commit()
      print("Spindle data updated successfully.")
      return_value = True
    except Exception as e:
      s.rollback()
      print("Error:", str(e))
      return_message='錯誤! API連線問題...'
      return_value = False
  #沒有spindle資料
  else:
    print("updateGrid, step 1-2")
    return_message="錯誤! 找不到主軸資料..."
    return_value = False

  s.close()

  return jsonify({
    'status': return_value,
    'message': return_message,
  })


# from reagent table update some data by id
@ updateTable.route("/updatePermissions", methods=['POST'])
def update_permissions():
  print("updatePermissions....")

  request_data = request.get_json()

  _id = request_data['perm_empID']

  _system = request_data['perm_checkboxForSystem']
  _admin = request_data['perm_checkboxForAdmin']
  _member = request_data['perm_checkboxForMember']

  return_value = True  # true: 資料正確, 註冊成功
  if _id == "":
      return_value = False  # false: 資料不完全 註冊失敗

  s = Session()
  if return_value:
      # 以最高權限寫入資料庫
      if _member:
          _p_id = 4
      if _admin:
          _p_id = 3
      if _system:
          _p_id = 2

      s.query(User).filter(User.emp_id == _id).update(
          {"perm_id": _p_id})

      s.commit()

  s.close()

  return jsonify({
      'status': return_value
  })
