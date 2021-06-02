import boto3
import botocore
from src.interfaces.i_subnet_manager import ISubnetManager
import src.exception.subnet_exception as subnet_exception
import re


class AwsSubnetManager(ISubnetManager):
    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')

    async def create_subnet(self, subnet_tag_name, cidr_block, vpc_id):
        """
        Create a new subnet
        @param subnet_tag_name: name of the subnet
        @type subnet_tag_name: str
        @param cidr_block: primary IPv4 CIDR block for the subnet
        @type cidr_block: str
        @param vpc_id: id of the vpc
        @type vpc_id: int
        @return: none
        @rtype: none
        @raise: exception when the cidr is incorrect
        """
        if await self.exists(subnet_tag_name):
            raise subnet_exception.SubnetNameAlreadyExists()
        else:
            try:
                subnet = self.resource.create_subnet(CidrBlock=cidr_block, VpcId=vpc_id)
                subnet.create_tags(Tags=[{'Key': 'Name', 'Value': subnet_tag_name}])
            # Catch les exceptions du au CidrBlock
            except botocore.exceptions.ClientError as err:
                if re.search('CidrBlock', err.response['Error']['Message']):
                    raise subnet_exception.SubnetCidrBlockException("CIDR exception", err.response['Error']['Message'])
                else:
                    raise err

    async def delete_subnet(self, subnet_tag_name):
        """
        Delete the specified subnet
        @param subnet_tag_name: name of the subnet
        @type subnet_tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the specified subnet does not exist
        """
        if await self.exists(subnet_tag_name):
            subnet_id = await self.subnet_id(subnet_tag_name)
            self.client.delete_subnet(SubnetId=subnet_id)
        else:
            raise subnet_exception.SubnetNameDoesNotExist()

    async def exists(self, subnet_tag_name):
        """
        Define if the subnet exists or not
        @param subnet_tag_name: name of the subnet
        @type subnet_tag_name: str
        @return: true or false
        @rtype: bool
        """
        response = self.client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [subnet_tag_name]}])

        return True if response['Subnets'] else False

    async def subnet_id(self, subnet_tag_name):
        """
        Get the id of the specified subnet
        @param subnet_tag_name: name of the subnet
        @type subnet_tag_name: str
        @return: id of the subnet
        @rtype: int
        @raise: exception when the specified subnet does not exist
        """
        response = self.client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [subnet_tag_name]}])
        if response['Subnets']:
            return response['Subnets'][0]['SubnetId']
        raise subnet_exception.SubnetNameDoesNotExist()
