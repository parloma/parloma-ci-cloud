from flask_json import as_json
from flask import Blueprint, request, current_app
from . import db
import os
from .utils import run_script

main = Blueprint('main', __name__,url_prefix='/api/1.1')

@main.route('/discovery')
@as_json
def discovery():
    return db.load()

@main.route('/name', methods=['POST'])
@as_json
def name():
    data = db.load()
    data['name'] = request.json['name']
    db.dump(data)
    return {}, 200

@main.route('/blink', methods =['POST'])
@as_json
def blink():
    run_script(current_app.config['BLINK_SCRIPT_PATH'])
    return {}