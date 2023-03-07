from os import getenv
from dotenv import load_dotenv

load_dotenv()

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

