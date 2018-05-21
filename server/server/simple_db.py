import json

class SimpleDB():
	_path = '/tmp/db.json'

	def __init__(self, app=None):
		if app:
			self.init_app(app)

	def init_app(self, app):
		self._path = app.config.get('DB_PATH') or self._path
		self.load()


	def load(self):
		try:
			with open(self._path) as f:
				return json.load(f)
		except:
			self.dump({})
		return {}

	def dump(self, data):
		with open(self._path, 'w+') as f:
			json.dump(data, f)

