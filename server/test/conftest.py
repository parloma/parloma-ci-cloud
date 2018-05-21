
from flask import Flask, Response as BaseResponse, json
from flask.testing import FlaskClient
from werkzeug.utils import cached_property
import pytest
from server import create_app, db as _db


@pytest.fixture
def app():
	app = create_app('test')

	class Response(BaseResponse):
	    @cached_property
	    def json(self):
	        return json.loads(self.data)


	class TestClient(FlaskClient):
	    def open(self, *args, **kwargs):
	        if 'json' in kwargs:
	            kwargs['data'] = json.dumps(kwargs.pop('json'))
	            kwargs['content_type'] = 'application/json'
	        return super(TestClient, self).open(*args, **kwargs)

	app.response_class = Response
	app.test_client_class = TestClient
	return app

@pytest.fixture
def db(app, tmpdir_factory):
	app.config['DB_PATH'] = str(tmpdir_factory.mktemp('db').join('db.json'))
	_db._path = app.config['DB_PATH']
	return _db

@pytest.fixture
def client(app):
	yield app.test_client()
