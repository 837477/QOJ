#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
###########################################
from qoj_model import *

#분반 정보 반환
def get_classinfo(db, class_id):
	result = QOJ__class(db).find__one_id(class_id)
	
	return result

#본인 분반 반환
def get_class(db, ID):
	result = QOJ__join_query(db).get__QOJ_user_class__class(ID, 0)

	return result

#관리자 분반 반환
def get_admin_class(db, ID):
	result = QOJ__join_query(db).get__QOJ_user_class__class(ID, 1)

	return result

#분반 소속 회원 반환
def get_class_member(db, class_id):
	result = QOJ__user_class(db).find__user_in_class(class_id)

	return result

#모든 분반 반환
def get_all_class(db):
	result = QOJ__class(db).find__all()
	
	return result

#분반 생성
def create_class(db, class_name, class_admin, class_sub_admin):
	USER = QOJ__user(db).find__one(user_id = class_admin)
	if not USER:
		return "None user"

	result = QOJ__class(db).insert__one(class_name, USER['user_id'])

	if result == "success":
		admin_list = []

		#해당 분반 찾기
		class_info = QOJ__class(db).find__one_name_admin(class_name, USER['user_id'])
		
		#교수 관리자 목록에 넣기.
		admin_list.append(USER['user_id'])
		admin_list += class_sub_admin
		admin_list = list(set(admin_list))
		
		#조교 연결
		for sub_admin in admin_list:
			USER = QOJ__user(db).find__one(user_id = sub_admin)
			if not USER:
				return "None user"
			QOJ__user_class(db).insert__one(USER['user_id'], class_info['class_id'], 1)

	return "success"

#분반 수정
def update_class(db, class_id, class_name, class_admin, class_sub_admin):
	USER = QOJ__user(db).find__one(user_id = class_admin)
	if not USER:
		return "None user"

	result = QOJ__class(db).update__one(class_id, class_name, USER['user_id'])
	QOJ__user_class(db).delete__admin_in_class(class_id)

	if result == "success":
		admin_list = []

		#해당 분반 찾기
		class_info = QOJ__class(db).find__one_id(class_id)
		
		#교수 관리자 목록에 넣기.
		admin_list.append(class_info['user_id'])
		admin_list += class_sub_admin
		admin_list = list(set(admin_list))
		
		#조교 연결
		for sub_admin in admin_list:
			USER = QOJ__user(db).find__one(user_id = sub_admin)
			if not USER:
				return "None user"
			QOJ__user_class(db).insert__one(USER['user_id'], class_info['class_id'], 1)

#분반 삭제
def delete_class(db, class_id):
	result = class_info = QOJ__class(db).delete__one(class_id)

	return result

#분반에 회원 넣기
def push_user(db, class_id, user_list):
	for user in user_list:
		USER = QOJ__user(db).find__one(user_id = user)

		if USER:
			if not QOJ__user_class(db).find__user_class_id(USER['user_id'], class_id):
				QOJ__user_class(db).insert__one(USER['user_id'], class_id, 0)
	
	return "success"
