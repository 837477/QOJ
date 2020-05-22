#!/usr/bin/env python3
###########################################
from flask import *
from flask_jwt_extended import *
from flask_cors import CORS
###########################################
#from wp_global import *
import qoj_global
from private_info import *
from DB_initiat import *


#APPS
import page, auth, class_manage, error

application = Flask(__name__, instance_relative_config=True, static_folder="dist")
CORS(application)

#Debug or Release
application.config.update(
		DEBUG = True,
		JWT_SECRET_KEY = JWT_SECRET_KEY,
	)
jwt = JWTManager(application)

def main_app(test_config = None):
	#DB init
	init_db()
	#BP.pages
	application.register_blueprint(page.BP)
	application.register_blueprint(auth.BP)
	application.register_blueprint(class_manage.BP)
	application.register_blueprint(error.BP)


@application.before_request
def before_request():
	get_db()

@application.teardown_request
def teardown_request(exception):
	close_db()

if __name__ == '__main__':
	main_app()
	application.run(host='0.0.0.0', debug=True, port='5000')