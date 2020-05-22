#!/usr/bin/env python3
###########################################
from flask import g
from MySQLdb import *
###########################################
import qoj_global
from private_info import DB_HOST, DB_ID, DB_PW

def get_db():
    if 'db' not in g:
        g.db = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='QOJ', charset='utf8mb4', cursorclass=cursors.DictCursor)
    
    if 'testdb' not in g:
        g.testdb = connect(host=DB_HOST, user=DB_ID, password=DB_PW, db='testDB', charset='utf8mb4', cursorclass=cursors.DictCursor)
        
def close_db():
    db = g.pop('db', None)
    if db is not None:
        if db.open:
            db.close()

#몽고디비 첫 start collection 체킹 및 초기화
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
        sql = open("models/table/table__QOJ_class.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_user.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_user_class.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_admin_class.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_manage_testDB.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_problem_group.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_problem.sql").read()
        cursor.execute(sql)
        sql = open("models/table/table__QOJ_user_problem.sql").read()
        cursor.execute(sql)
        
    db.commit()
    db.close()

    ##############################################################################################################

    #DB연결 (testDB)
    db = connect(host=DB_HOST , user=DB_ID, password=DB_PW, charset='utf8mb4', cursorclass=cursors.DictCursor)

    #DB 생성
    try:
        with db.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS testDB"
            cursor.execute(sql)
        db.commit()
    except Exception as ex:
        print("DB init Failed")
        print(ex)
    db.select_db('testDB')

    
    #DB 테이블 생성
    with db.cursor() as cursor:
        sql = open("models/table/table__testDB_test.sql").read()
        cursor.execute(sql)

    db.commit()
    db.close()