#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
import sqlparse
import re
from datetime import datetime
###########################################
from qoj_model import *

#problem_group + class
def get_problem_group1(db, class_id):
	result = QOJ__join_query(db).find__problem_group__class(class_id)
	
	return result

#순수 problem_group 정보 반환
def get_problem_group2(db, pg_id):
	result = QOJ__problem_group(db).find__problem_group(pg_id)
	
	return result

#문제집 속 문제들 반환
def get_problem_list(db, user_id, pg_id):
    db_result = QOJ__join_query(db).find__problem_list(user_id, pg_id)

    result = []
    for temp in db_result:
        flag = True
        for temp2 in result:
            if (temp['p_id'] == temp2['p_id']) and (temp['user_id'] == temp2['user_id']):
                if temp['up_state'] == 1:
                    temp2['up_state'] = 1
                    temp2['up_id'] = temp['up_id']
                    temp2['up_query'] = temp['up_query']
                flag = False
                break
        if flag:
            result.append(temp)

    return result

#내가 풀었던 모든 문제 반환
def get_myproblem(db, JWT):
    db_result = QOJ__v_all_problem(db).find__myproblem(JWT)

    result = []
    for temp in db_result:
        flag = True
        for temp2 in result:
            if (temp['p_id'] == temp2['p_id']) and (temp['user_id'] == temp2['user_id']):
                if temp['up_state'] == 1:
                    temp2['up_state'] = 1
                    temp2['up_id'] = temp['up_id']
                    temp2['up_query'] = temp['up_query']
                flag = False
                break
        if flag:
            result.append(temp)

    return result

#문제 반환
def get_problem(db, user_id, p_id):
    result = QOJ__join_query(db).find__problem(user_id, p_id)

    return result

#문제집 생성
def create_problem_group(db, class_id, pg_title):
    result = QOJ__problem_group(db).insert__one(class_id, pg_title)

    return result

#문제집 수정
def update_problem_group(db, pg_id, pg_title, pg_exam_start, pg_exam_end):
    result = QOJ__problem_group(db).update__one(pg_id, pg_title, pg_exam_start, pg_exam_end)

    return result

#문제집 삭제
def delete_problem_group(db, pg_id):
    result = QOJ__problem_group(db).delete__one(pg_id)

    return result

#문제집 활성화/비활성화
def change_activate(db, pg_id, pg_activate):
    result = QOJ__problem_group(db).update__activate(pg_id, pg_activate)

    return result

#문제집 시험모드 정보 변경
def change_exam(db, pg_id, pg_exam):
    result = QOJ__problem_group(db).update__exam(pg_id, pg_exam)

    return result

#문제집 시험모드 체크
def check_exam(db, pg_id):
    result = QOJ__problem_group(db).find__problem_group(pg_id)

    if (datetime.strptime(result['pg_exam_start'], '%Y-%m-%d %H:%M:%S') < datetime.now()) and (datetime.strptime(result['pg_exam_end'], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now()):
        return True
    else:
        return False

#up_id로 user_problem에서 하나 반환
def get_up_id(db, up_id):
    result = QOJ__user_problem(db).find__up_id(up_id)

    return result

#####################################################################

#문제 생성
def create_problem(db, pg_id, p_title, p_content, p_answer):
    result = QOJ__problem(db).insert__one(pg_id, p_title, p_content, p_answer)

    return result

#문제 수정
def update_problem(db, p_id, p_title, p_content, p_answer):
    result = QOJ__problem(db).update__one(p_id, p_title, p_content, p_answer)

    return result

#문제 삭제
def delete_problem(db, p_id):
    result = QOJ__problem(db).delete__one(p_id)

    return result

#어드민 전용 문제 반환 (정답도 반환됨)
def get_admin_problem(db, p_id):
    result = QOJ__problem(db).find_one(p_id)

    return result

#테스트 디비 가져오기
def get_testdb(db, class_id):
    result = QOJ__manage_testDB(db).find__class_id(class_id)
    for temp in result:
        split_result = temp['mt_table_name'].split('$')
        temp['mt_table_name'] = split_result[-1:]
    return result

#테스트 디비 삭제
def delete_testdb(QOJ_db, testDB_db, mt_id):
    target = QOJ__manage_testDB(QOJ_db).find__one(mt_id)

    query = "DROP TABLE " + target['mt_table_name'] + ";"
    QOJ__testDB(testDB_db).execute_query_admin(query)

    result = QOJ__manage_testDB(QOJ_db).delete__one(mt_id)

    return result

#사용자 query execute
def query_execute(QOJ_db, testDB_db, query, class_id):
    class_info = QOJ__class(QOJ_db).find__one_id(class_id)
    
    result = sqlparse.parse(query)

    #허용안하는 키워드 분별
    keyword_checking = [str(t).upper() for t in result[0].tokens]
    if 'DROP' in keyword_checking or 'DELETE' in keyword_checking or 'UPDATE' in keyword_checking or 'USE' in keyword_checking or 'GRANT' in keyword_checking or 'SET' in keyword_checking or 'CREATE' in keyword_checking:
        return "Do not execute"
    
    header = ""
    #테이블 이름 빼오기
    table_name = parseSelectSql(sql = query)
    if table_name:
        header = "QOJ$" + class_info['user_id'] + "$"
        query = query.replace(table_name['tableName'], (header + table_name['tableName']))

    #테스트 디비에 실행!
    try:
        result = QOJ__testDB(testDB_db).execute_query_user(query)
    except Exception as e:
        result = str(e)
        result = result.replace("qoj_test.", "")
        result = result.replace("qoj.", "")
        result = result.replace(header, "")
        result = result.replace(header.lower(), "")

    if not result:
        result = "Empty set"

    return result

#사용자 query submit
def query_submit(QOJ_db, testDB_db, JWT, query, class_id, p_id):
    class_info = QOJ__class(QOJ_db).find__one_id(class_id)
    problem_object = QOJ__problem(QOJ_db).find_one(p_id)

    query_answer = problem_object['p_answer']

    user_query = query

    result = sqlparse.parse(query)

    #허용안하는 키워드 분별
    keyword_checking = [str(t).upper() for t in result[0].tokens]
    if 'DROP' in keyword_checking or 'DELETE' in keyword_checking or 'UPDATE' in keyword_checking or 'USE' in keyword_checking or 'GRANT' in keyword_checking or 'SET' in keyword_checking or 'CREATE' in keyword_checking or 'INSERT' in keyword_checking:
        return "Do not execute"
    
    header = ""
    #사용자 쿼리문 테이블명 파싱
    table_name = parseSelectSql(sql = user_query)
    if table_name:
        header = "QOJ$" + class_info['user_id'] + "$"
        user_query = user_query.replace(table_name['tableName'], (header + table_name['tableName']))
    
    #사용자 쿼리문 테이블명 파싱
    table_name = parseSelectSql(sql = query_answer)
    if table_name:
        query_answer = query_answer.replace(table_name['tableName'], ("QOJ$" + class_info['user_id'] + "$" + table_name['tableName']))
    
    #사용자 쿼리 테스트 디비에 실행!
    try:
        user_result = QOJ__testDB(testDB_db).execute_query_user(user_query)
    except Exception as e:
        user_result = str(e)
        user_result = result.replace("qoj_test.", "")
        user_result = result.replace("qoj.", "")
        user_result = result.replace(header, "")
        user_result = result.replace(header.lower(), "")
        return user_result

    if not result:
        return "Empty set"
    
    #정답 쿼리 테스트 디비에 실행!
    admin_result = QOJ__testDB(testDB_db).execute_query_user(query_answer)

    user_result = json.dumps(user_result)
    admin_result = json.dumps(admin_result)

    if user_result == admin_result:
        QOJ__user_problem(QOJ_db).insert__one(JWT, p_id, 1, query)
        return True
    else:
        QOJ__user_problem(QOJ_db).insert__one(JWT, p_id, 0, query)
        return False

#특정 문제의 특정 사용자의 마지막 제출 쿼리 가져오기
def get_last_query(db, JWT, p_id):
    result = QOJ__user_problem(db).find__last_problem(JWT, p_id)

    return result

#특정 분반의 특정 문제집의 모든 학생에 대한 점수 정보
def get_total_score(db, class_id, pg_id):
    db_result = QOJ__v_all_problem(db).find__problem_analysis(class_id, pg_id)

    result = []
    for temp in db_result:
        flag = True
        for temp2 in result:
            if (temp['p_id'] == temp2['p_id']) and (temp['user_id'] == temp2['user_id']):
                if temp['up_state'] == 1:
                    temp2['up_state'] = 1
                    temp2['up_id'] = temp['up_id']
                    temp2['up_query'] = temp['up_query']
                flag = False
                break
        if flag:
            result.append(temp)

    return result

#######################################################################

#test DB SQL 삽입
def push_testDB(QOJ_db, testDB_db, file_name, class_id):
    class_info = QOJ__class(QOJ_db).find__one_id(class_id)

    FILE = open("models/testdb_table/" + file_name, 'r', encoding='UTF8')

    FILE_result = SQL_list(FILE)

    for query in FILE_result:
        result = sqlparse.parse(query)
        
        #허용안하는 키워드 분별
        keyword_checking = [str(t).upper() for t in result[0].tokens]
        if 'DROP' in keyword_checking or 'DELETE' in keyword_checking or 'UPDATE' in keyword_checking or 'USE' in keyword_checking or 'GRANT' in keyword_checking or 'SET' in keyword_checking:
            continue
        
        #테이블 생성이면?
        if (query.upper()).startswith('CREATE'):
            #테이블 이름 빼오기
            table_name = [str(t) for t in result[0].tokens if t.ttype is None][0]

            #테이블 이름 속에 '$' 체크
            if '$' in table_name:
                return False
            
            #최종 테이블 이름 파싱
            parse_table_name = 'QOJ$' + class_info['user_id'] + '$' + table_name

            query = query.replace(table_name, parse_table_name)

            #테스트디비 관리 테이블에 추가!
            QOJ__manage_testDB(QOJ_db).insert__one(class_id, parse_table_name)

        #테스트 디비에 실행!
        QOJ__testDB(testDB_db).execute_query_admin(query)

def SQL_list(file):
	output = []
	one = ''
	while True:
		line = file.readline()
		if not line:
			break
		if line.startswith('--'):
			continue
		one += line
		
		if one.find(';') != -1:
			one = re.sub(pattern='[/*](.*?)[/]', repl="", string=one)
			if len(one) >= 5:
				output.append(one.strip())
			one = ''
	return output


#import sqlparse
#result = sqlparse.parse(sql)
#print([str(t) for t in result[0].tokens if t.ttype is None][0])
#[str(t).upper() for t in result[0].tokens]
#print([str(t) for t in result[0].tokens]) in ["select".... 이런식 ㄱ ㄱ]

def parseSelectSql(sql=None):
    parsedSelect = {}
    sqlParse = sqlparse.parse(sql)
    for token in sqlParse[0].tokens:
        if token._get_repr_name() == 'Identifier':
            parsedSelect ['tableName'] = token.value
    return parsedSelect 