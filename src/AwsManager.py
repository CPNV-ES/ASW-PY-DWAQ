import boto3


class AwsManager:
    def __init__(self):
        self._client = boto3.client('ec2', use_ssl=False)
        self._resource = boto3.resource('ec2', use_ssl=False)
