import boto3
import os
from botocore.credentials import ReadOnlyCredentials


# Set your AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_KEY')

# Endpoint URL
endpoitn_url = os.getenv('AWS_ENDPOINT_URL')

# Define session
session = boto3.session.Session()

# Create credentials object
credentials = ReadOnlyCredentials(aws_access_key, aws_secret_key, None)

# Create an S3 client
s3 = boto3.client(
    service_name='s3',
    endpoitn_url=endpoitn_url,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    config=boto3.session.Config(signature_version="s3v4")
)
