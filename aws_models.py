import boto3
import pandas as pd
from datetime import datetime
import json
import ast
import logging


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

    def list_object_s3_bucket(self):
        s3_bucket = self.aws_resource.Bucket(self.bucket_name)
        files_in_s3 = [f.key.split('data' + "/")[1]
                       for f in s3_bucket.objects.filter(Prefix='data/').all()]
        files_in_s3.sort(key=self.sort_files_in_bucket)
        return files_in_s3

    def get_file_s3_bucket(self, filename):
        response = self.aws_resource.Object(
            self.bucket_name,
            filename)

        status = response.get()['ResponseMetadata']['HTTPStatusCode']
        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            file_content = response.get()['Body'].read().decode('utf-8')
            json_content = [json.loads(line) for line in file_content.splitlines()]
            return json_content
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
