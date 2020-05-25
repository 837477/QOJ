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

    def insert__one(self, class_name):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_class(class_name) VALUES(%s);"
            cursor.execute(query, (user_id))
        self.db.commit()
        return "success"
    
    def find__one(self, class_name):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM QOJ_class WHERE class_name = %s;"
            cursor.execute(query, (class_name,))
            result = cursor.fetchone()
        self.db.commit()
        return result

class QOJ__user_class(object):
    def __init__(self, db):
        super(QOJ__user_class, self).__init__()
        self.db = db

    def insert__one(self, user_id, class_id):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_user_class(user_id, class_id) VALUES(%s, %s);"
            cursor.execute(query, (user_id, class_id,))
        self.db.commit()
        return "success"

class QOJ__problem_group(object):
    def __init__(self, db):
        super(QOJ__problem_group, self).__init__()
        self.db = db

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

    def find__problem_list(self, user_id, pg_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.pg_id, A.p_id, A.p_name, B.up_state FROM QOJ_problem AS A LEFT JOIN (SELECT * FROM QOJ_user_problem WHERE user_id=%s) AS B ON A.p_id = B.p_id) AS RESULT_JOIN WHERE pg_id=%s;"
            cursor.execute(query, (user_id, pg_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result

    def find__problem(self, user_id, p_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.p_id, A.p_name, A.p_content, B.up_state, B.up_query FROM QOJ_problem AS A LEFT JOIN (SELECT p_id, up_state, up_query FROM QOJ_user_problem WHERE user_id=%s) AS B ON A.p_id = B.p_id) AS RESULT_JOIN WHERE p_id=%s;"
            cursor.execute(query, (user_id, p_id,))
            result = cursor.fetchone()
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