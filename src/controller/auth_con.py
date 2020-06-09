#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
###########################################
from qoj_model import *

def sign_up(db, ID, PW, NAME, EMAIL):
	USER = QOJ__user(db).find__one(user_id = ID)

	if USER:
		return "exist user"

	QOJ__user(db).insert__one(ID, generate_password_hash(PW), NAME, EMAIL)
	
	USER = QOJ__user(db).find__one(user_id = ID)
	
	#DB에서 성공적으로 조회되면, 연습문제 연결하고 회원가입 성공!
	if USER:
		test_class = QOJ__class(db).find__one_name_admin("QOJ 연습문제", "QOJ_ADMIN")		
		QOJ__user_class(db).insert__one(ID, test_class['class_id'], 0)

		return create_access_token(
				identity = ID,
				expires_delta=False
        )
	else: "Fail"

def sign_in(db, ID, PW):
	USER = QOJ__user(db).find__one_simple(user_id = ID)
	if not USER:
		return "Not Found"

	if check_password_hash(USER['user_pw'], PW):
		return create_access_token(
				identity = ID,
				expires_delta=False
        )
	else:
		return "Incorrect pw"

def user_update(db, ID, PW, CHECK_PW, EMAIL):
	USER = QOJ__user(db).find__one_simple(user_id = ID)
	if not USER:
		return abort(401)

	if PW != CHECK_PW:
		return "Check PW"

	result = QOJ__user(db).update__information(db, ID, generate_password_hash(PW), EMAIL)

	return result

def get_userinfo(db, JWT):
	USER = QOJ__user(db).find__one(user_id = JWT)
	if not USER: abort(401)

	return USER

def get_all_user(db):
	result = QOJ__user(db).find__all()

	return result

def withdrawal(db, JWT):
	USER = QOJ__user(db).find__one(user_id = JWT)
	if not USER: abort(401)

	result = QOJ__user(db).delete__one(user_id = JWT)

	return result
