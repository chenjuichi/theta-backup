from tables import User, Setting, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash


# --------------------------


s = Session()

# create setting table data
obj_list = []
settings = [{'items_per_page': 5, 'message': 'hello1'},
            {'items_per_page': 10, 'message': 'hello2'},
            {'message': 'hello3'}, {'message': 'hello4'},
            {'message': 'hello5'}, {'message': 'hello6'},
            {'message': 'hello7'}, {'message': 'hello8'},
           ]

for record in settings:
    user_setting = Setting(**record)
    obj_list.append(user_setting)

s.add_all(obj_list)
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()


# --------------------------


# insert 3 users
s = Session()
# user 1
emp_id = "1234"
emp_name = "陳瑞琪"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=2, setting_id=1,
                #password=generate_password_hash(password, method='sha256'))
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 2
emp_id = "0058"
emp_name = "魏徵佑"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=2, setting_id=2,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 3
emp_id = "0008"
emp_name = "廖家祥"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=2, setting_id=3,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 4
emp_id = "0009"
emp_name = "蔡孟辰"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=2, setting_id=3,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 5
emp_id = "0064"
emp_name = "賴彥勳"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=3, setting_id=3,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 6
emp_id = "0046"
emp_name = "洪宇良"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=3, setting_id=3,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)


# user 7
emp_id = "0059"
emp_name = "吳發財"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, perm_id=4, setting_id=4,
                password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

s.close()

print("insert 7 user data is ok...")

