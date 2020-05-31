import qoj_global
from DB_initiat import *
from MySQLdb import *
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

class QOJ__user(object):
    def __init__(self, db):
        super(QOJ__user, self).__init__()
        self.db = db

    def insert__one(self, user_id, user_pw, user_name, user_email):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user(user_id, user_pw, user_name, user_email) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (user_id, user_pw, user_name, user_email,))
        self.db.commit()
        return "success"

    def update__information(self, user_id, user_pw, user_email):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_user SET user_pw=%s, user_email=%s WHERE user_id=%s;"
            cursor.execute(query, (user_pw, user_email, user_id,))
        self.db.commit()
        return "success"
    
    def delete__one(self, user_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_user WHERE user_id=%s;"
            cursor.execute(query, (user_id,))
        self.db.commit()
        return "success"

    def find__all(self):
        with self.db.cursor() as cursor:
            query = "SELECT user_id, user_name FROM QOJ_user;"
            cursor.execute(query)
            result = cursor.fetchall()
        self.db.commit()
        return result

    def find__one_simple(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT user_id, user_pw FROM QOJ_user WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

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

    def insert__one(self, class_name, class_admin):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_class(class_name, user_id) VALUES(%s, %s);"
            cursor.execute(query, (class_name, class_admin,))
        self.db.commit()
        return "success"

    def delete__one(self, class_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_class WHERE class_id=%s"
            cursor.execute(query, (class_id,))
        self.db.commit()
        return "success"
    
    def find__all(self):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class;"
            cursor.execute(query)
            result = cursor.fetchall()
        self.db.commit()
        return result

    def find__id_one(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class WHERE class_id=%s;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    def find__one(self, class_name, class_admin):
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

    def insert__one(self, user_id, class_id, uc_type):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_class(user_id, class_id, uc_type) VALUES(%s, %s, %s);"
            cursor.execute(query, (user_id, class_id, uc_type,))
        self.db.commit()
        return "success"
    
    def delete__admin_in_class(self, class_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_user_class WHERE class_id=%s AND uc_type=1"
            cursor.execute(query, (class_id,))
        self.db.commit()
        return "success"

    def find__uc_type(self, user_id, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_class WHERE user_id=%s and class_id=%s"
            cursor.execute(query, (user_id, class_id))
            result = cursor.fetchone()
        self.db.commit()
        return result
    
    def find__user_in_class(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_class WHERE class_id=%s ORDER BY user_id;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result
    
    def find__user_class_id(self, user_id, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_class WHERE user_id=%s AND class_id=%s;"
            cursor.execute(query, (user_id, class_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

class QOJ__user_problem(object):
    def __init__(self, db):
        super(QOJ__user_problem, self).__init__()
        self.db = db

    def insert__one(self, user_id, p_id, up_state, up_query):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_problem(user_id, p_id, up_state, up_query) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (user_id, p_id, up_state, up_query,))
        self.db.commit()
        return "success"
    
    def find__last_problem(self, user_id, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_user_problem WHERE user_id=%s AND p_id=%s ORDER BY up_date DESC LIMIT 1;"
            cursor.execute(query, (user_id, p_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result
    

class QOJ__problem_group(object):
    def __init__(self, db):
        super(QOJ__problem_group, self).__init__()
        self.db = db

    def insert__one(self, class_id, pg_title):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem_group(class_id, pg_title) VALUES(%s, %s);"
            cursor.execute(query, (class_id, pg_title,))
        self.db.commit()
        return "success"

    def update__one(self, pg_id, pg_title, pg_exam_start, pg_exam_end):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_title=%s, pg_exam_start=%s, pg_exam_end=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_title, pg_exam_start, pg_exam_end, pg_id,))
        self.db.commit()
        return "success"

    def update__activate(self, pg_id, pg_activate):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_activate=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_activate, pg_id,))
        self.db.commit()
        return "success"

    def update__exam(self, pg_id, pg_exam):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem_group SET pg_exam=%s WHERE pg_id = %s;"
            cursor.execute(query, (pg_exam, pg_id,))
        self.db.commit()
        return "success"

    def delete__one(self, pg_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_problem_group WHERE pg_id=%s"
            cursor.execute(query, (pg_id,))
        self.db.commit()
        return "success"

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

    def insert__one(self, pg_id, p_title, p_content, p_answer):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_problem(pg_id, p_title, p_content, p_answer) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, (pg_id, p_title, p_content, p_answer,))
        self.db.commit()
        return "success"

    def update__one(self, p_id, p_title, p_content, p_answer):
        with self.db.cursor() as cursor:
            query = "UPDATE QOJ_problem SET p_title=%s, p_content=%s, p_answer=%s WHERE p_id=%s;"
            cursor.execute(query, (p_title, p_content, p_answer, p_id,))
        self.db.commit()
        return "success"

    def find__problem_list(self, user_id, pg_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.pg_id, A.p_id, A.p_title, B.up_state FROM QOJ_problem AS A LEFT JOIN (SELECT * FROM QOJ_user_problem WHERE user_id=%s) AS B ON A.p_id = B.p_id) AS RESULT_JOIN WHERE pg_id=%s;"
            cursor.execute(query, (user_id, pg_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

    def find_one_admin(self, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_problem WHERE p_id=%s;"
            cursor.execute(query, (p_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    def delete__one(self, p_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_problem WHERE p_id=%s"
            cursor.execute(query, (p_id,))
        self.db.commit()
        return "success" 

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

    def find__myproblem(self, user_id, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.p_id, A.p_title, A.p_content, B.up_state, B.up_query FROM QOJ_problem AS A LEFT JOIN (SELECT p_id, up_state, up_query FROM QOJ_user_problem WHERE user_id=%s) AS B ON A.p_id = B.p_id) AS RESULT_JOIN WHERE p_id=%s;"
            cursor.execute(query, (user_id, p_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

class QOJ__v_problem(object):
    def __init__(self, db):
        super(QOJ__v_problem, self).__init__()
        self.db = db

    def find__user(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT class_id, class_name, p_id, p_title, pg_exam, pg_id, pg_activate, up_state FROM v_problem WHERE user_id=%s AND pg_activate=1"
            cursor.execute(query, (user_id,))
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

class QOJ__manage_testDB(object):
    def __init__(self, db):
        super(QOJ__manage_testDB, self).__init__()
        self.db = db

    def insert__one(self, class_id, mt_table_name):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_manage_testdb(class_id, mt_table_name) VALUES(%s, %s);"
            cursor.execute(query, (class_id, mt_table_name,))
        self.db.commit()
        return "success"

    def delete__one(self, mt_id):
        with self.db.cursor() as cursor:
            query = "DELETE FROM QOJ_manage_testdb WHERE mt_id=%s;"
            cursor.execute(query, (mt_id,))
        self.db.commit()
        return "success"

    def find__one(self, mt_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_manage_testdb WHERE mt_id=%s;"
            cursor.execute(query, (mt_id,))
            result = cursor.fetchone()
        self.db.commit()
        return result

    def find__class_id(self, class_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_manage_testdb WHERE class_id=%s;"
            cursor.execute(query, (class_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

class QOJ__testDB(object):
    def __init__(self, db):
        super(QOJ__testDB, self).__init__()
        self.db = db

    def execute_query(self, query):
        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.db.commit()
        return result
