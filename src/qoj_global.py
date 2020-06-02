import sys
#Path initiat#################################################
basic_path = [
    './',
    '../',
    '../../',
]

envirement_path = [
    'controller',
    'models',
    'module',
    'templates',
    'view'
]

for path in basic_path:
    sys.path.insert(0, path)

for path in basic_path:
    for env_path in envirement_path:
        sys.path.insert(0, path + env_path)
##############################################################
from qoj_model import *

#회원 확인
def check_user(db, JWT):
    USER = QOJ__user(db).find__one(user_id = JWT)

    if USER:
        return True
    else:
        return False

#관리자 확인
def check_admin(db, JWT):
    ADMIN = QOJ__user(db).find__one(user_id = JWT)

    if ADMIN and ADMIN['user_id'] == "QOJ_ADMIN":
        return True
    else:
        return False

#분반 관리자 확인
def check_class_admin(db, class_id, JWT):
    USER = QOJ__user(db).find__one(user_id = JWT)

    if not USER:
        return False

    result = QOJ__user_class(db).find__user_class_id(JWT, class_id)

    if result:
        if result['uc_type'] == 1:
            return True
        else:
            return False
    else:
        return False
