import boto3
from abc import ABC
from src.interfaces.i_keypair_manager import IKeypairManager
from src.aws_manager import AwsManager

class AwsKeypairManager(IKeypairManager, ABC, AwsManager):
    def __init__(self):
        AwsManager.__init__(self)

    def create(self, name):
        return self._client.create_key_pair(KeyName=name)

    def exists(self, name):
        try:
            response = self._client.describe_key_pairs(KeyNames=[name])
            return True if response['KeyPairs'] else False
        except:
            return False

    def get_id(self,name):
        try:
            response = self._client.describe_key_pairs(KeyNames=[name])
            return response['KeyPairId']
        except:
            return False

    def delete(self, name):
        key_pair = self._client.delete_key_pair(KeyName=name)
        return key_pair
