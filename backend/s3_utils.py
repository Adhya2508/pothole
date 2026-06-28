import boto3

BUCKET_NAME = "smart-road-adhya2505-2026"
REGION = "ap-south-1"

s3 = boto3.client("s3")


def upload_file(local_path, s3_key):

    s3.upload_file(
        local_path,
        BUCKET_NAME,
        s3_key
    )


def get_file_url(s3_key):

    return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{s3_key}"