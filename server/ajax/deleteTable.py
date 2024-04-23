from flask import Blueprint, jsonify, request
from sqlalchemy import func

from database.tables import User, Spindle, Grid, OutTag, InTag, SpindleRunIn, Session

#from werkzeug.security import generate_password_hash

deleteTable = Blueprint('deleteTable', __name__)


# ------------------------------------------------------------------


@deleteTable.route("/removeUser", methods=['POST'])
def remove_user():
    print("removeUser....")
    request_data = request.get_json()
    userID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    s.query(User).filter(User.emp_id == userID).update({'isRemoved': False})
    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


@deleteTable.route("/removeStockIn", methods=['POST'])
def remove_stockIn():
    print("removeStockIn....")
    request_data = request.get_json()
    inTag_id = (request_data['id'] or '')

    print("data: ", inTag_id)

    return_message = ''
    return_value = True  # true: 資料正確, 註冊成功
    if inTag_id == "":
        return_value = False  # false: 資料不完全 註冊失敗
        return_message = '資料錯誤!'

    if return_value:
        s = Session()
        #s.query(InTag).filter(InTag.id == inTag_id).update(
        #    {'isRemoved': False})
        item = s.query(InTag).filter_by(id=inTag_id, isPrinted=False, isStockin=False).first()
        s.delete(item)

        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })

# update reagent's 'isRemoved'


@deleteTable.route("/removeReagent", methods=['POST'])
def remove_reagent():
    print("removeReagent....")
    request_data = request.get_json()
    reagentID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if reagentID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    # s.query(Reagent).filter(Reagent.reag_id ==
    #                        reagentID).update({'isRemoved': False})
    item = s.query(Reagent).filter_by(reag_id=reagentID).first()
    s.delete(item)

    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# remove grid data table
@deleteTable.route("/removeSpindle", methods=['POST'])
def remove_spindle():
  print("removeSpindle....")

  request_data = request.get_json()
  print("request_data: ", request_data)

  _id = request_data['id']
  _tempT = request_data['spindle_type']
  #_spindle_type = 1 if _tempT == '銑削/研磨主軸(自動換刀)' else (2 if _tempT == '研磨主軸(手動換刀)' else 3)
  _spindle_type = 0 if _tempT == '' else (1 if _tempT == '銑削/研磨主軸(自動換刀)' else (2 if _tempT == '研磨主軸(手動換刀)' else 3))

  _spindle_cat = request_data['spindle_cat']
  _tempT = request_data['spindle_cooling']
  _spindle_cooling = 0 if _tempT == 'N/A' else (1 if _tempT == '水冷' else (2 if _tempT == '油冷' else 3))
  _spindle_handle = request_data['spindle_handle']
  _spindle_outer = request_data['spindle_outer']
  _spindle_inner = request_data['spindle_inner']
  _spindle_rpm = request_data['spindle_rpm']
  _spindle_kw = request_data['spindle_kw']
  _spindle_nm = request_data['spindle_nm']
  _tempT = request_data['spindle_lubrication']
  _spindle_lubrication = (2, 1)[_tempT == '油氣潤滑']
  _tempT=request_data['spindle_motor']
  _spindle_motor = (_tempT, '')[_tempT == '空白']

  return_value = True
  return_message = ''
  return_message=''

  s = Session()

  #從現有主軸找資料
  existing_spindle = s.query(Spindle).filter_by(id=_id, spindle_type=_spindle_type, spindle_cat=_spindle_cat).first()
  _count_spindles_on_grid = len(existing_spindle._grids)

  if _count_spindles_on_grid == 0:
    existing_spindle.isRemoved = False
    s.delete(existing_spindle)

    try:
      s.commit()
      print("Spindle data updated successfully.")
    except Exception as e:
      s.rollback()
      print("Error:", str(e))
      return_message='錯誤! API連線問題...'
      return_value = False
  else:
      return_message='錯誤! 儲位上有此筆資料, 暫時不能刪除...'
      return_value = False

  s.close()

  return jsonify({
      'status': return_value,
  })


# remove grid data table
@deleteTable.route("/removeSpindleRunIn", methods=['POST'])
def remove_spindle_runin():
  print("removeSpindleRunIn....")

  request_data = request.get_json()
  print("request_data: ", request_data)

  _id = request_data['id']

  return_value = True
  return_message=''

  s = Session()

  #從現有儲位/主軸找資料
  spindle_runin_to_delete = s.query(SpindleRunIn).filter_by(id=_id).first()

  if spindle_runin_to_delete:
      # 刪除該實例
      s.delete(spindle_runin_to_delete)

      try:
        s.commit()
        print(f"成功刪除 ID 為 {_id} 的 SpindleRunIn 實例")
        return_value = True
      except Exception as e:
        s.rollback()
        print("Error:", str(e))
        return_message='錯誤! API連線問題...'
        return_value = False
  else:
      return_message='錯誤! 找不到資料...'
      print(f"找不到 ID 為 {_id} 的 SpindleRunIn 實例")

  s.close()

  return jsonify({
    'status': return_value,
    'message': return_message,
  })


# remove grid data table
@deleteTable.route("/removeGrid", methods=['POST'])
def remove_grid():
  print("removeGrid....")

  request_data = request.get_json()
  print("request_data: ", request_data)

  _temp_id = request_data['id']
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
  print("_id, _existing_grid_type,  _existing_grid_cat: ", _id, _existing_grid_type,  _existing_grid_cat )

  return_value = True
  return_message=''

  s = Session()

  #從現有儲位/主軸找資料
  existing_grid = s.query(Grid).filter(Grid.id == _id).first()
  existing_spindle = s.query(Spindle).filter_by(spindle_type=_existing_grid_type, spindle_cat=_existing_grid_cat).first()
  if existing_spindle:
    existing_grid._spindles.remove(existing_spindle)

    _count_spindles_on_grid = len(existing_grid._spindles)
    if _count_spindles_on_grid == 1:
      existing_grid.isRemoved = False
      s.delete(existing_grid)

  else:
    existing_grid.isRemoved = False
    s.delete(existing_grid)

  try:
    s.commit()
    print("Spindle data updated successfully.")
    return_value = True
  except Exception as e:
    s.rollback()
    print("Error:", str(e))
    return_message='錯誤! API連線問題...'
    return_value = False

  s.close()

  return jsonify({
      'status': return_value,
  })

'''
# update product's 'isRemoved'
@deleteTable.route("/removeProduct", methods=['POST'])
def remove_product():
    print("removeProduct....")
    request_data = request.get_json()
    productID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if productID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    if return_value:
      s = Session()
      #s.query(Product).filter(Product.id ==
      #                        productID).update({'isRemoved': False})
      item = s.query(Product).filter_by(id=productID).first()
      s.delete(item)

      s.commit()
      s.close()

    return jsonify({
      'status': return_value,
      'message': return_message,
    })


# update department' 'isRemoved'
@deleteTable.route("/removeDepartment", methods=['POST'])
def remove_department():
    print("removeDepartment....")
    request_data = request.get_json()
    departmentID = request_data['ID']

    return_value = True  # true: 資料正確, 註冊成功
    if departmentID == "":
        return_value = False  # false: 資料不完全 註冊失敗

    if return_value:
        s = Session()
        #s.query(Department).filter(Department.id ==
        #                           departmentID).update({'isRemoved': False})
        item = s.query(Department).filter_by(id=departmentID).first()
        s.delete(item)

        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
    })
'''

# delete outtag item and update intag's stockOut_temp_count
@deleteTable.route("/deleteStockOutAndStockInData", methods=['POST'])
def delete_StockOut_and_StockIn_data():
    print("deleteStockOutAndStockInData....")
    request_data = request.get_json()

    _data = request_data['stockOut_array']
    _count = request_data['stockOut_count']
    print("_data, _count: ", _data, _count)

    return_value = True  # true: 資料正確
    if not _data or len(_data) != _count:
        return_value = False  # false: 資料不完全

    s = Session()
    outtag = s.query(OutTag).filter_by(id=_data['stockOutTag_ID']).first()
    s.delete(outtag)

    # 2023-01-31 mark the following block
    '''
    intag = s.query(InTag).filter_by(id=_data['stockOutTag_InID']).first()

    cursor = s.query(func.sum(OutTag.count)).filter(
        OutTag.intag_id == _data['stockOutTag_InID']).filter(
        OutTag.isRemoved == True)
    total = cursor.scalar()

    intag.stockOut_temp_count = total  # 修改入庫資料
    '''
    #
    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })
