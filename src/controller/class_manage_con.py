#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
###########################################
from qoj_model import *

def get_class(db, ID):
	result = QOJ__join_query(db).get__QOJ_user_class__class(ID, 0)
	
	return result

def get_admin_class(db, ID):
	result = QOJ__join_query(db).get__QOJ_user_class__class(ID, 1)

	return result