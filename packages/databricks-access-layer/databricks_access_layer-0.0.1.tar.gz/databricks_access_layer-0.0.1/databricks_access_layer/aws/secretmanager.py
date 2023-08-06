import json

import boto3
from botocore.exceptions import ClientError

from databricks_access_layer.aws import get_aws_region


def get_secret(secret_name: str) -> dict:
    region_name = get_aws_region()
    session = boto3.session.Session(region_name=region_name)
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_str = get_secret_value_response["SecretString"]
    return json.loads(secret_str)
