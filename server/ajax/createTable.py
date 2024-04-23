import math

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from database.tables import User, Spindle, Permission, Grid, OutTag, InTag, Setting, SpindleRunIn, RunInData, Session
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

createTable = Blueprint('createTable', __name__)


# ------------------------------------------------------------------

# create user data and perm.id=1 into table
@createTable.route("/register", methods=['POST'])
def register():
    print("register....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    if emp_id == "" or emp_name == "" or sPWD == "":
      return_value = False  # false: 資料不完全 註冊失敗

    #dep = (request_data['dep'] or '')  # convert null into empty string

    s = Session()
    #department = s.query(Department).filter_by(dep_name=dep).first()
    #if not department:
    #    return_value = False  # if the user's department does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
      return_value = False  # if the user exist

    if return_value:
      new_user_setting = Setting(message='hello ' + emp_name,)
      s.add(new_user_setting)
      s.flush()
      new_user = User(emp_id=emp_id, emp_name=emp_name,
                      password=generate_password_hash(sPWD, method='scrypt'),   # 生成密碼, Werkzeug 3.0 版本
                      #dep_id=department.id,
                      #dep_id=1,
                      perm_id=4,  # member
                      setting_id=new_user_setting.id)
      s.add(new_user)

      s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# create user data and perm.id=4 into table
@createTable.route("/createUser", methods=['POST'])
def createUser():
    print("createUser....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    tempID = ""
    tempName = ""
    if emp_id == "" or emp_name == "" or sPWD == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string
    # code = request_data['perm_id']

    s = Session()
    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    # permission = s.query(Permission).filter_by(auth_code=code).first()
    # if not permission:
    #    return_value = False  # if the user's permission does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
        tempID = old_user.emp_id  # 歷史資料中的員工編號
        tempName = old_user.emp_name
        return_value = False  # if the user exist

    if return_value:
        new_user_setting = Setting(
            message='add ' + emp_name,)
        s.add(new_user_setting)
        s.flush()
        new_user = User(emp_id=emp_id,
                        emp_name=emp_name,
                        password=generate_password_hash(sPWD, method='sha256'),
                        dep_id=department.id,
                        # perm_id=permission.id,
                        perm_id=4,  # first permission,auth_code=0:none
                        setting_id=new_user_setting.id,)
        s.add(new_user)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value,
        'returnID': tempID,
        'returnName': tempName,
    })


@createTable.route("/createSpindleRunins", methods=['POST'])
def create_spindle_runins():
    print("createSpindleRunins....")

    request_data = request.get_json()
    #print("request_data: ", request_data)

    _obj = request_data['block']
    #_count = request_data['count']
    _cat=request_data['spindleRunIn_spindle_cat']
    _empID = request_data['spindleRunIn_employer_emp_id']


    return_value = True  # true: 資料正確, true
    return_message=''
    s = Session()

    _spindle = s.query(Spindle).filter_by(spindle_cat=_cat).first()
    _user = s.query(User).filter_by(emp_id=_empID).first()

    _spindleRunIn_excel_file = request_data['spindleRunIn_excel_file']
    _spindleRunIn_customer = request_data['spindleRunIn_customer']
    _spindleRunIn_work_id = request_data['spindleRunIn_id']
    _spindleRunIn_date = request_data['spindleRunIn_date']

    if (not _spindle or not _user):
      return_value = False  # true: 資料正確, true
      return_message= '錯誤! 在' + _spindleRunIn_excel_file + '內, 系統沒有主軸' + _cat + '或員工編號' + _empID + '資料...'
    else:
      new_spindle_runin = SpindleRunIn(
        spindleRunIn_excel_file = _spindleRunIn_excel_file,
        spindleRunIn_customer = _spindleRunIn_customer,
        spindleRunIn_work_id = _spindleRunIn_work_id,
        spindleRunIn_spindle_id = _spindle.id,
        spindleRunIn_employer = _user.id,
        spindleRunIn_date = _spindleRunIn_date,
      )

      s.add(new_spindle_runin)
      s.flush()
      spindle_runin_id = new_spindle_runin.id
      print("spindle_runin_id: ", spindle_runin_id)

      runin_data_total_size = len(_obj)
      _objects = []
      for x in range(runin_data_total_size):
        u = RunInData(
        spindleRunIn_id = spindle_runin_id,
        spindleRunIn_period = _obj[x]['spindleRunIn_period'],
        spindleRunIn_speed_level = _obj[x]['spindleRunIn_speed_level'],
        spindleRunIn_speed = _obj[x]['spindleRunIn_speed'],
        spindleRunIn_stator_temp = _obj[x]['spindleRunIn_stator_temp'],
        spindleRunIn_inner_frontBearing_temp = _obj[x]['spindleRunIn_inner_frontBearing_temp'],
        spindleRunIn_inner_backBearing_temp = _obj[x]['spindleRunIn_inner_backBearing_temp'],
        spindleRunIn_outer_frontBearing_temp = _obj[x]['spindleRunIn_outer_frontBearing_temp'],
        spindleRunIn_outer_backBearing_temp = _obj[x]['spindleRunIn_outer_backBearing_temp'],
        spindleRunIn_room_temp = _obj[x]['spindleRunIn_room_temp'],
        spindleRunIn_coolWater_temp = _obj[x]['spindleRunIn_coolWater_temp'],
        spindleRunIn_Rphase_current = _obj[x]['spindleRunIn_Rphase_current'],
        spindleRunIn_Sphase_current = _obj[x]['spindleRunIn_Sphase_current'],
        spindleRunIn_Tphase_current = _obj[x]['spindleRunIn_Tphase_current'],
        spindleRunIn_cool_pipeline_flow = _obj[x]['spindleRunIn_cool_pipeline_flow'],
        spindleRunIn_cool_pipeline_pressure = _obj[x]['spindleRunIn_cool_pipeline_pressure'],
        spindleRunIn_frontBearing_vibration_speed1 = _obj[x]['spindleRunIn_frontBearing_vibration_speed1'],
        spindleRunIn_frontBearing_vibration_acc1 = _obj[x]['spindleRunIn_frontBearing_vibration_acc1'],
        spindleRunIn_frontBearing_vibration_disp1 = _obj[x]['spindleRunIn_frontBearing_vibration_disp1'],
        spindleRunIn_frontBearing_vibration_speed2 = _obj[x]['spindleRunIn_frontBearing_vibration_speed2'],
        spindleRunIn_frontBearing_vibration_acc2 = _obj[x]['spindleRunIn_frontBearing_vibration_acc2'],
        spindleRunIn_frontBearing_vibration_disp2 = _obj[x]['spindleRunIn_frontBearing_vibration_disp2'],
        spindleRunIn_backBearing_vibration_speed1 = _obj[x]['spindleRunIn_backBearing_vibration_speed1'],
        spindleRunIn_backBearing_vibration_acc1 = _obj[x]['spindleRunIn_backBearing_vibration_acc1'],
        spindleRunIn_backBearing_vibration_disp1 = _obj[x]['spindleRunIn_backBearing_vibration_disp1'],
        spindleRunIn_backBearing_vibration_speed2 = _obj[x]['spindleRunIn_backBearing_vibration_speed2'],
        spindleRunIn_backBearing_vibration_acc2 = _obj[x]['spindleRunIn_backBearing_vibration_acc2'],
        spindleRunIn_backBearing_vibration_disp2 = _obj[x]['spindleRunIn_backBearing_vibration_disp2'],
        )
        _objects.append(u)

      s.bulk_save_objects(_objects)

      try:
          s.commit()
      except pymysql.err.IntegrityError as e:
          s.rollback()
      except exc.IntegrityError as e:
          s.rollback()
      except Exception as e:
          s.rollback()

      spindle_runin_record = s.query(SpindleRunIn).filter_by(id=spindle_runin_id).first()
      runin_data_records = s.query(RunInData).filter_by(spindleRunIn_id=spindle_runin_id).all()

      for array in runin_data_records:
        spindle_runin_record._runin_data.append(array)

      try:
          s.commit()
      except pymysql.err.IntegrityError as e:
          s.rollback()
      except exc.IntegrityError as e:
          s.rollback()
      except Exception as e:
          s.rollback()
    #end if-else

    s.close()

    return jsonify({
      'status': return_value,
      'message': return_message,
    })


# create InTag data into table
@createTable.route("/createStockInGrids", methods=['POST'])
def create_stockin_grids():
    print("createStockInGrids....")

    request_data = request.get_json()
    print("request_data: ", request_data)

    _work_id = request_data['work_id']    #製令單號
    _empID = request_data['empID']        #員工編號
    _spindle_id = request_data['spindle_id']
    _stockin_date = request_data['stockin_date']        #入庫日
    _stockin_period = request_data['stockin_period']    #效期
    _grid_id = request_data['grid_id']
    _count = request_data['count']

    return_value = True  # true: 資料正確, true
    return_message=''

    s = Session()
    _user = s.query(User).filter_by(emp_id=_empID).first()
    _grid = s.query(Grid).filter_by(id=_grid_id).first()

    new_intag = InTag(work_id=_work_id, user_id=_user.id, spindle_id=_spindle_id, date=_stockin_date, period=_stockin_period, count=_count)

    s.flush()

    _grid._intags_g_i.extend([new_intag])
    _grid.total_size = _grid.total_size + _count
    s.add_all([_grid])

    try:
        s.commit()
    except pymysql.err.IntegrityError as e:
        s.rollback()
    except exc.IntegrityError as e:
        s.rollback()
    except Exception as e:
        s.rollback()

    s.close()

    return jsonify({
      'status': return_value,
      'message': return_message,
    })


# create InTag data into table
@createTable.route("/addStockInItem", methods=['POST'])
def add_stockin_item():
    print("addStockInItem....")
    request_data = request.get_json()

    _id = request_data['InTagID']
    _count = (request_data['InTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockIn, 入庫: ", _id, _count)

    s = Session()

    intag_item = s.query(InTag).filter_by(id=_id).first()
    # 狀況1, 數量不同(add=>isStockin, _count; modify=>isPrinted, cnt - _count)
    print("intag_item.count: ", intag_item.count, _count)
    if (intag_item.count != _count):  #部分入庫
        print("部分入庫, status 1...")

        new_intag = InTag(user_id=intag_item.user_id,
                          reagent_id=intag_item.reagent_id,
                          count=_count,
                          ori_count=_count,     # 2023-07-11 add
                          reag_period=intag_item.reag_period,
                          batch=intag_item.batch,
                          intag_date=intag_item.intag_date,
                          stockIn_alpha=intag_item.stockIn_alpha,
                          #grid_id=intag_item.grid_id, # 2023-01-12 mark
                          isStockin=True)
        s.add(new_intag)

        s.query(InTag).filter(InTag.id == _id).update({
            'isStockin': False,
            'isPrinted': True,
            'count': intag_item.count - _count,
        })
    # 狀況2, 數量相同(add=>isStockin, _count;  modify=>isPrinted false)
    else: #全部入庫
        print("全部入庫, status 2...")
        new_intag = InTag(user_id=intag_item.user_id,
                          reagent_id=intag_item.reagent_id,
                          count=_count,
                          ori_count=_count,     # 2023-07-11 add
                          reag_period=intag_item.reag_period,
                          batch=intag_item.batch,
                          intag_date=intag_item.intag_date,
                          stockIn_alpha=intag_item.stockIn_alpha,
                          #grid_id=intag_item.grid_id, # 2023-01-12 mark
                          isStockin=True)
        s.add(new_intag)
        '''
        s.query(InTag).filter(InTag.id == _id).update({
            'isStockin': False,
            'isPrinted': False,
            # 'count': intag_item.count - _count,
        })
        '''
        del_obj = s.query(InTag).filter(InTag.id == _id).delete()
        print("del_obj: ", del_obj)

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# create InTag data into table
@createTable.route("/addStockOutItem", methods=['POST'])
def add_stockout_item():
    print("addStockOutItem....")
    request_data = request.get_json()

    _id = request_data['OutTagID']
    _count = (request_data['OutTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockOut, 領料: ", _id, _count)

    s = Session()

    outtag_item = s.query(OutTag).filter_by(id=_id).first()
    intag_item = s.query(InTag).filter_by(id=outtag_item.intag_id).first()
    _reagent = s.query(Reagent).filter_by(id=intag_item.reagent_id).first()

    if (outtag_item.count != _count):  # 部分領料
      #新增領料紀錄(isStockout=True)
      new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                          count=_count,
                          #unit=outtag_item.unit,       # 2023-01-13 mark
                          outtag_date=outtag_item.outtag_date,

                          stockOut_alpha=outtag_item.stockOut_alpha,
                          isStockout=True)
      s.add(new_outtag)
      #修改目前待領料紀錄(isPrinted=True)
      outtag_item.count = outtag_item.count - _count

      if (_reagent.reag_scale == 1):  #單位相同
        print("狀況1, 部分領料, 出入庫單位相同")  #出入庫單位相同
        '''
        #新增領料紀錄(isStockout=True)
        new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                            count=_count,
                            #unit=outtag_item.unit,       # 2023-01-13 mark
                            outtag_date=outtag_item.outtag_date,

                            stockOut_alpha=outtag_item.stockOut_alpha,
                            isStockout=True)
        s.add(new_outtag)
        '''

        '''
        s.query(OutTag).filter(OutTag.id == _id).update({
            'isStockout': False,
            'isPrinted': True,
            'count': outtag_item.count - _count,
        })
        '''

        '''
        #修改目前待領料紀錄(isPrinted=True)
        outtag_item.count = outtag_item.count - _count
        '''
        #stockin_item = s.query(InTag).filter_by(id == outtag_item.intag_id).first()
        ##stockin_item = s.query(InTag).filter_by(id = outtag_item.intag_id).first()
        ##tt = stockin_item.count - _count
        #修改領料後,原來在庫紀錄(isStockin=True)
        tt = intag_item.count - _count
        if (tt != 0):
          #s.query(InTag).filter(InTag.id == outtag_item.intag_id).update({'count': tt})
          intag_item.count=tt
        else:
          s.delete(intag_item)
      else: #單位不相同
        print("狀況2, 部分領料, 出入庫單位不同")  #出入庫單位不同

        '''
        new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                            count=_count,
                            #unit=outtag_item.unit,       # 2023-01-13 mark
                            outtag_date=outtag_item.outtag_date,
                            stockOut_alpha=outtag_item.stockOut_alpha,
                            isStockout=True)
        s.add(new_outtag)
        '''

        #stockin_item = s.query(InTag).filter_by(id == outtag_item.intag_id).first()
        #stockin_item = s.query(InTag).filter_by(id = outtag_item.intag_id).first()
        '''
        tt = intag_item.count * _reagent.reag_scale - _count

        myInCount=tt/_reagent.reag_scale
        myInCount=math.ceil(myInCount*10)
        myInCount=myInCount/10
        '''
####
        temp_count = _count * -1
        temp_scale = _reagent.reag_scale
        for intag_row in s.query(InTag):
          if (not (intag_row.id==outtag_item.intag_id and intag_row.isRemoved and (not intag_row.isPrinted) and intag_row.isStockin)):
            continue

          myReturn=intag_row.count * temp_scale + temp_count   #入庫出庫單位轉換

          if (myReturn==0): #該筆入庫數量與出庫數量相同(單位已轉換)
            intag_row.isRemoved=False
            intag_item.isStockin=False
            intag_item.count=0
            break

          if (myReturn>0):  #該筆入庫數量大於出庫數量(單位已轉換)
            myInCount=myReturn / _reagent.reag_scale

            #myInCount=math.floor(myInCount*10)  # 取小數點1位  # 2023-07-11 modify
            #myInCount=myInCount/10
            myInCount=math.floor(myInCount*1000)  # 取小數點3位
            myInCount=round(myInCount/1000, 0)         # 取整數, # 2023-07-12 modify

            intag_item.count=myInCount
            break

          if (myReturn<0):  #該筆入庫數量小於出庫數量(單位已轉換)
            intag_row.isRemoved=False
            intag_item.isStockin=False
            intag_item.count=0
            temp_count=myReturn
####
        '''
        myInCount=item.count * _reagent.reag_scale
        myInCount=myInCount - myOutCount
        myInCount=myInCount/_reagent.reag_scale
        myInCount=math.ceil(myInCount*10)
        myInCount=myInCount/10
        '''

        '''
        if (tt != 0):
          s.query(InTag).filter(InTag.id == outtag_item.intag_id).update(
                {'count': myInCount})
        else:
          s.delete(stockin_item)
        '''
    else:  # 全部領料
      '''
      new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id, count=_count,
                          #unit=outtag_item.unit,        # 2023-01-13 mark
                          outtag_date=outtag_item.outtag_date,
                          stockOut_alpha=outtag_item.stockOut_alpha,
                          isStockout=True)
      s.add(new_outtag)
      '''
      outtag_item.count = _count
      outtag_item.isPrinted = False
      outtag_item.isStockout = True
      #if (_reagent.reag_scale == 1):  #單位相同
      print("狀況3/4, 全部領料, 出入庫單位相同/出入庫單位不同")  #出入庫單位相同
      #
      #_objects = s.query(InTag).all()
      #for intag in _objects:
      temp_count = _count * -1
      temp_scale = _reagent.reag_scale
      for intag_row in s.query(InTag):
        if (not (intag_row.id==outtag_item.intag_id and intag_row.isRemoved and (not intag_row.isPrinted) and intag_row.isStockin)):
          continue

        myReturn = intag_row.count * temp_scale + temp_count   #入庫出庫單位轉換

        if (myReturn==0): #該筆入庫數量與出庫數量相同(單位已轉換)
          print("a, 該筆入庫數量與出庫數量相同(單位已轉換)...")
          intag_row.isRemoved=False
          intag_item.isStockin=False
          intag_item.count=0
          break

        if (myReturn>0):  #該筆入庫數量大於出庫數量(單位已轉換)
          print("b, 該筆入庫數量大於出庫數量(單位已轉換)...")
          myInCount=myReturn / temp_scale
          print("b-1, myInCount ",myInCount)
          # 2023-06-02 modify
          #myInCount=math.floor(myInCount*10)   # 取小數點1位
          myInCount=math.floor(myInCount*1000)  # 取小數點3位
          print("b-2, myInCount ",myInCount)
          # 2023-06-02 modify
          #myInCount=myInCount/10
          myInCount=round(myInCount/1000, 0)         # 取整數, # 2023-07-12 modify
          print("b-3, myInCount ",myInCount)
          # 2023-06-02 modify
          #intag_item.count=myInCount
          intag_item.count=round(myInCount, 2)
          break

        if (myReturn<0):  #該筆入庫數量小於出庫數量(單位已轉換)
          print("c, 該筆入庫數量小於出庫數量(單位已轉換)...")
          intag_row.isRemoved=False
          intag_item.isStockin=False
          intag_item.count=0
          temp_count=myReturn

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


'''
# create InTag data into table
@createTable.route("/addStockOutItem", methods=['POST'])
def add_stockout_item():
    print("addStockOutItem....")
    request_data = request.get_json()

    _id = request_data['InTagID']
    _count = (request_data['InTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockOut, 領料: ", _id, _count)

    s = Session()

    s.query(OutTag).filter(OutTag.id == _id).update({
        'isStockout': True,  # true:已入庫
        'count': _count,
    })

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })
'''

# create reagent data table


@createTable.route("/createReagent", methods=['POST'])
def create_reagent():
    print("createReagent....")
    request_data = request.get_json()

    _block = request_data['block']
    #_emp_dep = _block['dep_name']
    print("_block", _block)

    _id = _block['reag_id']
    _name = _block['reag_name']
    _product = _block['reag_product']
    _in_unit = _block['reag_In_unit']
    _out_unit = _block['reag_Out_unit']
    _scale = _block['reag_scale']
    # _period = _block['reag_period']    #依2022-12-12操作教育訓練建議作修正
    _stock = _block['reag_stock']
    _temp = _block['reag_temp']
    _catalog = _block['reag_catalog']

    return_value = True  # true: 資料正確, 註冊成功
    tempID = ""
    tempName = ""

    # if _id == "" or _name == "" or _in_unit == "" or _out_unit == "" or _scale == "" or _stock == "" or _temp == "" or _catalog == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    # convert null into empty string
    _supplier = _block['reag_supplier']

    s = Session()

    supplier = s.query(Supplier).filter_by(super_name=_supplier).first()
    if not supplier:
        return_value = False  # if the reagent's supplier does not exist
        print("step1")

    product = s.query(Product).filter_by(name=_product).first()
    if not product:
        return_value = False  # if the reagent's product does not exist
        print("step2")

    cat_item = s.query(Department).filter_by(dep_name=_catalog).first()
    if not cat_item:
        return_value = False  # if the reagent's product does not exist
        print("step2-1")

    old_reagent = s.query(Reagent).filter_by(reag_id=_id).first()
    if old_reagent:
        tempID = old_reagent.reag_id
        tempName = old_reagent.reag_name
        return_value = False  # if the user exist
        print("step3")

    if return_value:
        _scale = int(_scale)
        _stock = float(_stock)

        if _temp == '室溫':  # 0:室溫、1:2~8度C、2:-20度C
            k1 = 0
        if _temp == '2~8度C':
            k1 = 1
        if _temp == '-20度C':
            k1 = 2

        new_reagent = Reagent(reag_id = _id,
                              reag_name = _name,
                              reag_In_unit = _in_unit,
                              reag_Out_unit = _out_unit,
                              # reag_period=_period,    #依2022-12-12操作教育訓練建議作修正
                              reag_scale = _scale,
                              reag_stock = _stock,
                              reag_temp = k1,
                              # reag_catalog=_catalog,
                              catalog_id = cat_item.id,
                              product_id = product.id,
                              super_id = supplier.id)
        s.add(new_reagent)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value,
        'returnID': tempID,
        'returnName': tempName,
    })


# create grid data table
@createTable.route("/createGrid", methods=['POST'])
def create_grid():
  print("createGrid....")

  request_data = request.get_json()
  _spindle_type = request_data['grid_type']
  _spindle_cat = request_data['grid_cat']
  _station = request_data['grid_station']
  _layout = request_data['grid_layout']
  _grid_max_size = request_data['grid_max_size']

  return_value = True
  s = Session()

  existing_grid = s.query(Grid).filter_by(station=_station, layout=_layout).first()
  if existing_grid:
    print("Grid already exists with the same station and layout.")
    return_value = False
  else:
    new_grid = Grid(station=_station, layout=_layout)
    s.add(new_grid)
    s.flush()
    existing_spindle = s.query(Spindle).filter_by(spindle_type=_spindle_type, spindle_cat=_spindle_cat).first()
    if existing_spindle:
      new_grid.isAll = False    #2024-03-30 add
      new_grid._spindles.extend([existing_spindle])
      s.add_all([new_grid])
      #s.commit() #2024-03-30 mark
      print("Existing spindles associated with grid9.")
    else:
      print("No spindle created and associated with new_grid.")
      #return_value = False #2024-03-30 mark
    s.commit()  #2024-03-30 add
  s.close()

  return jsonify({
      'status': return_value
  })


# create spindle data table
@createTable.route("/createSpindle", methods=['POST'])
def create_spindle():
  print("createSpindle....")

  request_data = request.get_json()
  print("request_data: ", request_data)
  _spindle_type = int(request_data['spindle_type'])
  _spindle_cat = request_data['spindle_cat']
  _spindle_outer = request_data['spindle_outer']
  _spindle_inner = request_data['spindle_inner']
  _spindle_lubrication=int(request_data['spindle_lubrication'])
  _spindle_rpm = request_data['spindle_rpm']
  _spindle_motor = request_data['spindle_motor']
  temp_str=request_data['spindle_motor']
  _spindle_motor = (temp_str, '')[temp_str == '空白']
  _spindle_kw = request_data['spindle_kw']
  _spindle_nm = request_data['spindle_nm']
  _spindle_cooling= int(request_data['spindle_cooling'])
  _spindle_handle=request_data['spindle_handle']

  return_value = True
  return_message = ''
  s = Session()

  new_spindle = Spindle(
    spindle_type =_spindle_type,
    spindle_cat = _spindle_cat,
    spindle_outer = _spindle_outer,
    spindle_inner = _spindle_inner,
    spindle_lubrication = _spindle_lubrication,
    spindle_rpm = _spindle_rpm,
    spindle_motor = _spindle_motor,
    spindle_kw = _spindle_kw,
    spindle_nm = _spindle_nm,
    spindle_cooling = _spindle_cooling,
    spindle_handle = _spindle_handle,
  )

  s.add(new_spindle)

  try:
    s.commit()
    print("Spindle data create successfully.")
  except Exception as e:
    s.rollback()
    print("Error:", str(e))
    return_message = '錯誤! 主軸資料新增沒有成功...'
    return_value = False

  s.close()

  return jsonify({
      'status': return_value,
      'message': return_message,
  })


'''
# create supplier data table
@createTable.route("/createSupplier", methods=['POST'])
def create_supplier():
    print("createSupplier....")
    request_data = request.get_json()

    _supID = request_data['sup_id']
    _supName = request_data['sup_name']
    _supAddress = request_data['sup_address']
    _supContact = request_data['sup_contact']
    _supPhone = request_data['sup_phone']
    _supProducts = request_data['sup_products']
    print("_supProducts: ", _supProducts)

    #data_check = (True, False)[_supID == "" or _supName == "" or _supAddress == "" or _supContact == "" or _supPhone == "" or len(_supProducts) == 0]
    data_check = (True, False)[_supID == "" or _supName == "" or _supContact == "" or len(_supProducts) == 0]

    return_value = True  # true: 資料正確, 註冊成功
    if not data_check:
        return_value = False  # false: 資料不完全 註冊失敗
        print("step1, error 供應商資料空白!")

    s = Session()

    old_supplier = s.query(Supplier).filter(or_(Supplier.super_id==_supID, Supplier.super_name==_supName)).first()

    if old_supplier:
        return_value = False  # if the supplier exist
        print("step2, error 供應商資料重複!")

    if return_value:
        new_supplier = Supplier(super_id=_supID, super_name=_supName,
                                super_address=_supAddress, super_connector=_supContact, super_tel=_supPhone)

        s.add(new_supplier)

        s.flush()
        tempID=new_supplier.id
        print("tempID", tempID)

        for array in _supProducts:
            target = s.query(Product).filter_by(name=array).first()
            new_supplier._products.append(target)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''

'''
# create product data table
@createTable.route("/createProduct", methods=['POST'])
def create_product():
    print("createProduct....")
    request_data = request.get_json()

    _prdName = request_data['prd_name']

    data_check = (True, False)[_prdName == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()

    old_product = s.query(Product).filter_by(name=_prdName).first()
    if old_product:
        return_value = False  # the product record had existed

    if return_value:
        new_product = Product(name=_prdName)

        s.add(new_product)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''

'''
# create department data table
@createTable.route("/createDepartment", methods=['POST'])
def create_department():
    print("createDepartment....")
    request_data = request.get_json()

    _block = request_data['block']
    _emp_dep = _block['dep_name']

    data_check = (True, False)[_emp_dep == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()
    old_department = s.query(Department).filter_by(dep_name=_emp_dep).first()
    if old_department:
        return_value = False  # the product record had existed

    if return_value:
        new_department = Department(dep_name=_emp_dep)
        s.add(new_department)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''

# create stockout data into table
@createTable.route("/createStockOutGrids", methods=['POST'])
def create_stockout_grids():
    print("createStockOutGrids....")

    request_data = request.get_json()
    print("request_data: ", request_data)

    _work_id = request_data['work_id']    #製令單號
    _empID = request_data['empID']        #員工編號
    _stockout_date = request_data['stockout_date']        #出庫日

    return_value = True  # true: 資料正確
    return_message='資料ok!'

    return_array = []
    return_value = True  # true: 資料正確

    s = Session()

    _user = s.query(User).filter_by(emp_id=_empID).first()
    _intag = s.query(InTag).filter_by(work_id=_work_id).first()

    if (not _user) or ( not _intag):
        return_value = False  # if the user's department does not exist
        return_message='找不到資料!'

    _intag.isRemoved = False
    #s.query(InTag).filter_by(work_id=_work_id).update(
    #    {'items_per_page': newSetting})

    new_outtag = OutTag(
      intag_id=_intag.id,
      user_id=_user.id,
      date=_stockout_date,
    )

    _intag._outstocks.append(new_outtag)

    s.add(new_outtag)

    try:
        s.commit()
    except pymysql.err.IntegrityError as e:
        s.rollback()
    except exc.IntegrityError as e:
        s.rollback()
    except Exception as e:
        s.rollback()

    s.close()

    print(return_message)

    return jsonify({
        'status': return_value,
    })


'''


for key in Boys.keys():
    if key in Dict.keys():
        print True
    else:
        print False

    s = Session()
    if return_value:
        _objects = s.query(OutTag).all()
        for outtagKey in _objects.keys():
            if outtagKey in _data.keys():

            new_department = OutTag(dep_name=_emp_dep)
            s.add(new_department)
            s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''
