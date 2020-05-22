#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
import time
###########################################
from qoj_global import check_user
from class_manage_con import *

BP = Blueprint('class_manage', __name__)

@BP.route('/API/V1/class_manage/get_class')
@jwt_required
def API_V1_auth__get_class():
    process_time = time.time()
    if check_user(g.db, get_jwt_identity()):
        try:
            result = get_class(g.db, get_jwt_identity())
            status = "success"
        except:
            result = status = "fail"
    else:
        result = "Access denied"
    process_time = time.time() - process_time
    return jsonify(
        API_STATUS = status,
        RESULT = result,
        PROCESS_TIME = process_time
    )