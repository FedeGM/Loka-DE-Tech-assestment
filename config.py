from os import getenv
import logging
from logging.config import dictConfig

from dotenv import load_dotenv

load_dotenv()

logLevel = getenv('LOGGING_LEVEL', default= logging.DEBUG)
logging_config =dict()
logging_config['version'] = 1
str_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging_config['formatters'] = {'f': {'format': str_format}}
logging_config['handlers'] = {'h': {'class': 'logging.StreamHandler',
                                    'formatter': 'f',
                                    'level': logLevel}}
logging_config['root'] = {'handlers': ['h'], 'level': logLevel}

dictConfig(logging_config)

logger = logging.getLogger()

config_data = dict()

config_data['BUCKET_NAME_FROM'] = getenv('BUCKET_NAME_FROM')
config_data['BUCKET_NAME_TO'] = getenv('BUCKET_NAME_TO')
config_data['AWS_ACCESS_KEY'] = getenv('AWS_ACCESS_KEY')
config_data['AWS_ACCESS_SECRET'] = getenv('AWS_ACCESS_SECRET_KEY')
config_data['AWS_BUCKET'] = getenv('S3_URL')
config_data['AWS_REGION'] = getenv('AWS_REGION')
config_data['SERVER'] = getenv('MYSQL_SERVER')
config_data['DATABASE'] = getenv('MYSQL_DATABASE')
config_data['USERNAME'] = getenv('MYSQL_USERNAME')
config_data['PASSWORD'] = getenv('MYSQL_PASSWORD')
config_data['PORT'] = getenv('MYSQL_PORT')

