#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
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
    result = QOJ__problem(db).find__problem_list(user_id, pg_id)

    return result

#문제 반환
def get_problem(db, user_id, p_id):
    result = QOJ__problem(db).find__problem(user_id, p_id)

    return result