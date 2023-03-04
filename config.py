from os import getenv
from dotenv import load_dotenv

load_dotenv()

config_data = dict()

config_data['BUCKET_NAME'] = getenv('BUCKET_NAME')
config_data['AWS_ACCESS_KEY'] = getenv('AWS_ACCESS_KEY')
config_data['AWS_ACCESS_SECRET'] = getenv('AWS_ACCESS_SECRET_KEY')
config_data['AWS_BUCKET'] = getenv('S3_URL')
