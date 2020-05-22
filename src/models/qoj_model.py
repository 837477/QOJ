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
            query = "SELECT user_id, user_name, user_email, user_type FROM QOJ_user WHERE user_id = %s;"
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

class QOJ__admin_class(object):
    def __init__(self, db):
        super(QOJ__admin_class, self).__init__()
        self.db = db

    def insert__one(self, user_id, class_id):
        with self.db.cursor() as cursor:
            query = "INSERT INTO QOJ_admin_class(user_id, class_id) VALUES(%s, %s);"
            cursor.execute(query, (user_id, class_id,))
        self.db.commit()
        return "success"

class QOJ__join_query(object):
    def __init__(self, db):
        super(QOJ__join_query, self).__init__()
        self.db = db

    def get__QOJ_user_class__class(self, user_id):
        with self.db.cursor() as cursor:
            query = "SELECT * FROM (SELECT A.user_id, A.class_id, B.class_name FROM QOJ_user_class AS A LEFT JOIN (SELECT class_id, class_name FROM QOJ_class) AS B ON A.class_id = B.class_id) AS JOIN_RESULT WHERE user_id =%s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
        self.db.commit()
        return result