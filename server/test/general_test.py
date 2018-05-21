from faker import Faker 
import uuid
import pytest

def test_apprunning(client):
	res = client.get('/')
	assert res.status_code is not None

def test_discovery_online(client):
	res = client.get('/api/1.1/discovery')
	assert res.status_code == 200
	assert res.content_type == 'application/json'
	assert type(res.json) == dict

def test_read_discovery_from_file(app, client, db):
	fk = Faker()
	d = {
	  "bridge": fk.domain_name(), 
	  "master": "*",
	  "model": "HBrain-CI v0.5.2", 
	  "name": fk.name(),
	  "rid": str(uuid.uuid4())
	}

	db.dump(d)

	res = client.get('/api/1.1/discovery')
	for key,item in d.items():
		assert res.json[key] == item

def test_change_name_endponit(client, app, db):
	fk = Faker()
	newname = fk.domain_name()
	res = client.post('/api/1.1/name', json = {'name': newname})
	assert res.status_code == 200
	data = db.load()
	assert data['name'] == newname

def test_endpoint_blink_run_shell_script(app, client, tmpdir_factory):
	test_dir = tmpdir_factory.mktemp('test_script_blink')
	shell_script = str(test_dir.join('blink.sh'))
	print(shell_script)

	app.config['BLINK_SCRIPT_PATH'] = shell_script

	output_file = str(test_dir.join('res.txt'))
	with open(shell_script, 'w') as f:
		f.write('echo ciao > {}'.format(output_file))

	res = client.post('/api/1.1/blink', json = {})
	assert res.status_code == 200

	with open(output_file) as f:
		assert f.read().strip() == 'ciao'

def test_run_script_function_works(tmpdir_factory):
	test_dir = tmpdir_factory.mktemp('test_script_blink')
	output_file = str(test_dir.join('res.txt'))
	shell_script = str(test_dir.join('blink.sh'))

	with open(shell_script, 'w') as f:
		f.write('echo ciao > {}'.format(output_file))

	from server.utils import run_script
	run_script(shell_script)

	with open(output_file) as f:
		assert f.read().strip() == 'ciao'
