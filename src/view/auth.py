#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import time
###########################################
from qoj_global import check_user, check_admin
from auth_con import *

BP = Blueprint('auth', __name__)

#회원가입
@BP.route('/API/V1/auth/sign_up', methods = ['POST'])
def API_V1_auth__sign_up():
    ID = request.get_json()['id']
    PW = request.get_json()['pw']
    NAME = request.get_json()['name']
    EMAIL = request.get_json()['email']
    process_time = time.time()
    try:
        result = sign_up(g.db, ID, PW, NAME, EMAIL)
        status = "success"
    except:
        result = status = "fail"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#로그인
@BP.route('/API/V1/auth/sign_in', methods = ['POST'])
def API_V1_auth__sign_in():
    ID = request.get_json()['id']
    PW = request.get_json()['pw']
    process_time = time.time()
    try:
        result = sign_in(g.db, ID, PW)
        status = "success"
    except:
        result = status = "fail"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#회원정보 변경
@BP.route('/API/V1/auth/update', methods = ['POST'])
@jwt_required
def API_V1_auth__update():
    process_time = time.time()
    PW = request.get_json()['pw']
    CEHCK_PW = request.get_json()['check_pw']
    EMAIL = request.get_json()['email']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = user_update(g.db, get_jwt_identity(), PW, CEHCK_PW, EMAIL)
            status = "success"
        except:
            result = status = "fail"
    else:
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#회원 정보 반환
@BP.route('/API/V1/auth/get_userinfo')
@jwt_required
def API_V1_auth__get_userinfo():
    process_time = time.time()
    try:
        result = get_userinfo(g.db, get_jwt_identity())
        status = "success"
    except:
        result = status = "fail"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )

#모든 회원 정보 반환
@BP.route('/API/V1/auth/get_all_user')
@jwt_required
def API_V1_auth__get_all_user():
    process_time = time.time()
    if check_admin(g.db, get_jwt_identity()):
        try:
            result = get_all_user(g.db)
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

#회원 탈퇴
@BP.route('/API/V1/auth/withdrawal')
@jwt_required
def API_V1_auth__withdrawal():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        try:
            result = withdrawal(g.db, get_jwt_identity())
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

#어드민 확인
@BP.route('/API/V1/auth/check_admin')
@jwt_required
def API_V1_auth__check_admin():
    process_time = time.time()
    status = "success"
    if check_admin(g.db, get_jwt_identity()):
        result = True
    else:
        result = False
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )
