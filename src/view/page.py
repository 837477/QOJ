#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
###########################################
import qoj_global

BP = Blueprint('page', __name__)

@BP.route('/')
@BP.route('/board')
@BP.route('/lecture')
def main():
	return render_template('index.html')