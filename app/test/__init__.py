import logging
import boto3
from werkzeug.datastructures import FileStorage
from botocore.exceptions import ClientError
from app.main import Config
from app.main.service.aws_service import upload_file
from app.main.service.ski_service import upload_ski_picture


# list the contents of your S3 bucket to ensure you can connect.
def check_s3_connection():
    account_key = Config.AWS_ACCESSKEY
    account_secret = Config.AWS_SECRETKEY
    bucket_url = Config.BUCKET_URL

    s3_client = boto3.client(
        's3',
        aws_access_key_id=account_key,
        aws_secret_access_key=account_secret
    )

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_url)
        if 'Contents' in response:
            logging.info("Connection to S3 successful. Bucket contains:")
            for obj in response['Contents']:
                logging.info(obj['Key'])
        else:
            logging.info("Connection to S3 successful. Bucket is empty.")
    except ClientError as e:
        logging.error(f"Error connecting to S3: {e}")
        return False
    return True


def test_upload_file():
    with open("test_image.png", "rb") as test_file:
        file = FileStorage(stream=test_file, filename="test_image.png")
        path = "test_image.png"
        success = upload_file(file, path)
        if success:
            logging.info("Test file uploaded successfully")
        else:
            logging.error("Test file upload failed")


def test():

    file = FileStorage(stream=("test_image.png", "rb"), filename="test_image.png")
    upload_ski_picture(1, 12, file)


test()
"""check_s3_connection()
test_upload_file()"""
