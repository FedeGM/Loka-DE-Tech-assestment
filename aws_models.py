import boto3
import pandas as pd
from datetime import datetime
import json
import ast
import logging
from config import logger


class AWSConnection:
    def __init__(self, bucket: str, access_key: str, access_secret: str, resource: str) -> None:
        self.bucket_name = bucket
        self.resource = resource
        self.aws_session = boto3.Session(
            aws_access_key_id=access_key, aws_secret_access_key=access_secret)
        self.aws_client = boto3.client(service_name=self.resource,
                                       aws_access_key_id=access_key,
                                       aws_secret_access_key=access_secret)
        self.aws_resource = self.aws_session.resource(self.resource)

    def sort_files_in_bucket(self, filename):
        str_date = filename[:-12]
        date = datetime.strptime(str_date, '%Y-%m-%d-%H-%M-%S')
        return date

    def list_folders_s3_bucket(self):
        s3_bucket = self.aws_resource.Bucket(self.bucket_name)
        folders_in_s3 = [f.key.split('/')[0] for f in s3_bucket.objects.all()]
        unique_folders = list(dict.fromkeys(folders_in_s3))
        return unique_folders

    def list_object_s3_bucket(self):
        s3_bucket = self.aws_resource.Bucket(self.bucket_name)
        files_in_s3 = [f.key for f in s3_bucket.objects.all()]
        return files_in_s3

    def list_sorted_object_s3_bucket(self, prefix: str):
        s3_bucket = self.aws_resource.Bucket(self.bucket_name)
        files_in_s3 = [f.key.split(prefix + "/")[1] for f in s3_bucket.objects.filter(Prefix=prefix+'/').all()]
        files_in_s3.sort(key=self.sort_files_in_bucket)
        return files_in_s3

    def get_file_s3_bucket(self, filename):
        response = self.aws_resource.Object(
            self.bucket_name,
            filename)

        status = response.get()['ResponseMetadata']['HTTPStatusCode']
        if status == 200:
            logger(f"Successful S3 get_object response. Status - {status}")
            file_content = response.get()['Body'].read().decode('utf-8')
            json_content = [json.loads(line) for line in file_content.splitlines()]
            return json_content
        else:
            logger(f"Unsuccessful S3 get_object response. Status - {status}")

    def move_files_to_a_s3(self, s3_bucket_from, source_filename, s3_bucket_to, target_filename):
        bucket = self.aws_resource.Bucket(s3_bucket_to)
        bucket.copy({'Bucket': s3_bucket_from, 'Key': source_filename}, target_filename)
        logger(f'file {source_filename} copied')
    
