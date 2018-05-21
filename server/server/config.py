class Config(object):
    DB_PATH = '/db.json'
    BLINK_SCRIPT_PATH = '/blink.sh'

class DockerConfig(Config):
    DB_PATH = '/db.json'
    BLINK_SCRIPT_PATH = '/blink.sh'

class TestConfig(Config):
    DEBUG = True
    DB_PATH = './db.json'

configs = {
    'default': Config,
    'docker': DockerConfig,
    'test': TestConfig
}