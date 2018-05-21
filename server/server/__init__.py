from flask import Flask
from flask_json import FlaskJSON
from .simple_db import SimpleDB
from .config import configs
from flask_cors import CORS

db = SimpleDB()

def create_app(conf_name = 'default'):
	app = Flask(__name__)
	app.config.from_object(configs[conf_name])

	FlaskJSON(app)
	db.init_app(app)
	CORS(app)

	from .main import main as main_bp
	app.register_blueprint(main_bp)
	
	from .ros import ros as ros_bp
	app.register_blueprint(ros_bp)

	return app