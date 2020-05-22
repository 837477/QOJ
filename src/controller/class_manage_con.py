#!/usr/bin/env python3
###########################################
from werkzeug.security import *
from flask_jwt_extended import *
import json
###########################################
from qoj_model import *

def get_class(db, ID):
	result = QOJ__join_query(db).get__QOJ_user_class__class(user_id = ID)
	
	return result