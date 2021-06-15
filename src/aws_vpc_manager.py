from abc import ABC

import boto3
from src.interfaces.i_vpc_manager import IVpcManager


class AwsVpcManager(IVpcManager, ABC):
    def __init__(self):
        # AmazonEc2Client
        self._client = boto3.client('ec2', use_ssl=False)
        self._resource = boto3.resource('ec2', use_ssl=False)

    async def create_vpc(self, tag_name, cidr_block):
        """
        Create a new vpc
        @param tag_name: name of the vpc
        @type tag_name: str
        @param cidr_block: primary IPv4 CIDR block for the VPC
        @type cidr_block: str
        @return: none
        @rtype: none
        @raise: exception when the vpc already exists
        """
        if not await self.exists(tag_name):
            vpc = self._resource.create_vpc(CidrBlock=cidr_block)
            vpc.create_tags(Tags=[{"Key": "Name", "Value": tag_name}])
            vpc.wait_until_available()
        else:
            raise VpcNameAlreadyExists

    async def delete_vpc(self, tag_name):
        """
        Delete the specified vpc
        @param tag_name: name of the vpc
        @type tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the vpc does not exist
        """
        if await self.exists(tag_name):
            vpc_id = await self.get_id(tag_name)
            self._client.delete_vpc(VpcId=vpc_id)
        else:
            raise VpcNameDoesNotExist

    async def exists(self, tag_name):
        """
        Define if the vpc exists or not
        @param tag_name: name of the vpc
        @type tag_name: str
        @return: true or false
        @rtype: bool
        """
        response = self._client.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': [tag_name]}])
        return True if response['Vpcs'] else False

    async def get_id(self, tag_name):
        """
        Get the id of the specified vpc
        @param tag_name: name of the vpc
        @type tag_name: str
        @return: id of the vpc
        @rtype: int
        @raise: exception when the specified vpc does not exist
        """
        response = self._client.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': [tag_name]}])
        if response['Vpcs']:
            return response['Vpcs'][0]['VpcId']
        raise VpcNameDoesNotExist


class VpcNameAlreadyExists(Exception):
    def __init__(self, expression="VpcNameAlreadyExists", message="Vpc already exists!"):
        self.expression = expression
        self.message = message


class VpcNameDoesNotExist(Exception):
    def __init__(self, expression="VpcNameDoesNotExist", message="Vpc doesn't exists!"):
        self.expression = expression
        self.message = message
