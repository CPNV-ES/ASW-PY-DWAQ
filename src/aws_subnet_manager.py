from abc import ABC
import botocore
from src.aws_manager import AwsManager
from src.interfaces.i_subnet_manager import ISubnetManager
import re


class AwsSubnetManager(ISubnetManager, ABC, AwsManager):
    def __init__(self):
        AwsManager.__init__(self)

    async def create_subnet(self, tag_name, cidr_block, vpc_id):
        """
        Create a new subnet
        @param tag_name: name of the subnet
        @type tag_name: str
        @param cidr_block: primary IPv4 CIDR block for the subnet
        @type cidr_block: str
        @param vpc_id: id of the vpc
        @type vpc_id: int
        @return: none
        @rtype: none
        @raise: exception when the cidr is incorrect
        """
        if await self.exists(tag_name):
            raise SubnetNameAlreadyExists()
        else:
            try:
                subnet = self._resource.create_subnet(CidrBlock=cidr_block, VpcId=vpc_id)
                subnet.create_tags(Tags=[{'Key': 'Name', 'Value': tag_name}])
            # Catch cidr block exceptions
            except botocore.exceptions.ClientError as err:
                if re.search('CidrBlock', err.response['Error']['Message']):
                    raise SubnetCidrBlockException("CIDR exception", err.response['Error']['Message'])
                else:
                    raise err

    async def delete_subnet(self, tag_name):
        """
        Delete the specified subnet
        @param tag_name: name of the subnet
        @type tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the specified subnet does not exist
        """
        if await self.exists(tag_name):
            subnet_id = await self.get_id(tag_name)
            self._client.delete_subnet(SubnetId=subnet_id)
        else:
            raise SubnetNameDoesNotExist()

    async def exists(self, tag_name):
        """
        Define if the subnet exists or not
        @param tag_name: name of the subnet
        @type tag_name: str
        @return: true or false
        @rtype: bool
        """
        response = self._client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [tag_name]}])

        return True if response['Subnets'] else False

    async def get_id(self, tag_name):
        """
        Get the id of the specified subnet
        @param tag_name: name of the subnet
        @type tag_name: str
        @return: id of the subnet
        @rtype: int
        @raise: exception when the specified subnet does not exist
        """
        response = self._client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [tag_name]}])
        if response['Subnets']:
            return response['Subnets'][0]['SubnetId']
        raise SubnetNameDoesNotExist()


class SubnetNameAlreadyExists(Exception):
    def __init__(self, expression="SubnetNameAlreadyExists", message="Subnet already exists!"):
        self.expression = expression
        self.message = message


class SubnetNameDoesNotExist(Exception):
    def __init__(self, expression="SubnetNameDoesNotExist", message="Subnet doesn't exists!"):
        self.expression = expression
        self.message = message


class SubnetCidrBlockException(Exception):
    def __init__(self, expression="SubnetCidrBlockException", message="Cidr block error!"):
        self.expression = expression
        self.message = message
