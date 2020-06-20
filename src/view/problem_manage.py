#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import sqlparse
import time
###########################################
from qoj_global import check_user, check_admin, check_class_admin
from problem_manage_con import *

BP = Blueprint('problem_manage', __name__)

#problem_group + class
@BP.route('/API/V1/problem_manage/get_problem_group1', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_problem_group1():
    process_time = time.time()
    class_id = request.get_json()['class_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_problem_group1(g.db, class_id)
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

#problem_group + class
@BP.route('/API/V1/problem_manage/get_problem_group2', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_problem_group2():
    process_time = time.time()
    pg_id = request.get_json()['pg_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_problem_group2(g.db, pg_id)
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

#problem_list
@BP.route('/API/V1/problem_manage/get_problem_list', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_problem_list():
    process_time = time.time()
    pg_id = request.get_json()['pg_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_problem_list(g.db, get_jwt_identity(), pg_id)
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

#특정 문제에 대한 반환
@BP.route('/API/V1/problem_manage/get_problem', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_problem():
    process_time = time.time()
    p_id = request.get_json()['p_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_problem(g.db, get_jwt_identity(), p_id)
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

#문제집 추가
@BP.route('/API/V1/problem_manage/create_problem_group', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__create_problem_group():
    process_time = time.time()
    class_id = request.get_json()['class_id']
    pg_title = request.get_json()['pg_title']
    if check_class_admin(g.db, class_id, get_jwt_identity()):
        try:
            result = create_problem_group(g.db, class_id, pg_title)
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

#문제집 수정 $$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/update_problem_group', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__update_problem_group():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    pg_id = request.get_json()['pg_id']
    pg_title = request.get_json()['pg_title']
    pg_exam_start = request.get_json()['pg_exam_start']
    pg_exam_end = request.get_json()['pg_exam_end']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = update_problem_group(g.db, pg_id, pg_title, pg_exam_start, pg_exam_end)
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

#문제집 삭제 $$$$$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/delete_problem_group', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__delete_problem_group():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    pg_id = request.get_json()['pg_id']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = delete_problem_group(g.db, pg_id)
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

#문제집 활성/비활성 $$$$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/change_activate', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__change_activate():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    pg_id = request.get_json()['pg_id']
    pg_activate = request.get_json()['pg_activate']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = change_activate(g.db, pg_id, pg_activate)
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

#문제집 시험모드 수정 $$$$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/change_exam', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__change_exam():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    pg_id = request.get_json()['pg_id']
    pg_exam = request.get_json()['pg_exam']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = change_exam(g.db, pg_id, pg_exam)
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

#문제집 시험모드 체크
@BP.route('/API/V1/problem_manage/check_exam', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__check_exam():
    process_time = time.time()
    pg_id = request.get_json()['pg_id']
    if check_user(g.db, get_jwt_identity()):    
        result = check_exam(g.db, pg_id)
        try:
            result = check_exam(g.db, pg_id)
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

#특정 문제집의 모든 학생에 대한 점수 정보
@BP.route('/API/V1/problem_manage/get_total_score', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_total_score():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    PG_ID = request.get_json()['pg_id']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = get_total_score(g.db, CLASS_ID, PG_ID)
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


#################################################################################

#problem 실행
@BP.route('/API/V1/problem_manage/execute', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__execute():
    process_time = time.time()
    QUERY = request.get_json()['query']
    CLASS_ID = request.get_json()['class_id']
    if check_user(g.db, get_jwt_identity()):    
        try:
            result = query_execute(g.db, g.testdb, QUERY, CLASS_ID)
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

#problem 제출
@BP.route('/API/V1/problem_manage/submit', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__submit():
    process_time = time.time()
    QUERY = request.get_json()['query']
    CLASS_ID = request.get_json()['class_id']
    P_ID = request.get_json()['p_id']
    if check_user(g.db, get_jwt_identity()):    
        result = query_submit(g.db, g.testdb, get_jwt_identity(), QUERY, CLASS_ID, P_ID)
        try:
            result = query_submit(g.db, g.testdb, get_jwt_identity(), QUERY, CLASS_ID, P_ID)
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

#최근에 제출 했던 쿼리 반환
@BP.route('/API/V1/problem_manage/last_query', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__last_query():
    process_time = time.time()
    P_ID = request.get_json()['p_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_last_query(g.db, get_jwt_identity(), P_ID)
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

#사용자가 시도한 문제 반환
@BP.route('/API/V1/problem_manage/get_myproblem')
@jwt_required
def API_V1_problem_manage__get_myproblem():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_myproblem(g.db, get_jwt_identity())
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

#문제 생성 $$$$$$$$$$$$$$$$$4
@BP.route('/API/V1/problem_manage/create_problem', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__create_problem():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    pg_id = request.get_json()['pg_id']
    p_title = request.get_json()['p_title']
    p_content = request.get_json()['p_content']
    p_answer = request.get_json()['p_answer']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = create_problem(g.db, pg_id, p_title, p_content, p_answer)
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

#문제 수정 $$$$$$$$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/update_problem', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__update_problem():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    p_id = request.get_json()['p_id']
    p_title = request.get_json()['p_title']
    p_content = request.get_json()['p_content']
    p_answer = request.get_json()['p_answer']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = update_problem(g.db, p_id, p_title, p_content, p_answer)
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

#문제 삭제 $$$$$$$$$$$$$$$$$$$
@BP.route('/API/V1/problem_manage/delete_problem', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__delete_problem():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    p_id = request.get_json()['p_id']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = delete_problem(g.db, p_id)
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

#관리자전용 문제 반환
@BP.route('/API/V1/problem_manage/admin_problem', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__admin_problem():
    process_time = time.time()
    class_id = request.get_json()['class_id']
    p_id = request.get_json()['p_id']
    if check_class_admin(g.db, class_id, get_jwt_identity()):
        try:
            result = get_admin_problem(g.db, p_id)
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

#사용자가 시도한 문제 반환
@BP.route('/API/V1/problem_manage/get_up_id', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_up_id():
    process_time = time.time()
    UP_ID = request.get_json()['up_id']
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_up_id(g.db, UP_ID)
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


#############################################################################

#문제 테이블 삽입
@BP.route('/API/V1/problem_manage/push_testdb', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__push_testdb():
    process_time = time.time()
    CLASS_ID = request.form['class_id']
    FILES = request.files.getlist('file')
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        #파일이 있냐?!
        if FILES:
            FILE = FILES[0]
            #파일 확장자 / 이름길이 체크
            file_check = file_name_encode(FILE.filename, get_jwt_identity())
            if file_check:
                FILE.save('./models/testdb_table/'+ file_check)
        try:
            result = push_testDB(g.db, g.testdb, file_check, CLASS_ID)
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

#문제 테이블 조회
@BP.route('/API/V1/problem_manage/get_testdb', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__get_testdb():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = get_testdb(g.db, CLASS_ID)
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

#테이블 삭제
@BP.route('/API/V1/problem_manage/delete_testdb', methods = ['POST'])
@jwt_required
def API_V1_problem_manage__delete_testdb():
    process_time = time.time()
    CLASS_ID = request.get_json()['class_id']
    MT_ID = request.get_json()['mt_id']
    if check_class_admin(g.db, CLASS_ID, get_jwt_identity()):
        try:
            result = delete_testdb(g.db, g.testdb, MT_ID)
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

#############################################################################
def file_name_encode(file_name, admin_id):
	#허용 확장자 / 길이인지 확인.
	if file_name.split('.')[-1].lower() == "sql" and len(file_name) < 240:

		#이름 변환!
		path_name = str('QOJ$' + admin_id + '$' + file_name)

		return path_name
	
	else:
		return None