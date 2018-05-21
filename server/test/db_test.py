from faker import Faker
from server.simple_db import SimpleDB
import json

def test_db_class(db,app):
	fk = Faker()
	fn = app.config['DB_PATH']

	assert db.load() == {}
	with open(fn) as f:
		assert json.load(f) == {}

	data =  {'data': fk.name()}
	db.dump(data)

	with open(fn) as f:
		assert json.load(f) == data

	data =  {'data': fk.name()}

	with open(fn, 'w') as f:
		json.dump(data, f)

	assert db.load() == data