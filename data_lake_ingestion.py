from datetime import datetime
import pandas as pd

#### Own Files ####
from aws_models import AWSConnection
from config import config_data
###################

#### Initializa the S3 resource ####

# Creating the connection to the 'de-tech-assessment-2022' S3 Bucket to list and pull all the files
s3_bucket_from = AWSConnection(bucket=config_data['BUCKET_NAME_FROM'],
                          access_key=config_data['AWS_ACCESS_KEY'],
                          access_secret=config_data['AWS_ACCESS_SECRET'],
                          resource='s3')

# Creating the connection to the new 'loka-s3-data-lake' (S3 Bucket) as Data Lake to store all the files from the original bucket. Here we store those files on a folder of that Day.
s3_bucket_to = AWSConnection(bucket=config_data['BUCKET_NAME_TO'],
                          access_key=config_data['AWS_ACCESS_KEY'],
                          access_secret=config_data['AWS_ACCESS_SECRET'],
                          resource='s3')

files = s3_bucket_from.list_sorted_object_s3_bucket(prefix='data')

snapshot_files = []

for file in files:
    stg_snapshot_file = dict()
    str_date = file[:-12]
    date = datetime.strptime(str_date, '%Y-%m-%d-%H-%M-%S').strftime('%Y-%m-%d')
    stg_snapshot_file['bucket_name'] = config_data['BUCKET_NAME_FROM']
    stg_snapshot_file['date'] = date
    stg_snapshot_file['filename'] = file
    snapshot_files.append(stg_snapshot_file)
    s3_bucket_to.move_files_to_a_s3(s3_bucket_from= config_data['BUCKET_NAME_FROM'],
                                    source_filename= 'data/'+stg_snapshot_file['filename'],
                                    s3_bucket_to = config_data['BUCKET_NAME_TO'],
                                    target_filename= stg_snapshot_file['date']+'/'+stg_snapshot_file['filename'])
