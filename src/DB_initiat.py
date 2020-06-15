#!/usr/bin/env python3
###########################################
from flask import g
from flask_jwt_extended import *
from werkzeug.security import *
from MySQLdb import *
###########################################
import qoj_global
from private_info import DB_HOST, DB_ID, DB_PW

def get_db():
    if 'db' not in g:
        g.db = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='QOJ', charset='utf8mb4', cursorclass=cursors.DictCursor)
    
    if 'testdb' not in g:
        g.testdb = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='QOJ_test', charset='utf8mb4', cursorclass=cursors.DictCursor)
        
def close_db():
    db = g.pop('db', None)
    if db is not None:
        if db.open:
            db.close()

    db = g.pop('testdb', None)
    if db is not None:
        if db.open:
            db.close()

#첫 DB 초기화
def init_db():
	#DB연결 (QOJ)
    db = connect(host=DB_HOST , user=DB_ID, password=DB_PW, charset='utf8mb4', cursorclass=cursors.DictCursor)

    #DB 생성
    try:
        with db.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS QOJ"
            cursor.execute(sql)
        db.commit()
    except Exception as ex:
        print("DB init Failed")
        print(ex)
    db.select_db('QOJ')

    #DB 테이블 생성
    with db.cursor() as cursor:
        sql = open("models/table/table__QOJ_user.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_class.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_user_class.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_manage_testDB.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_problem_group.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_problem.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_user_problem.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_view_all_problem.sql").read()
        cursor.execute(sql)
        
    db.commit()
    db.close()

    ##############################################################################################################

    #DB연결 (QOJ_test)
    db = connect(host=DB_HOST , user=DB_ID, password=DB_PW, charset='utf8mb4', cursorclass=cursors.DictCursor)

    #DB 생성
    try:
        with db.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS QOJ_test"
            cursor.execute(sql)
        db.commit()
    except Exception as ex:
        print("DB init Failed")
        print(ex)
    db.select_db('QOJ_test')

    
    #DB 테이블 생성
    with db.cursor() as cursor:
        sql = open("models/testdb_table/table__testDB_practice.sql").read()
        cursor.execute(sql)

    db.commit()
    db.close()

#DB 필수 데이터 삽입
def init_data():
    #DB연결 (QOJ)
    db = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='QOJ', charset='utf8mb4', cursorclass=cursors.DictCursor)

    ######################################################################
    #Admin 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_user WHERE user_id = "QOJ_ADMIN";'
        cursor.execute(query)
        result = cursor.fetchone()
        
    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_user(user_id, user_pw, user_name, user_email) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, ("QOJ_ADMIN", generate_password_hash("imlisgod"), "QOJ_MASTER", "QOJ@QOJ.com",))
        db.commit()
    ######################################################################

    ######################################################################
    #QOJ_class 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_class WHERE class_name = "QOJ 연습문제";'
        cursor.execute(query)
        result = cursor.fetchone()

    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_class(class_name, user_id) VALUES(%s, %s);"
            cursor.execute(query, ("QOJ 연습문제", "QOJ_ADMIN"))
        db.commit()
    #######################################################################

    ######################################################################
    #QOJ_user_class 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_class WHERE class_name = "QOJ 연습문제";'
        cursor.execute(query)
        QOJ_class = cursor.fetchone()

    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_user_class WHERE class_id = "%s" AND user_id = "QOJ_ADMIN";'
        cursor.execute(query, (QOJ_class['class_id'],))
        result = cursor.fetchone()
    
    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_class(class_id, user_id, uc_type) VALUES(%s, %s, %s);"
            cursor.execute(query, (QOJ_class['class_id'], "QOJ_ADMIN", 1))
        db.commit()
    
    #######################################################################

    #####################################################################
    #QOJ_manage_testDB 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_manage_testDB WHERE mt_table_name = "QOJ$QOJ_ADMIN$practice" and class_id = "%s";'
        cursor.execute(query, (QOJ_class['class_id'],))
        result = cursor.fetchone()

    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_manage_testDB(class_id, mt_table_name) VALUES(%s, %s);"
            cursor.execute(query, (QOJ_class['class_id'], "QOJ$QOJ_ADMIN$practice",))
        db.commit()
    #######################################################################

    ######################################################################
    #QOJ_problem_group 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_problem_group WHERE pg_title = "연습문제" and class_id = "%s";'
        cursor.execute(query, (QOJ_class['class_id'],))
        result = cursor.fetchone()

    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem_group(pg_title, class_id) VALUES(%s, %s);"
            cursor.execute(query, ("연습문제", QOJ_class['class_id'],))
        db.commit()
    #######################################################################

    ######################################################################
    #QOJ_problem 초기화
    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_problem_group WHERE class_id = "%s" and pg_title = "연습문제";'
        cursor.execute(query, (QOJ_class['class_id'],))
        QOJ_problem_group = cursor.fetchone()

    with db.cursor() as cursor:
        query = 'SELECT * FROM QOJ_problem WHERE p_title = "학생을 찾아라!" and pg_id = "%s";'
        cursor.execute(query, (QOJ_problem_group['pg_id'],))
        result = cursor.fetchone()

    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem(p_title, p_content, pg_id, p_answer) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, ("학생을 찾아라!", "practice 테이블은 세종대학교 학생 정보를 담은 테이블입니다. test 테이블로부터 컴퓨터공학과 학생들만 조회하려고 할 때, 쿼리문을 작성해주세요.", QOJ_problem_group['pg_id'], "SELECT * FROM practice WHERE major='컴퓨터공학과';",))
        db.commit()
    #######################################################################

    db.commit()
    db.close()

    db = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='QOJ_test', charset='utf8mb4', cursorclass=cursors.DictCursor)

    ######################################################################
    #QOJ_test 초기화
    with db.cursor() as cursor:
        #query = 'SELECT 1 FROM Information_schema.tables WHERE table_name = "QOJ_ADMIN$practice" AND table_schema = "QOJ_test";'
        query = "SELECT * FROM QOJ$QOJ_ADMIN$practice WHERE sid = 1;"
        cursor.execute(query)
        result = cursor.fetchone()

    if not result:
        with db.cursor() as cursor:
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (1, '홍길동', '16008740', '컴퓨터공학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (2, '김나무', '21007221', '건축공학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (3, '오지오', '18000002', '나노신소재학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (4, '강정우', '16004122', '데이터사이언스학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (5, '하원빈', '17005123', '컴퓨터공학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (6, '서정빈', '17005812', '수학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (7, '김영석', '19001020', '물리천문학과');"
            cursor.execute(query)
            query = "INSERT INTO QOJ$QOJ_ADMIN$practice(sid, name, id, major) VALUES (8, '나장후', '20004210', '지능기전학과');"
            cursor.execute(query)
        db.commit()
    #######################################################################

    db.close()
