from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database.tables import User, Permission, Setting, Spindle, InTag, OutTag, Session
from sqlalchemy import and_, or_, not_

from flask_cors import CORS

from operator import itemgetter   # 2023-08-25  add

getTable = Blueprint('getTable', __name__)


# ------------------------------------------------------------------

# list user, department, permission and setting table all data
@getTable.route('/login', methods=['POST'])
def login():
    print("login....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    password = (request_data['password'] or '')
    # remember = True if request_data['remember'] else False

    s = Session()
    user = s.query(User).filter_by(emp_id=userID).first()

    return_value = True  # true: 資料正確
    if not user:
        return_value = False
        _user_object = {}
    else:
        print("login user: ", user)

        xx = not user.isRemoved  # isRemoved=False, 表示該使用者已被註記移除

        if not user or not check_password_hash(user.password, password) or xx:
            return_value = False  # if the user doesn't exist or password is wrong, reload the page
            _user_object = {}
        else:
            # if the above check passes, then we know the user has the right credentials
            # return_value = True

            #dep_item = s.query(Department).filter_by(id=user.dep_id).first()
            perm_item = s.query(Permission).filter_by(
                id=user.perm_id).first()
            setting_item = s.query(Setting).filter_by(
                id=user.setting_id).first()

            s.query(User).filter(User.emp_id ==
                                 userID).update({'isOnline': True})
            s.commit()

            _user_object = {
                'empID': user.emp_id,
                'name': user.emp_name,
                #'dep': dep_item.dep_name,
                #'dep_id': dep_item.id,
                'perm_name': perm_item.auth_name,
                'perm': perm_item.auth_code,
                'password': password,
                'setting_items_per_page': setting_item.items_per_page,
                'setting_message': setting_item.message,
            }

    s.close()

    return jsonify({
        'status': return_value,
        'user': _user_object
    })
