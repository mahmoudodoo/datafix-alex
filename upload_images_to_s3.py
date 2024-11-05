import os
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
import urllib.parse

# Set up S3 client using boto3 with region and signature version 4
my_config = Config(
    region_name='us-east-2',  # Ohio region
    signature_version='s3v4'
)
s3 = boto3.client('s3', config=my_config)

# Specify your target S3 bucket and folder path
bucket_name = 'wpro.ai'
s3_folder = 'uploads/'

# Define the local folder containing the images
local_folder = 's3.amazonaws.com'

# Function to upload a file to S3
def upload_file_to_s3(local_file_path, bucket_name, s3_file_path):
    try:
        # Upload the file to S3
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Iterate over the files in the local folder and upload them to the S3 bucket
for root, dirs, files in os.walk(local_folder):
    for file_name in files:
        # Construct the full local file path
        local_file_path = os.path.join(root, file_name)
        
        # URL-decode the file name in case it contains special characters like %20 (spaces) etc.
        decoded_file_name = urllib.parse.unquote(file_name)
        
        # Remove the local folder prefix to construct the relative file path for S3
        relative_path = os.path.relpath(local_file_path, local_folder)
        
        # Ensure the relative path is URL-decoded
        decoded_relative_path = urllib.parse.unquote(relative_path)

        # URL-encode the S3 path to handle spaces and special characters correctly
        s3_file_path = urllib.parse.quote(os.path.join(s3_folder, decoded_relative_path).replace("\\", "/"))
        
        # Upload the file to S3
        upload_file_to_s3(local_file_path, bucket_name, s3_file_path)
