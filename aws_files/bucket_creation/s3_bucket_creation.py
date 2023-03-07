import boto3

from config import config_data

# Script that allow to create a S3 Bucket on AWS.

resource = boto3.resource("s3", region_name = config_data['AWS_REGION'])
bucket_name = "loka-s3-data-lake"
location = {'LocationConstraint': config_data['AWS_REGION']}
bucket = resource.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration=location)
print("Amazon S3 bucket has been created")
