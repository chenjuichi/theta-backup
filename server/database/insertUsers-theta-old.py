from tables import User, Setting, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash

# --------------------------

s = Session()
# user 1
emp_id = "1234"
emp_name = "陳瑞琪"
password = "a1234"
new_user = User(emp_id=emp_id, emp_name=emp_name, password=generate_password_hash(password, method='scrypt'))
s.add(new_user)

# user 2
emp_id = "0058"
emp_name = "魏徵佑"
password = "a0058"
new_user = User(emp_id=emp_id, emp_name=emp_name, password=generate_password_hash(password, method='scrypt'))
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

# append department and permission data into user table
#department = [6, 6]
#permission = [2, 2]  # BY permission table id

user_objects = s.query(User).all()
users = [u.__dict__ for u in user_objects]
i = 1
for user in users:
    s.query(User).filter(User.id == i).update(
        {"perm_id": 2})
    i = i+1

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

# create setting table data
obj_list = []
settings = [{'message': 'hello1'},  # 1
            {'message': 'hello2'},  # 2
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

# append setting data into user table
setting_objects = s.query(Setting).all()
new_settings = [u.__dict__ for u in setting_objects]

user_objects = s.query(User).all()
users = [u.__dict__ for u in user_objects]
i = 0
for user in users:
    s.query(User).filter(User.id == i+1).update(
        {"setting_id": new_settings[i]['id']})
    i = i+1

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

print("insert 2 user data is ok...")
