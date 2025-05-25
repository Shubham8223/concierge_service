import boto3
from server.config.config import settings
aws_creds = settings.get_aws_credentials()

def get_bedrock_client():
    session = boto3.Session(
        aws_access_key_id=aws_creds["access_key"],
        aws_secret_access_key=aws_creds["secret_key"],
        region_name=aws_creds["region"]
    )
    client = session.client("bedrock-runtime")
    return client
