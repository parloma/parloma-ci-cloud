import os

def run_script(script_path):
    os.system("bash -c \"{}\"".format(script_path))

def run_ros_script(script):
    script = "source /opt/ros/kinetic/setup.bash && {}".format(script)
    run_script(script)