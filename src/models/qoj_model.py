#!/usr/bin/env python3
############################################################
from MySQLdb import *
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
############################################################
import qoj_global
from DB_initiat import *

class QOJ__user(object):
    def __init__(self, db):
        super(QOJ__user, self).__init__()
        self.db = db

    #사용자 삽입
    def insert__one(self, user_id, user_pw, user_name, user_email):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user(user_id, user_pw, user_name, user_email) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (user_id, user_pw, user_name, user_email,))
        self.db.commit()
        return "success"

    #사용자 정보 갱신
    def update__information(self, user_id, user_pw, user_email):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_user SET user_pw=%s, user_email=%s WHERE user_id=%s;"
            cursor.execute(query, (user_pw, user_email, user_id,))
        self.db.commit()
        return "success"
    
    #사용자 삭제
    def delete__one(self, user_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_user WHERE user_id=%s;"
            cursor.execute(query, (user_id,))
        self.db.commit()
        return "success"

    #사용자 전체 반환
    def find__all(self):
        with self.db.cursor() as cursor:
            query = "SELECT user_id, user_name FROM QOJ_user;"
            cursor.execute(query)
            result = cursor.fetchall()
        self.db.commit()
        return result

    #사용자 찾기 (심플용 = 회원 확인용)
    def find__one_simple(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT user_id, user_pw FROM QOJ_user WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    #사용자 찾기 (정보 반환용)
    def find__one(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT user_id, user_name, user_email FROM QOJ_user WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result
    
class QOJ__class(object):
    def __init__(self, db):
        super(QOJ__class, self).__init__()
        self.db = db
    
    #분반 추가
    def insert__one(self, class_name, class_admin):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_class(class_name, user_id) VALUES(%s, %s);"
            cursor.execute(query, (class_name, class_admin,))
        self.db.commit()
        return "success"

    #분반 수정
    def update__one(self, class_id, class_name, class_admin):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_class SET class_name=%s, user_id=%s WHERE class_id=%s;"
            cursor.execute(query, (class_name, class_admin, class_id,))
        self.db.commit()
        return "success"

    #분반 삭제
    def delete__one(self, class_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_class WHERE class_id=%s"
            cursor.execute(query, (class_id,))
        self.db.commit()
        return "success"
    
    #분반 전체 반환
    def find__all(self):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class;"
            cursor.execute(query)
            result = cursor.fetchall()
        self.db.commit()
        return result

    #분반 아이디로 찾기
    def find__one_id(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class WHERE class_id=%s;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    #분반 이름과 담당 교수로 찾기
    def find__one_name_admin(self, class_name, class_admin):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class WHERE class_name=%s and user_id=%s;"
            cursor.execute(query, (class_name, class_admin,))
            result = cursor.fetchone()
        self.db.commit()
        return result

class QOJ__user_class(object):
    def __init__(self, db):
        super(QOJ__user_class, self).__init__()
        self.db = db

    #분반 사용자 연결 추가
    def insert__one(self, user_id, class_id, uc_type):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_class(user_id, class_id, uc_type) VALUES(%s, %s, %s);"
            cursor.execute(query, (user_id, class_id, uc_type,))
        self.db.commit()
        return "success"
    
    #해당 분반의 관리자들 삭제
    def delete__admin_in_class(self, class_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_user_class WHERE class_id=%s AND uc_type=1"
            cursor.execute(query, (class_id,))
        self.db.commit()
        return "success"

    #해당 분반의 사용자의 연결 정보 반환
    def find__user_class_id(self, user_id, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_class WHERE user_id=%s AND class_id=%s;"
            cursor.execute(query, (user_id, class_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result
    
    #특정 분반의 사용자들 반환
    def find__user_in_class(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_class WHERE class_id=%s ORDER BY user_id;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

class QOJ__user_problem(object):
    def __init__(self, db):
        super(QOJ__user_problem, self).__init__()
        self.db = db

    #사용자 문제 풀이 제출 (문제, 사용자 연결)
    def insert__one(self, user_id, p_id, up_state, up_query):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_problem(user_id, p_id, up_state, up_query) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (user_id, p_id, up_state, up_query,))
        self.db.commit()
        return "success"
    
    #특정 사용자가 특정 문제에서 마지막에 제출한 문제 반환 (정답이 있으면 정답중 가장 최근 것 반환)
    def find__last_problem(self, user_id, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_problem WHERE user_id=%s AND p_id=%s AND up_state=1 ORDER BY up_date DESC LIMIT 1;"
            cursor.execute(query, (user_id, p_id,))
            result = cursor.fetchone()
            if not result:
                query = "SELECT * FROM QOJ_user_problem WHERE user_id=%s AND p_id=%s ORDER BY up_date DESC LIMIT 1;"
                cursor.execute(query, (user_id, p_id,))
                result = cursor.fetchone()
        self.db.commit()
        return result
    
    def find__up_id(self, up_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_problem WHERE up_id=%s";
            cursor.execute(query, (up_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result
    
class QOJ__problem_group(object):
    def __init__(self, db):
        super(QOJ__problem_group, self).__init__()
        self.db = db

    #문제집 생성
    def insert__one(self, class_id, pg_title):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem_group(class_id, pg_title) VALUES(%s, %s);"
            cursor.execute(query, (class_id, pg_title,))
        self.db.commit()
        return "success"

    #문제집 수정
    def update__one(self, pg_id, pg_title, pg_exam_start, pg_exam_end):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_title=%s, pg_exam_start=%s, pg_exam_end=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_title, pg_exam_start, pg_exam_end, pg_id,))
        self.db.commit()
        return "success"

    #문제집 활성화 수정 (활성/비활성)
    def update__activate(self, pg_id, pg_activate):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_activate=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_activate, pg_id,))
        self.db.commit()
        return "success"

    #문제집 시험모드 수정
    def update__exam(self, pg_id, pg_exam):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_exam=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_exam, pg_id,))
        self.db.commit()
        return "success"

    #문제집 삭제
    def delete__one(self, pg_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_problem_group WHERE pg_id=%s"
            cursor.execute(query, (pg_id,))
        self.db.commit()
        return "success"

    #특정 문제집 반환
    def find__problem_group(self, pg_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_problem_group WHERE pg_id = %s;"
            cursor.execute(query, (pg_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result
    
class QOJ__problem(object):
    def __init__(self, db):
        super(QOJ__problem, self).__init__()
        self.db = db

    #문제 생성
    def insert__one(self, pg_id, p_title, p_content, p_answer):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem(pg_id, p_title, p_content, p_answer) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (pg_id, p_title, p_content, p_answer,))
        self.db.commit()
        return "success"

    #문제 수정
    def update__one(self, p_id, p_title, p_content, p_answer):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem SET p_title=%s, p_content=%s, p_answer=%s WHERE p_id=%s;"
            cursor.execute(query, (p_title, p_content, p_answer, p_id,))
        self.db.commit()
        return "success"

    #문제 정보 반환 (정답 쿼리까지)
    def find_one(self, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_problem WHERE p_id=%s;"
            cursor.execute(query, (p_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    #문제 삭제
    def delete__one(self, p_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_problem WHERE p_id=%s"
            cursor.execute(query, (p_id,))
        self.db.commit()
        return "success" 

class QOJ__manage_testDB(object):
    def __init__(self, db):
        super(QOJ__manage_testDB, self).__init__()
        self.db = db

    #테스트 디비 테이블 정보 삽입
    def insert__one(self, class_id, mt_table_name):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_manage_testdb(class_id, mt_table_name) VALUES(%s, %s);"
            cursor.execute(query, (class_id, mt_table_name,))
        self.db.commit()
        return "success"

    #테스트 디비 정보 삭제
    def delete__one(self, mt_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_manage_testdb WHERE mt_id=%s;"
            cursor.execute(query, (mt_id,))
        self.db.commit()
        return "success"

    #테스트 디비 정보 반환
    def find__one(self, mt_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_manage_testdb WHERE mt_id=%s;"
            cursor.execute(query, (mt_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    #특정 분반의 테스트 디비 정보들 반환
    def find__class_id(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_manage_testdb WHERE class_id=%s;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

class QOJ__join_query(object):
    def __init__(self, db):
        super(QOJ__join_query, self).__init__()
        self.db = db

    def get__QOJ_user_class__class(self, user_id, uc_type):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.uc_id, A.user_id, A.uc_type, A.class_id, B.class_name, B.class_date FROM QOJ_user_class AS A LEFT JOIN (SELECT * FROM QOJ_class) AS B ON A.class_id = B.class_id) AS RESULT_JOIN WHERE user_id = %s AND uc_type = %s"
            cursor.execute(query, (user_id, uc_type))
            result = cursor.fetchall()
        self.db.commit()
        return result

    def find__problem_group__class(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.*, B.class_name FROM QOJ_problem_group AS A LEFT JOIN (SELECT * FROM QOJ_class) AS B ON A.class_id = B.class_id) AS RESULT_JOIN WHERE class_id = %s;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

    #유저가 푼 특정 문제 반환.
    def find__problem(self, user_id, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT DISTINCT(p_id), p_title, p_content, up_state, up_query, pg_id FROM (SELECT A.up_id, A.up_query, A.up_state, A.up_date, A.user_id, B.* FROM (SELECT * FROM QOJ_user_problem WHERE user_id=%s) AS A LEFT JOIN (SELECT * FROM QOJ_problem) AS B ON A.p_id = B.p_id ) AS RESULT WHERE p_id=%s;"
            cursor.execute(query, (user_id, p_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    def find__problem_list(self, user_id, pg_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.pg_id, A.p_id, A.p_title, B.up_id, B.up_state, B.user_id, B.up_query FROM QOJ_problem AS A LEFT JOIN (SELECT * FROM QOJ_user_problem WHERE user_id=%s) AS B ON A.p_id = B.p_id) AS RESULT_JOIN WHERE pg_id=%s;"
            cursor.execute(query, (user_id, pg_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

class QOJ__v_all_problem(object):
    def __init__(self, db):
        super(QOJ__v_all_problem, self).__init__()
        self.db = db

    def find__problem_analysis(self, class_id, pg_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM v_all_problem WHERE class_id=%s AND pg_id=%s ORDER BY p_id ASC, user_id ASC;"
            cursor.execute(query, (class_id, pg_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result
    
    #유저가 풀었던 모든 문제들 반환
    def find__myproblem(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM v_all_problem WHERE user_id = %s AND up_query IS NOT NULL;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

############################################################

class QOJ__testDB(object):
    def __init__(self, db):
        super(QOJ__testDB, self).__init__()
        self.db = db

    #관리자는 문제를 생성해야하기 때문에,
    #실제 DB에 커밋을 시켜준다.
    def execute_query_admin(self, query):
        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            self.db.commit()
        return result
    
    #유저가 작성한 쿼리는 무조건 트랜젝션으로 실제 디비에 commit하지 않음.
    #어차피 사용자는 SELECT만 치기 때문에 보안적 측면을 위해서!
    def execute_query_user(self, query):
        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result


