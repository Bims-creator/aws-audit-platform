import boto3


def get_session(profile_name: str | None = None, region_name: str = "us-east-1") -> boto3.Session:
    return boto3.Session(profile_name=profile_name, region_name=region_name)