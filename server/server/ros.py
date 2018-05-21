from flask_json import as_json
from flask import Blueprint, request, current_app
from .utils import run_ros_script

ros = Blueprint('ros', __name__,url_prefix='/api/1.1/ros')

@ros.route('/killnode', methods=["POST"])
@as_json
def killnode():
    run_ros_script('rosnode kill {}'.format(request.json['node']))
    return{}

@ros.route('/run', methods=["POST"])
@as_json
def runnode():
    with open('/tmp/rosnode.py', 'w+') as f:
        f.write(request.json['file'])
    run_ros_script('python /tmp/rosnode.py &')
    return {}