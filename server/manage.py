import os
from server import create_app

if __name__ == '__main__':
	app = create_app(os.environ.get('CONFIG_SERVER') or 'default')
	app.run(host="0.0.0.0")