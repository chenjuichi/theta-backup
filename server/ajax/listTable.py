import math
import random
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.sql import func
# from werkzeug.security import check_password_hash
from database.tables import User, Permission, Spindle, Grid, association_table
from database.tables import SpindleRunIn, RunInData
from database.tables import InTag, OutTag, Session

from flask_cors import CORS

from operator import itemgetter

from dotenv import dotenv_values

import pymysql
from sqlalchemy import exc

listTable = Blueprint('listTable', __name__)

# ------------------------------------------------------------------

@listTable.route("/listFileOK", methods=['GET'])
def list_file_ok():
  print("listFileOK....")

  _file_ok = current_app.config['file_ok']
  print("file_ok flag value is: ", _file_ok)

  if _file_ok:
    current_app.config['file_ok'] = False
    #file_ok = False

  return jsonify({
    'outputs': _file_ok
  })


@listTable.route("/listDotEnv", methods=['GET'])
def list_dot_env():
  print("listDotEnv....")

  env_path = current_app.config['envDir']
  #env_path = "./.env"                        # 主目錄下的 .env 文件path
  #env_path = "d:\\theta-asrs\\asrs\\.env"     # 2024-04-26 modify
  env_vars = dotenv_values(env_path)

  schedule_1_str= env_vars["schedule_1_24HHMM"]
  schedule_1 = schedule_1_str.split(",")
  schedule_2_str= env_vars["schedule_2_24HHMM"]
  schedule_2 = schedule_2_str.split(",")

  #主軸型號
  spindle_cat_str= env_vars["spindle_cat1"]
  spindle_cat1 = spindle_cat_str.split(",")
  spindle_cat_str= env_vars["spindle_cat2"]
  spindle_cat2 = spindle_cat_str.split(",")
  spindle_cat_str= env_vars["spindle_cat3"]
  spindle_cat3 = spindle_cat_str.split(",")
  #主軸外徑(mm)
  spindle_outer_str= env_vars["spindle_outer1"]
  spindle_outer1 = spindle_outer_str.split(",")
  spindle_outer_str= env_vars["spindle_outer2"]
  spindle_outer2 = spindle_outer_str.split(",")
  #前軸承內徑(mm)
  spindle_inner_str= env_vars["spindle_inner1"]
  spindle_inner1 = spindle_inner_str.split(",")
  spindle_inner_str= env_vars["spindle_inner2"]
  spindle_inner2 = spindle_inner_str.split(",")
  #最高轉速(rpm)
  spindle_rpm_str= env_vars["spindle_rpm1"]
  spindle_rpm1 = spindle_rpm_str.split(",")
  spindle_rpm_str= env_vars["spindle_rpm2"]
  spindle_rpm2 = spindle_rpm_str.split(",")
  #馬達規格
  spindle_motor_str= env_vars["spindle_motor1"]
  spindle_motor1 = spindle_motor_str.split(",")
  spindle_motor_str= env_vars["spindle_motor2"]
  spindle_motor2 = spindle_motor_str.split(",")
  #馬達功率 S1(Kw)
  spindle_S1Kw_str= env_vars["spindle_S1Kw1"]
  spindle_S1Kw1=spindle_S1Kw_str.split(",")
  spindle_S1Kw_str= env_vars["spindle_S1Kw2"]
  spindle_S1Kw2=spindle_S1Kw_str.split(",")
  #馬達扭力 S1(Nm)
  spindle_S1Nm_str= env_vars["spindle_S1Nm1"]
  spindle_S1Nm1=spindle_S1Nm_str.split(",")
  spindle_S1Nm_str= env_vars["spindle_S1Nm2"]
  spindle_S1Nm2=spindle_S1Nm_str.split(",")
  #刀把介面
  spindle_handles_str= env_vars["spindle_handles1"]
  spindle_handles1 = spindle_handles_str.split(",")
  spindle_handles_str= env_vars["spindle_handles2"]
  spindle_handles2 = spindle_handles_str.split(",")
  spindle_handles_str= env_vars["spindle_handles3"]
  spindle_handles3 = spindle_handles_str.split(",")
  spindle_handles_str= env_vars["spindle_handles4"]
  spindle_handles4 = spindle_handles_str.split(",")
  spindle_handles_str= env_vars["spindle_handles5"]
  spindle_handles5 = spindle_handles_str.split(",")

  return jsonify({
    'schedule_1': schedule_1,
    'schedule_2': schedule_2,
    'spindle_cat1': spindle_cat1,
    'spindle_cat2': spindle_cat2,
    'spindle_cat3': spindle_cat3,
    'spindle_outer1': spindle_outer1,
    'spindle_outer2': spindle_outer2,
    'spindle_inner1': spindle_inner1,
    'spindle_inner2': spindle_inner2,
    'spindle_rpm1': spindle_rpm1,
    'spindle_rpm2': spindle_rpm2,
    'spindle_motor1': spindle_motor1,
    'spindle_motor2': spindle_motor2,
    'spindle_S1Kw1': spindle_S1Kw1,
    'spindle_S1Kw2': spindle_S1Kw2,
    'spindle_S1Nm1': spindle_S1Nm1,
    'spindle_S1Nm2': spindle_S1Nm2,
    'spindle_handles1': spindle_handles1,
    'spindle_handles2': spindle_handles2,
    'spindle_handles3': spindle_handles3,
    'spindle_handles4': spindle_handles4,
    'spindle_handles5': spindle_handles5,
  })


# list all users
@listTable.route("/listUsers", methods=['GET'])
def list_users():
    print("listUsers....")

    s = Session()
    _user_results = []
    return_value = True
    _objects = s.query(User).all()
    users = [u.__dict__ for u in _objects]
    for user in users:
        perm_item = s.query(Permission).filter_by(id=user['perm_id']).first()
        if (user['isRemoved']):
            _user_object = {
                'emp_id': user['emp_id'],
                'emp_name': user['emp_name'],
                'emp_perm': perm_item.auth_code,
            }
            _user_results.append(_user_object)
    s.close()

    temp_len = len(_user_results)
    print("listUsers, 員工總數: ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _user_results
    })


# list spindles
@listTable.route("/listSpindles", methods=['GET'])
def list_reagents():
    print("listSpindles....")

    _results = []
    return_value = True
    s = Session()
    _objects = s.query(Spindle).all()
    spindles = [u.__dict__ for u in _objects]
    for spindle in spindles:
      k0 = ''
      if spindle['spindle_type'] == 1:
        k0 = '銑削/研磨主軸(自動換刀)'
      if spindle['spindle_type'] == 2:
        k0 = '研磨主軸(手動換刀)'
      if spindle['spindle_type'] == 3:
        k0 = '修砂主軸(手動換刀)'
      k1 = ''
      if spindle['spindle_lubrication'] == 1:  # 1:油氣潤滑, 2:油脂潤滑
        k1 = '油氣潤滑'
      if spindle['spindle_lubrication'] == 2:
        k1 = '油脂潤滑'
      k2 = ''
      if spindle['spindle_cooling'] == 0:  # 0: N/A, 1:水冷, 2:油冷, 3:水冷/油冷
        k2 = 'N/A'
      if spindle['spindle_cooling'] == 1:
        k2 = '水冷'
      if spindle['spindle_cooling'] == 2:
        k2 = '油冷'
      if spindle['spindle_cooling'] == 3:
        k2 = '水冷/油冷'

      if (spindle['isRemoved']):
        _obj = {
          'id': spindle['id'],
          'isAll': spindle['isAll'],
          'spindle_type': k0,
          'spindle_cat': spindle['spindle_cat'],
          'spindle_outer': spindle['spindle_outer'],
          'spindle_inner': spindle['spindle_inner'],
          'spindle_rpm': spindle['spindle_rpm'],
          'spindle_motor': spindle['spindle_motor'],
          'spindle_kw': spindle['spindle_kw'],
          'spindle_nm': spindle['spindle_nm'],
          'spindle_lubrication': k1,
          'spindle_cooling': k2,
          'spindle_handle':spindle['spindle_handle'],
        }

        _results.append(_obj)
    s.close()

    temp_len = len(_results)
    print("Spindle總數量: ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results,
    })


# list permission all data(theta)
@listTable.route("/listPermissions", methods=['GET'])
def list_permissions():
    print("listPermissions....")
    s = Session()
    _results = []
    _objects = s.query(User).all()
    users = [u.__dict__ for u in _objects]
    for user in users:
        #dep_item = s.query(Department).filter_by(id=user['dep_id']).first()

        perm_item = s.query(Permission).filter_by(id=user['perm_id']).first()
        k1 = False
        k2 = False
        k3 = False
        # print("permission: ", perm_item.auth_code)
        if perm_item.auth_code == 1:  # 0:none, 1:system, 2:admin, 3:member
            k1 = True
        if perm_item.auth_code == 2:
            k2 = True
        if perm_item.auth_code == 3:
            k3 = True
        # print("permission: ", k1, k2, k3)
        if (user['isRemoved']):
            _obj = {
                'perm_empID': user['emp_id'],
                'perm_empName': user['emp_name'],
                #'perm_empDep': dep_item.dep_name,
                'perm_empDep': '',
                'perm_checkboxForSystem': k1,
                'perm_checkboxForAdmin': k2,
                'perm_checkboxForMember': k3,
                # 'emp_perm': perm_item.auth_code  # 0:none, 1:system, 2:admin, 3:member
            }
            _results.append(_obj)
    s.close()

    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list runinData all data(theta)
@listTable.route("/listRunInData", methods=['POST'])
def list_runin_data():
  print("listRunInData....")

  request_data = request.get_json()
  _id = (request_data['id'])

  _results = []
  return_value = True
  s = Session()

  #_objects = s.query(RunInData).filter(RunInData.spindleRunIn_id == _id).order_by(RunInData.spindleRunIn_speed_level.asc()).all()
  _objects = s.query(RunInData).filter(RunInData.spindleRunIn_id == _id).all()

  for data in _objects:
    _obj = {
      'id': str(data.id),
      'spindleRunIn_period': data.spindleRunIn_period ,         #時間
      'spindleRunIn_speed_level': data.spindleRunIn_speed_level ,    #段速
      'spindleRunIn_speed': data.spindleRunIn_speed ,          #轉速
      'spindleRunIn_stator_temp': data.spindleRunIn_stator_temp ,    #定子溫度
      'spindleRunIn_inner_frontBearing_temp': data.spindleRunIn_inner_frontBearing_temp ,   #內部前軸承溫度
      'spindleRunIn_inner_backBearing_temp': data.spindleRunIn_inner_backBearing_temp ,   #內部後軸承溫度
      'spindleRunIn_outer_frontBearing_temp': data.spindleRunIn_outer_frontBearing_temp ,  #外部前軸承溫度
      'spindleRunIn_outer_backBearing_temp': data.spindleRunIn_outer_backBearing_temp ,   #外部後軸承溫度
      'spindleRunIn_room_temp': data.spindleRunIn_room_temp ,          #室溫
      'spindleRunIn_coolWater_temp': data.spindleRunIn_coolWater_temp ,    #冷卻機水溫
      'spindleRunIn_Rphase_current': data.spindleRunIn_Rphase_current ,    #R相電流
      'spindleRunIn_Sphase_current': data.spindleRunIn_Sphase_current ,    #S相電流
      'spindleRunIn_Tphase_current': data.spindleRunIn_Tphase_current ,    #T相電流
      'spindleRunIn_cool_pipeline_flow': data.spindleRunIn_cool_pipeline_flow ,              #冷卻機管路流量
      'spindleRunIn_cool_pipeline_pressure': data.spindleRunIn_cool_pipeline_pressure ,          #冷卻機管路壓力
      'spindleRunIn_frontBearing_vibration_speed1': data.spindleRunIn_frontBearing_vibration_speed1 ,   #前軸承震動速度-1
      'spindleRunIn_frontBearing_vibration_acc1': data.spindleRunIn_frontBearing_vibration_acc1 ,     #前軸承震動加速度-1
      'spindleRunIn_frontBearing_vibration_disp1': data.spindleRunIn_frontBearing_vibration_disp1 ,    #前軸承震動位移-1
      'spindleRunIn_frontBearing_vibration_speed2': data.spindleRunIn_frontBearing_vibration_speed2 ,   #前軸承震動速度-2
      'spindleRunIn_frontBearing_vibration_acc2': data.spindleRunIn_frontBearing_vibration_acc2 ,     #前軸承震動加速度-2
      'spindleRunIn_frontBearing_vibration_disp2': data.spindleRunIn_frontBearing_vibration_disp2 ,    #前軸承震動位移-2
      'spindleRunIn_backBearing_vibration_speed1': data.spindleRunIn_backBearing_vibration_speed1 ,    #後軸承震動速度-1
      'spindleRunIn_backBearing_vibration_acc1': data.spindleRunIn_backBearing_vibration_acc1 ,      #後軸承震動加速度-1
      'spindleRunIn_backBearing_vibration_disp1': data.spindleRunIn_backBearing_vibration_disp1 ,     #後軸承震動位移-1
      'spindleRunIn_backBearing_vibration_speed2': data.spindleRunIn_backBearing_vibration_speed2 ,    #後軸承震動速度-2
      'spindleRunIn_backBearing_vibration_acc2': data.spindleRunIn_backBearing_vibration_acc2 ,      #後軸承震動加速度-2
      'spindleRunIn_backBearing_vibration_disp2': data.spindleRunIn_backBearing_vibration_disp2 ,     #後軸承震動位移-2
    }

    _results.append(_obj)

  s.close()
  print("_results:", len(_results))
  return jsonify({
    'status': return_value,
    'outputs': _results
  })


# list spindleRunin all data(theta)
@listTable.route("/listSpindleRunIns", methods=['GET'])
def list_spindle_runins():
  print("listSpindleRunIns....")

  _results = []
  return_value = True
  s = Session()

  _objects = s.query(SpindleRunIn).all()
  for spindle_runin in _objects:
    if (spindle_runin.isRemoved):
      target_spindle = s.query(Spindle).filter_by(id=spindle_runin.spindleRunIn_spindle_id).first()
      user = s.query(User).filter_by(id=spindle_runin.spindleRunIn_employer).first()
      k0 = ''
      if target_spindle.spindle_type == 1:
        k0 = '銑削/研磨主軸(自動換刀)'
      if target_spindle.spindle_type == 2:
        k0 = '研磨主軸(手動換刀)'
      if target_spindle.spindle_type == 3:
        k0 = '修砂主軸(手動換刀)'

      _obj = {}
      _obj = {
        'id': str(spindle_runin.id),
        'spindleRunIn_excel_file': spindle_runin.spindleRunIn_excel_file, #
        'spindleRunIn_customer': spindle_runin.spindleRunIn_customer,     #
        'spindleRunIn_spindle_type': k0,
        'spindleRunIn_spindle_cat': target_spindle.spindle_cat,
        'spindleRunIn_id': spindle_runin.spindleRunIn_work_id,            #
        'spindleRunIn_employer': user.emp_name,
        'spindleRunIn_employer_emp_id': user.emp_id,
        'spindleRunIn_date': spindle_runin.spindleRunIn_date,             #
      }

      _results.append(_obj)

  s.close()
  print("_results:", len(_results))
  return jsonify({
    'status': return_value,
    'outputs': _results
  })


# list grid all data(theta)
@listTable.route("/listGrids", methods=['GET'])
def list_grids():
  print("listGrids....")

  _results = []
  s = Session()

  _objects = s.query(Grid).all()
  ik=0
  print("total grids: ", len( _objects))
  for grid in _objects:
    if (grid.isRemoved):
      ik +=1
      print("grid", ik)
      s0 = ''
      if grid.station == 1:
        s0 = '待跑合A區'
      if grid.station == 2:
        s0 = '待校正B區'
      if grid.station == 3:
        s0 = '待測試C區'
      if grid.station == 4:
        s0 = '異常處理D區'

      #spindle_count = s.query(func.count(association_table.c.spindle_id)).filter_by(grid_id=grid.id).scalar()
      spindles = s.query(Spindle).join(association_table).filter(association_table.c.grid_id == grid.id).all()

      if not spindles:  #2024-03-30 add
        print("grid step1...")

        _obj = {}
        _obj = {
          'id': str(grid.id) + '_' + str(random.randint(1,100)),
          'station': s0,
          'layout': str(grid.layout),
          'max_size': grid.max_size,
          'type_and_cat': ''
        }
        _results.append(_obj)
      else:
        for spindle in spindles:
          print("grid step2...")

          k0 = ''
          if spindle.spindle_type == 1:
            k0 = '銑削/研磨主軸(自動換刀)'
          if spindle.spindle_type == 2:
            k0 = '研磨主軸(手動換刀)'
          if spindle.spindle_type == 3:
            k0 = '修砂主軸(手動換刀)'
          _obj = {}
          _obj = {
            'id': str(grid.id) + '_' + str(random.randint(1,100)),
            #'s_id': spindle.id,
            'station': s0,
            'layout': str(grid.layout),
            'max_size': grid.max_size,
            'type_and_cat': k0 + ' / ' + spindle.spindle_cat,
          }
          #print("id sp_id", grid.id, spindle.id, _obj)
          _results.append(_obj)

  s.close()
  print("_results:", len(_results))
  return jsonify({
      'status': 'success',
      'outputs': _results
  })


# list grid and spindle
@listTable.route("/listGridsAndSpindles", methods=['GET'])
def list_grids_and_spindles():
    print("listGridsAndSpindles....")

    s = Session()
    _results = []
    _objects = s.query(Grid).all()
    for grid in _objects:
        if (grid.isRemoved):
            s0 = ''
            if grid.station == 1:
              s0 = '待跑合A區'
            if grid.station == 2:
              s0 = '待校正B區'
            if grid.station == 3:
              s0 = '待測試C區'
            if grid.station == 4:
              s0 = '異常處理D區'

            _obj = {
                'id': grid.id,
                'station': s0,
                'layout': str(grid.layout),
                'total_size': grid.total_size,
                'max_size': grid.max_size,
                'type_and_cat': [],
            }

            if not grid._spindles:
              k0 = ''
              k1 = ''
            else:
              for spindle in grid._spindles:
                k1=spindle.spindle_cat
                k0 = ''
                if spindle.spindle_type == 1:
                  k0 = '銑削/研磨主軸(自動換刀)'
                if spindle.spindle_type == 2:
                  k0 = '研磨主軸(手動換刀)'
                if spindle.spindle_type == 3:
                  k0 = '修砂主軸(手動換刀)'


                _obj_TypeAndCat = {
                  'type': k0,
                  'cat': k1,
                }
                _obj['type_and_cat'].append(_obj_TypeAndCat)
                # print("supplier product: ", product.id)
              #end for loop
              _results.append(_obj)
              # print("supplier product: ", _results)

    temp_len = len(_results)
    print("儲位總數: ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list grid table all data for 入庫
@listTable.route("/listStockInGrids", methods=['GET'])
def list_stockin_grids():
  print("listStockInGrids....")

  return_value = True
  _results = []
  s = Session()

  grid_records = s.query(Grid).all()

  for grid in grid_records:
    _obj = {
      'id':grid.id,
      'spindleStockIn_station': grid.station,
      'spindleStockIn_layout': grid.layout,
      'spindleStockIn_total_size': grid.total_size,
      'aufnr': [],
      'spindles': [],
      'isSelect': False,
      'spindleStockIn_max_size': grid.max_size,
      #'selectPeriod': '',
    }
    associated_intags = grid._intags_g_i
    associated_spindles = grid._spindles
    len_intags = 0
    #len_spindles = 0
    if associated_intags:
      for intag in associated_intags:
        if intag.isRemoved:
          existing_spindle = s.query(Spindle).filter_by(id = intag.spindle_id, isRemoved = True).first()
          existing_user = s.query(User).filter_by(id = intag.user_id).first()
          #k1=spindle.spindle_cat
          k0 = ''
          if existing_spindle.spindle_type == 1:
            k0 = '銑削/研磨主軸(自動換刀)'
          if existing_spindle.spindle_type == 2:
            k0 = '研磨主軸(手動換刀)'
          if existing_spindle.spindle_type == 3:
            k0 = '修砂主軸(手動換刀)'
          _obj_for_aufnr = {}
          _obj_for_aufnr = {
            'spindleIn_workID': intag.work_id,
            'spindleStockIn_type': k0,
            'spindleStockIn_cat': existing_spindle.spindle_cat,
            'spindleStockIn_employer': existing_user.emp_id + ' ' + existing_user.emp_name,
            'spindleStockIn_date': intag.date,
            'spindleStockIn_period': intag.period,
            'last': 1,
          }
          _obj['aufnr'].append(_obj_for_aufnr)
          len_intags += 1
        #end if
      #end for loop
    #end if

    if associated_spindles:
      for spd in associated_spindles:
        '''
        k0 = ''
        if spd.spindle_type == 1:
          k0 = '銑削/研磨主軸(自動換刀)'
        if spd.spindle_type == 2:
          k0 = '研磨主軸(手動換刀)'
        if spd.spindle_type == 3:
          k0 = '修砂主軸(手動換刀)'
        _obj_for_spindles = {}
        '''
        _obj_for_spindles = {
          'id': spd.id,
          'type': str(spd.spindle_type),
          'cat': spd.spindle_cat,
          'isAll': spd.isAll,
        }
        _obj['spindles'].append(_obj_for_spindles)
        #len_spindles += 1
    #end if

    _obj['count'] = len_intags
    _results.append(_obj)
  #end for loop
  temp_len = len(_results)
  #print("intag總數: ", temp_len, _results)
  print("intag總數: ", temp_len)

  if (temp_len == 0):
      return_value = False

  s.close()
  return jsonify({
      'status': return_value,
      'outputs': _results
  })


'''
# list grid table all data for 入庫
@listTable.route("/listStockInGrids", methods=['GET'])
def list_stockin_grids():
    print("listStockInGrids....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()

    for grid in _objects:
        # if (grid.isRemoved):
        for reagent in grid._reagents_on_grid:
            _obj = {
                'grid_reagID': reagent.reag_id,
                'grid_reagName': reagent.reag_name,
                'grid_station': grid.station,
                'grid_layout': grid.layout,
                'grid_pos': grid.pos,
                'id': grid.id,
                'seg_id': grid.seg_id,
                'range0': grid.range0,
                'range1': grid.range1,
            }
            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })
'''

# list grid table all data for 入庫
@listTable.route("/listStockOutGrids", methods=['GET'])
def list_stockout_grids():
    print("listStockOutGrids....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()

    for grid in _objects:
        # if (grid.isRemoved):
        for reagent in grid._reagents_on_grid:
            _obj = {
                'grid_reagID': reagent.reag_id,
                'grid_reagName': reagent.reag_name,
                'grid_station': grid.station,
                'grid_layout': grid.layout,
                'grid_pos': grid.pos,
                'id': grid.id,
                'seg_id': grid.seg_id,
                'range0': grid.range0,
                'range1': grid.range1,
            }
            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })

@listTable.route("/listGridForCheck", methods=['POST'])
def list_grid_for_check():
    print("listGridForCheck....")

    request_data = request.get_json()

    _reag_id = request_data['reag_id']
    print("reeagent id: ", _reag_id)
    return_value = True

    s = Session()
    reag_item = s.query(Reagent).filter_by(reag_id=_reag_id).first()
    if reag_item:   # 2023-05-03 add
      if not reag_item.grid_id:
        return_value = False
    else:           # 2023-05-03 add
        return_value = False  # 2023-05-03 add

    print("reeagent grid: ", reag_item.grid_id, return_value)

    s.close()
    return jsonify({
        'status':  return_value,
    })

@listTable.route("/listGridForCheckByReagentName", methods=['POST'])
def list_grid_for_check_by_reagent_name():
    print("listGridForCheckByReagentName....")

    request_data = request.get_json()
    _reag_name = request_data['reag_name']
    print("reeagent name: ", _reag_name)

    _results = []
    return_value = True
    s = Session()

    if _reag_name is not None:  # 2023-05-03 add
      _objects = s.query(Reagent).filter(Reagent.reag_name.ilike("%" + _reag_name + "%")).all()
      #reag_item = [u.__dict__ for u in _objects]
      for reag_item in _objects:
        print(reag_item.reag_name)
        _results.append(reag_item.reag_name)

    s.close()
    return jsonify({
        'status':  return_value,
         'outputs': _results
    })


# list inStock table all data
@listTable.route("/listStockInData", methods=['GET'])
def list_stockin_data():
    print("listStockInData....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag in _objects:
        if (intag.isRemoved and (not intag.isPrinted) and (not intag.isStockin)):
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_cnt': intag.count,
                'stockInTag_cnt_max': intag.count,
                'stockInTag_alpha': intag.stockIn_alpha,
                'stockInTag_isPrinted': intag.isPrinted,
                'stockInTag_isStockin': intag.isStockin,
            }

            _results.append(_obj)

    temp_len = len(_results)
    print("listStockInData, total(待入庫資料總數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockInLastAlpha", methods=['GET'])
def list_stockin_last_alpha():
    print("listStockInLastAlpha....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).order_by(InTag.stockIn_alpha.desc()).all()
    '''
    for intag in _objects:
        if (intag.isRemoved and intag.isPrinted and (not intag.isStockin)):  # 資料存在, 而且已經貼標籤,
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_cnt': intag.count,

                'active': False,
            }

            _results.append(_obj)
    '''
    s.close()

    temp_len = len(_results)
    print("listStockInLastAlpha, input total(準備列印標籤入庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockInItems", methods=['GET'])
def list_stockin_items():
    print("listStockInItems....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).all()

    for intag in _objects:
        if (intag.isRemoved and intag.isPrinted and (not intag.isStockin)):  # 資料存在, 而且已經貼標籤,
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_unit':reagent.reag_In_unit, # add
                'stockInTag_cnt': intag.count,

                'active': False,
            }

            _results.append(_obj)

    s.close()

    temp_len = len(_results)
    print("listStockInItems, input total(準備列印標籤入庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockOutItems", methods=['GET'])
def list_stockout_items():
    print("listStockOutItems....")
    s = Session()
    _results = []
    return_value = True  # true: 資料正確
    _objects = s.query(OutTag).all()

    for outtag in _objects:
        if (outtag.isRemoved and outtag.isPrinted and (not outtag.isStockout)):  # 資料存在, 而且已經貼標籤
            user = s.query(User).filter_by(id=outtag.user_id).first()

            in_tag = s.query(InTag).filter_by(id=outtag.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': outtag.id,
                'stockOutTag_reagID': reagent.reag_id,
                'stockOutTag_reagName': reagent.reag_name,
                'stockOutTag_reagPeriod': in_tag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_reagTemp': k1,
                'stockOutTag_Date': outtag.outtag_date,  # 出庫日期
                'stockOutTag_EmpID': user.emp_id,
                'stockOutTag_Employer': user.emp_name,
                'stockOutTag_batch': in_tag.batch,
                'stockOutTag_cnt': outtag.count,
                'stockOutTag_unit':reagent.reag_Out_unit,   # add
                #'stockOutTag_unit':reagent.reag_In_unit,   # add
                'stockOutTag_scale':reagent.reag_scale,

                'active': False,
            }

            _results.append(_obj)
    s.close()

    temp_len = len(_results)
    print("listStockOutItems, output total(準備列印標籤出庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list outStock_tagPrint table all data
@listTable.route("/liststockOutTagPrintData", methods=['GET'])
def list_stockout_tag_print_data():
    print("liststockOutTagPrintData....")
    s = Session()
    _results = []
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag_print in _objects:
        if (outtag_print.isRemoved and (not outtag_print.isPrinted) and (not outtag_print.isStockout)):  # 在庫, 還沒列印標籤, 還沒出庫
            user = s.query(User).filter_by(id=outtag_print.user_id).first()

            in_tag = s.query(InTag).filter_by(
                id=outtag_print.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': outtag_print.id,
                'stockOutTag_InID': outtag_print.intag_id,
                'stockOutTag_reagID': reagent.reag_id,
                'stockOutTag_reagName': reagent.reag_name,
                'stockOutTag_reagPeriod': in_tag.reag_period,         # 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_reagTemp': k1,
                'stockOutTag_In_Date': in_tag.intag_date,             # 入庫日期
                'stockOutTag_Out_Date': outtag_print.outtag_date,     # 出庫日期(領用日期)
                'stockOutTag_Employer': user.emp_name,

                'stockOutTag_batch': in_tag.batch,
                #'stockOutTag_unit': outtag_print.unit,     # 2023-01-13 mark
                'stockOutTag_unit': reagent.reag_Out_unit,  # 2023-01-13 add
                'stockOutTag_cnt': outtag_print.count,
                'stockOutTag_cnt_max': in_tag.count * reagent.reag_scale,        # 2023-08-09 add

                #'stockOutTag_cnt': in_tag.count * reagent.reag_scale, #在庫數 * 比例
                'stockOutTag_alpha': outtag_print.stockOut_alpha,
                # 'stockOutTag_cnt': outtag_print.count - outtag_print.stockOut_temp_count,
                'stockOutTag_isPrinted': outtag_print.isPrinted,
                'stockOutTag_isStockin': outtag_print.isStockout,
                'stockInTag_rePrint': '出庫'
            }

            tempAlpha=in_tag.stockIn_alpha.lower()
            _obj['stockOutTag_alpha']=tempAlpha    # 字母, 2023-07-14 add
            #print("_obj: ", _obj)

            _results.append(_obj)

    s.close()
    #print("_results: ", _results)
    #newlist = sorted(_results, key=itemgetter('stockOutTag_reagID'))   # 2023-08-25 add

    return jsonify({
        'status': 'success',
        'outputs': _results
        #'outputs': newlist    # 2023-08-25 modify
    })


# list outStock_tagPrint table all data
@listTable.route("/liststockOutTagPrintForSame", methods=['GET'])
def list_stockout_tag_print_for_same():
    print("liststockOutTagPrintForSame....")
    s = Session()
    _results = []
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag_print in _objects:
        if (outtag_print.isRemoved and (not outtag_print.isPrinted) and (not outtag_print.isStockout)):  # 在庫, 還沒列印標籤, 還沒出庫
            user = s.query(User).filter_by(id=outtag_print.user_id).first()

            in_tag = s.query(InTag).filter_by(
                id=outtag_print.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': outtag_print.id,
                'stockOutTag_InID': outtag_print.intag_id,
                'stockOutTag_reagID': reagent.reag_id,
                'stockOutTag_reagName': reagent.reag_name,
                'stockOutTag_reagPeriod': in_tag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_reagTemp': k1,
                'stockOutTag_In_Date': in_tag.intag_date,  # 入庫日期
                'stockOutTag_Out_Date': outtag_print.outtag_date,  # 出庫日期(領用日期)
                'stockOutTag_Employer': user.emp_name,
                'stockOutTag_batch': in_tag.batch,
                #'stockOutTag_unit': outtag_print.unit,     # 2023-01-13 mark
                'stockOutTag_unit': reagent.reag_Out_unit,  # 2023-01-13 add
                'stockOutTag_cnt': outtag_print.count,
                #'stockOutTag_cnt': in_tag.count * reagent.reag_scale, #在庫數 * 比例
                'stockOutTag_alpha': outtag_print.stockOut_alpha,
                # 'stockOutTag_cnt': outtag_print.count - outtag_print.stockOut_temp_count,
                'stockOutTag_isPrinted': outtag_print.isPrinted,
                'stockOutTag_isStockin': outtag_print.isStockout,
            }

            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list inStock_tagPrint table all data
@listTable.route("/listRePrintTagData", methods=['GET'])
def list_reprint_tag_data():
    print("listRePrintTagData....")
    s = Session()
    _results = []
    # 入庫標籤資料
    _objects = s.query(InTag).all()
    for intag_print in _objects:
        #if (intag_print.isRemoved and intag_print.isPrinted):
        #if (intag_print.isPrinted):
        if (intag_print.isRemoved and (not intag_print.isPrinted) and intag_print.isStockin):    # 2023-07-20 modify
            user = s.query(User).filter_by(id=intag_print.user_id).first()
            reagent = s.query(Reagent).filter_by(
                id=intag_print.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag_print.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_rePrint': '入庫',
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag_print.intag_date,  # 入庫日期
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag_print.batch,
                #'stockInTag_cnt': intag_print.count,
                'stockInTag_cnt': 1,
                'stockInTag_alpha': intag_print.stockIn_alpha,
                # 'stockInTag_cnt': intag_print.count - intag_print.stockOut_temp_count,
                'stockInTag_isPrinted': intag_print.isPrinted,
                'stockInTag_isStockin': intag_print.isStockin,
                'isIn': True,
            }

            _results.append(_obj)
    # 出庫標籤資料
    _objects = s.query(OutTag).all()
    for intag_print in _objects:
        #if (intag_print.isRemoved and intag_print.isPrinted):
        #if (intag_print.isPrinted):                                                            #
        if (intag_print.isRemoved and (not intag_print.isPrinted) and intag_print.isStockout):  # 2023-08-09 modify
            user = s.query(User).filter_by(id=intag_print.user_id).first()
            in_tag = s.query(InTag).filter_by(id=intag_print.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag_print.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_rePrint': '出庫',
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag_print.outtag_date,  # 入庫日期
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': in_tag.batch,
                #'stockInTag_cnt': intag_print.count,
                'stockInTag_cnt': 1,
                #'stockInTag_alpha': intag_print.stockOut_alpha,  # 2023-08-07 modify
                'stockInTag_alpha': in_tag.stockIn_alpha.lower(),         # 2023-08-08 modify
                # 'stockInTag_cnt': intag_print.count - intag_print.stockOut_temp_count,
                'stockInTag_isPrinted': intag_print.isPrinted,
                'stockInTag_isStockin': intag_print.isStockout,
                'isIn': False,
            }

            _results.append(_obj)


    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list inStock_tagPrint table all data
@listTable.route("/listStockInTagPrintData", methods=['GET'])
def list_stockin_tag_print_data():
    print("listStockInTagPrintData....")
    s = Session()
    _results = []
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag_print in _objects:
        if (intag_print.isRemoved and (not intag_print.isPrinted) and (not intag_print.isStockin)):
            user = s.query(User).filter_by(id=intag_print.user_id).first()
            reagent = s.query(Reagent).filter_by(
                id=intag_print.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag_print.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag_print.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag_print.intag_date,  # 入庫日期
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag_print.batch,
                'stockInTag_cnt': intag_print.count,
                'stockInTag_alpha': intag_print.stockIn_alpha,
                # 'stockInTag_cnt': intag_print.count - intag_print.stockOut_temp_count,
                'stockInTag_isPrinted': intag_print.isPrinted,
                'stockInTag_isStockin': intag_print.isStockin,
                'stockInTag_rePrint': '入庫'
            }

            _results.append(_obj)

    s.close()

    #newlist = sorted(_results, key=itemgetter('stockInTag_reagID'))   # 2023-08-25 add

    return jsonify({
        'status': 'success',
        'outputs': _results
        #'outputs': newlist # 2023-08-25 modify
    })

'''
# list inStock_tagPrint all data count
@listTable.route("/listStockInTagPrintCount", methods=['GET'])
def list_stockin_tag_print_count():
    print("listStockInTagPrintCount....")
    s = Session()

    temp_count = 0
    return_value = True
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag_print in _objects:
        if (intag_print.isRemoved and intag_print.isPrinted and (not intag_print.isStockin)):
            temp_count = temp_count + 1
            print("id: ", intag_print.id)

    s.close()

    print("listStockInTagPrintCount, total(入庫試劑總數): ", temp_count)
    if (temp_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': temp_count,
    })
'''

# list outStock_tagPrint all data count
@listTable.route("/listStockOutTagPrintCount", methods=['GET'])
def list_stockout_tag_print_count():
    print("listStockOutTagPrintCount....")
    s = Session()

    temp_count = 0
    return_value = True
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag_print in _objects:
        if (outtag_print.isRemoved and outtag_print.isPrinted and (not outtag_print.isStockout)):
            temp_count = temp_count + 1
            print("id: ", outtag_print.id)

    s.close()

    print("listStockOutTagPrintCount, total(待領料試劑總數): ", temp_count)
    if (temp_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': temp_count,
    })


# list outStock table all data
@listTable.route("/listStockOutData", methods=['GET'])
def list_stockout_data():
    print("listStockOutData....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag in _objects:
        if (outtag.isRemoved and (not outtag.isPrinted) and (not outtag.isStockout)):
            _inTag = s.query(InTag).filter_by(id=outtag.intag_id).first()
            user = s.query(User).filter_by(id=outtag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=_inTag.reagent_id).first()
            supplier = s.query(Supplier).filter_by(id=reagent.super_id).first()

            _obj = {
                'stockOutTag_reagID': reagent.reag_id,                # 資材碼
                'stockOutTag_reagName': reagent.reag_name,            # 品名

                'stockOutTag_alpha': _inTag.stockIn_alpha.lower(),    # 字母, 2023-07-14 add

                'stockOutTag_batch': _inTag.batch,              # 入庫批號, 2023-02-10 add
                'stockOutTag_supplier': supplier.super_name,    # 供應商
                'stockOutTag_reagPeriod': _inTag.reag_period,   # 效期, 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_InDate': _inTag.intag_date,        # 入庫日期
                'stockOutTag_Date': outtag.outtag_date,         # 領用日期
                'stockOutTag_EmpID': user.emp_id,
                'stockOutTag_Employer': user.emp_name,
                #'stockOutTag_cnt': outtag.count,
                #'stockOutTag_cnt': _inTag.count * reagent.reag_scale,
                #'stockOutTag_cnt': _inTag.count,
                #'stockOutTag_cnt_max': outtag.count,   #
                'stockOutTag_cnt_max': _inTag.count * reagent.reag_scale,    # 2023-08-09 modify
                'stockOutTag_cnt': outtag.count,
                'stockOutTag_scale': reagent.reag_scale,
                #'stockOutTag_unit': outtag.unit,             # 2023-01-13 mark
                'stockOutTag_unit': reagent.reag_Out_unit,    # 2023-01-13 add
                #'stockOutTag_unit':  reagent.reag_In_unit,   # 在庫單位,reag_In_unit
                'stockOutTag_InID': _inTag.id,
                'stockOutTag_ID': outtag.id,
                'stockOutTag_isPrinted': outtag.isPrinted,
                'stockOutTag_isStockin': outtag.isStockout,
            }

            _results.append(_obj)

    temp_len = len(_results)
    print("listStockOutData, total(待出庫資料總數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list Stock records(StockIn) all data
@listTable.route("/listStockRecords", methods=['GET'])
def list_stock_records():
  print("listStockRecords....")

  return_value = True
  _results = []

  s = Session()

  grid_records = s.query(Grid).all()

  for grid in grid_records:
    s0 = ''
    if grid.station == 1:
      s0 = '待跑合A區'
    if grid.station == 2:
      s0 = '待校正B區'
    if grid.station == 3:
      s0 = '待測試C區'
    if grid.station == 4:
      s0 = '異常處理D區'

    _obj = {
      #'id':grid.id,
      'spindleStockIn_st_lay': s0 + ' 第' + str(grid.layout) + '層',
      #'spindleStockIn_station': grid.station,
      #'spindleStockIn_layout': grid.layout,
      'aufnr': [],
      'spindles': [],
      'isSelect': False,
    }
    associated_intags = grid._intags_g_i
    associated_spindles = grid._spindles

    len_intags = 0

    if associated_intags:
      for intag in associated_intags:
          existing_spindle = s.query(Spindle).filter_by(id = intag.spindle_id, isRemoved = True).first()
          existing_user = s.query(User).filter_by(id = intag.user_id).first()
          k0 = ''
          if existing_spindle.spindle_type == 1:
            k0 = '銑削/研磨主軸(自動換刀)'
          if existing_spindle.spindle_type == 2:
            k0 = '研磨主軸(手動換刀)'
          if existing_spindle.spindle_type == 3:
            k0 = '修砂主軸(手動換刀)'

          out_empName = ''
          out_date = ''
          if (intag.isRemoved==False):
            outtag=intag._outstocks

            outtag_user = s.query(User).filter_by(id = outtag[0].user_id).first()
            out_empName = outtag_user.emp_name  #
            out_date = outtag[0].date              #

          _obj_for_aufnr = {}
          _obj_for_aufnr = {
            'spindleIn_workID': intag.work_id,
            'spindleStockIn_type_cat': k0 + ' / ' + existing_spindle.spindle_cat,
            #'spindleStockIn_type': k0,
            #'spindleStockIn_cat': existing_spindle.spindle_cat,
            'spindleStockIn_employer': existing_user.emp_name,
            'spindleStockIn_date': intag.date,
            'spindleStockOut_employer': out_empName,
            'spindleStockOut_date': out_date,
            'spindleStockIn_period': intag.period,
            'comment':intag.comment,
            'date_comment': intag.date_comment,                     # 在庫備註說明的日期
            'user_comment': intag.user_comment,                     # 在庫備註說明的員工
            'intag_id': intag.id,
            #'last': 1,
          }
          _obj['aufnr'].append(_obj_for_aufnr)
          #len_intags += 1
        #end if
      #end for loop
    #end if
    '''
    if associated_spindles:
      for spd in associated_spindles:

        k0 = ''
        if spd.spindle_type == 1:
          k0 = '銑削/研磨主軸(自動換刀)'
        if spd.spindle_type == 2:
          k0 = '研磨主軸(手動換刀)'
        if spd.spindle_type == 3:
          k0 = '修砂主軸(手動換刀)'
        _obj_for_spindles = {}

        _obj_for_spindles = {
          'id': spd.id,
          'type': k0,
          'cat': spd.spindle_cat,
          'isAll': spd.isAll,
        }
        _obj['spindles'].append(_obj_for_spindles)

        #len_spindles += 1
    #end if
    '''

    #_obj['count'] = len_intags
    _results.append(_obj)
  #end for loop
  temp_len = len(_results)
  #print("intag總數: ", temp_len, _results)
  print("stock record總數: ", temp_len)

  if (temp_len == 0):
    return_value = False

  s.close()
  return jsonify({
    'status': return_value,
    'outputs': _results
  })


# list inventory records all data
@listTable.route("/listInventorys", methods=['GET'])
def list_inventorys():
    print("listInventorys....")
    s = Session()
    temp_kk = 1  # 紀錄筆數id, 起始值=1
    _results = []
    _objects = s.query(InTag).all()
    # intags = [u.__dict__ for u in _objects]
    for intag in _objects:
        # if (intag.isRemoved and intag.isPrinted and intag.isStockin):
        #if (intag.isRemoved and intag.isStockin): # 在庫 且 已入庫    , 2023-06-12 modify
        if (intag.isRemoved and intag.isStockin and intag.count > 0): # 在庫 且 已入庫, 2023-06-15 modify
            _user = s.query(User).filter_by(id=intag.user_id).first()
            _reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()
            # _supplier = s.query(Supplier).filter_by(id=_reagent.super_id).first()
            #_grid = s.query(Grid).filter_by(id=intag.grid_id).first()    # 2023-01-13 mark
            _grid = s.query(Grid).filter_by(id=_reagent.grid_id).first()  # 2023-01-13 add

            _product = s.query(Product).filter_by(id=_reagent.product_id).first() # 2023-05-23 add
            print("_product.name: ", _product.name)
            k1 = ''
            if _reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if _reagent.reag_temp == 1:
                k1 = '2~8度C'
            if _reagent.reag_temp == 2:
                k1 = '-20度C'

            # 2023-06-15 modify
            #modify_cnt_str=str(intag.count_inv_modify)
            #modify_comment=intag.comment
            #if intag.count_inv_modify==0.0:
            #  modify_cnt_str=''
            #  modify_comment=''
            modify_cnt_str=''
            modify_comment=''

            _obj = {
                #'id': temp_kk,     # 2023-0612 modify
                'id': intag.id,     #
                'stockInTag_reagID': _reagent.reag_id,          # 資材碼
                'stockInTag_reagName': _reagent.reag_name,      # 品名
                'stockInTag_reagProduct': _product.name,        # 2023-05-23 add, 資材類別
                'stockInTag_stockInBatch': intag.batch,         #批次, # 2023-0216 add
                'stockInTag_reagPeriod': intag.reag_period,     # 效期, 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,    # 保存溫度
                'stockInTag_Date': intag.intag_date,    # 入庫日期
                'stockInTag_Employer': _user.emp_name,  # 入庫人員
                'stockInTag_grid': _grid.station + '站' + _grid.layout + '層' + _grid.pos + '格',
                #'stockInTag_grid_id': _grid.id,      # 2023-01-13 mark
                'stockInTag_grid_id': _reagent.grid_id,   # 2023-01-13 add
                'stockInTag_grid_station': _grid.station,
                'stockInTag_grid_layout': _grid.layout,
                'stockInTag_grid_pos': _grid.pos,
                # 在庫數量
                # 'stockInTag_cnt': str(intag.count) + _reagent.reag_In_unit,
                'stockInTag_cnt': str(intag.count) + _reagent.reag_In_unit,
                'stockInTag_cnt_inv_mdf': modify_cnt_str,
                'stockInTag_comment': modify_comment,
                'intag_id': intag.id,
            }

            _results.append(_obj)
            temp_kk += 1

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })
