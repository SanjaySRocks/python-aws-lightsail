import boto3
from botocore.exceptions import NoCredentialsError
import mimetypes

def upload_file_to_bucket(file_name, object_name=None):
    """Upload a file to an S3 bucket using credentials from a profile and return the URL."""
    
    try:
        # Create a session using the default profile
        session = boto3.Session(profile_name="default")

        # Initialize the S3 resource and specify the bucket
        s3_client = session.client('s3')
        bucket_name = 'bucket-38mgsd'

        # Use the file name as the object name if not specified
        if object_name is None:
            object_name = file_name.split('\\')[-1]

        # Define the folder name within the bucket
        folder_name = "medico"
        object_key = f"{folder_name}/{object_name}"

        # Upload the file
        content_type, _ = mimetypes.guess_type(file_name)

        s3_client.upload_file(file_name, bucket_name, object_key, ExtraArgs={
                'ContentType': content_type or 'application/octet-stream'
            })

        # Construct the URL
        region = s3_client.meta.region_name
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return url

    except NoCredentialsError:
        print("Credentials not available.")
        return None

# Example usage
file_name = r'C:\Users\sanjay\Downloads\360_F_393139863_ZNwRPc4078pCDF3KoaUD86dJPI9C31KS.jpg'

# Upload file and get the URL
file_url = upload_file_to_bucket(file_name)

if file_url:
    print(f"File uploaded successfully. URL: {file_url}")
else:
    print("File upload failed.")
