import os


def get_aws_region() -> str:
    return os.getenv("AWS_REGION", "us-west-2")
