#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import time
###########################################
from qoj_global import check_admin
from auth_con import *

BP = Blueprint('auth', __name__)

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

@BP.route('/API/V1/auth/level_up')
@jwt_required
def API_V1_auth__level_up_admin():
    process_time = time.time()
    if check_admin(g.db, get_jwt_identity()):
        TARGET_ID = request.get_json()['target_id']
        TARGET_LEVEL = request.get_json()['target_level']
        try:
            result = get_law_1(g.db, law_name)
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
