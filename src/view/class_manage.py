#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import time
###########################################
from qoj_global import check_user, check_admin, check_class_admin
from class_manage_con import *

BP = Blueprint('class_manage', __name__)

#분반 정보 반환
@BP.route('/API/V1/class_manage/get_classinfo', methods=['POST'])
@jwt_required
def API_V1_auth__get_classinfo():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    if check_user(g.db, get_jwt_identity()):
        result = get_classinfo(g.db, CLASS_ID)
        try:
            result = get_classinfo(g.db, CLASS_ID)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

@BP.route('/API/V1/class_manage/get_class')
@jwt_required
def API_V1_auth__get_class():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_class(g.db, get_jwt_identity())
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#관리자 분반 반환
@BP.route('/API/V1/class_manage/get_admin_class')
@jwt_required
def API_V1_auth__get_admin_class():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_admin_class(g.db, get_jwt_identity())
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#모든 분반 조회
@BP.route('/API/V1/class_manage/get_all_class')
@jwt_required
def API_V1_auth__get_all_class():
    process_time = time.time()
    if check_admin(g.db, get_jwt_identity()):
        try:
            result = get_all_class(g.db)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#분반 생성
@BP.route('/API/V1/class_manage/create_class', methods=['POST'])
@jwt_required
def API_V1_auth__create_class():
    process_time = time.time()
    CLASS_NAME = request.get_json()['class_name']
    CLASS_ADMIN = request.get_json()['class_admin']
    CLASS_SUB_ADMIN = request.get_json()['class_sub_admin']
    if check_admin(g.db, get_jwt_identity()):    
        try:
            result = create_class(g.db, CLASS_NAME, CLASS_ADMIN, CLASS_SUB_ADMIN)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#분반 수정
@BP.route('/API/V1/class_manage/update_class', methods=['POST'])
@jwt_required
def API_V1_auth__update_class():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    CLASS_NAME = request.get_json()['class_name']
    CLASS_ADMIN = request.get_json()['class_admin']
    CLASS_SUB_ADMIN = request.get_json()['class_sub_admin']
    if check_admin(g.db, get_jwt_identity()):    
        result = update_class(g.db, CLASS_ID, CLASS_NAME, CLASS_ADMIN, CLASS_SUB_ADMIN)
        try:
            result = update_class(g.db, CLASS_ID, CLASS_NAME, CLASS_ADMIN, CLASS_SUB_ADMIN)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#분반 삭제
@BP.route('/API/V1/class_manage/delete_class', methods=['POST'])
@jwt_required
def API_V1_auth__delete_class():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    if check_admin(g.db, get_jwt_identity()):
        try:
            result = delete_class(g.db, CLASS_ID)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#분반 소속 회원 반환
@BP.route('/API/V1/class_manage/get_class_member', methods=['POST'])
@jwt_required
def API_V1_auth__get_class_member():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    if check_admin(g.db, get_jwt_identity()) or check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = get_class_member(g.db, CLASS_ID)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#분반 회원 추가
@BP.route('/API/V1/class_manage/push_user', methods=['POST'])
@jwt_required
def API_V1_auth__push_user():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    USER_LIST = request.get_json()['user_list']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = push_user(g.db, CLASS_ID, USER_LIST)
            status = "success"
        except:
            result = status = "fail"
    else:
        status = "success"
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )