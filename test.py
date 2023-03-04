import boto3
from datetime import datetime
from aws_models import AWSConnection
from config import config_data
import json
from json import JSONDecodeError

# #### Initializa the S3 resource ####

# session = boto3.Session(aws_access_key_id=config_data['AWS_ACCESS_KEY'],
#                         aws_secret_access_key=config_data['AWS_ACCESS_SECRET'])


# s3 = session.resource('s3')

# my_bucket = s3.Bucket('de-tech-assessment-2022')

# # for my_bucket_object in my_bucket.objects.filter(Prefix='data/'):
# #     print(my_bucket_object.key)

# event_dict = dict()
# mapping = dict()
# files_in_s3 = [f.key.split('data' + "/")[1] for f in my_bucket.objects.filter(Prefix='data/').all()]

# def sort(datestr):
#     date = datestr[:-12]
#     date_a = datetime.strptime(date, '%Y-%m-%d-%H-%M-%S')
#     return date_a

# for file in files_in_s3:
#     print(file)

s3_bucket = AWSConnection(bucket=config_data['BUCKET_NAME'], 
                      access_key=config_data['AWS_ACCESS_KEY'],
                      access_secret=config_data['AWS_ACCESS_SECRET'], 
                      resource='s3')

# files = s3_bucket.list_object_s3_bucket()
# for file in files:
#     print(file)

a = s3_bucket.get_file_s3_bucket(filename='data/2019-06-01-15-17-4-events.json')
