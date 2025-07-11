from pyconfigparser import configparser, ConfigError
from schema import Use, And

SCHEMA_CONFIG = {
    'api': {
    	'user': And(Use(str), lambda string: len(string) > 0),
    	'password': And(Use(str), lambda string: len(string) > 0),
    	'endpoint': And(Use(str), lambda string: len(string) > 0)
    }
}


def init():

    try:
        config = configparser.get_config(SCHEMA_CONFIG, config_dir='./', file_name='config.yml')
    except ConfigError as e:
        print(e)
        exit()
    return config
