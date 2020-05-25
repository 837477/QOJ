#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import time
###########################################
from qoj_global import check_user
from problem_manage_con import *

BP = Blueprint('problem_manage', __name__)

#problem_group + class
@BP.route('/API/V1/problem_manage/get_problem_group1', methods = ['POST'])
@jwt_required
def API_V1_auth__get_problem_group1():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        class_id = request.get_json()['class_id']
        try:
            result = get_problem_group1(g.db, class_id)
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

#problem_group + class
@BP.route('/API/V1/problem_manage/get_problem_group2', methods = ['POST'])
@jwt_required
def API_V1_auth__get_problem_group2():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        pg_id = request.get_json()['pg_id']
        try:
            result = get_problem_group2(g.db, pg_id)
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

#problem_list
@BP.route('/API/V1/problem_manage/get_problem_list', methods = ['POST'])
@jwt_required
def API_V1_auth__get_problem_list():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        pg_id = request.get_json()['pg_id']
        try:
            result = get_problem_list(g.db, get_jwt_identity(), pg_id)
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


#problem
@BP.route('/API/V1/problem_manage/get_problem', methods = ['POST'])
@jwt_required
def API_V1_auth__get_problem():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        p_id = request.get_json()['p_id']
        try:
            result = get_problem(g.db, get_jwt_identity(), p_id)
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