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

        Parameters
        ----------
        subnet_tag_name : string
            The name of the subnet
        cidr_block : string
            The primary IPv4 CIDR block for the subnet
        vpc_id: string
            The id of the vpc
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
        Delete a subnet

        Parameters
        ----------
        subnet_tag_name : string
            The name of the subnet
        """
        if await self.exists(subnet_tag_name):
            subnet_id = await self.subnet_id(subnet_tag_name)
            self.client.delete_subnet(SubnetId=subnet_id)
        else:
            raise subnet_exception.SubnetNameDoesntExists()

    async def exists(self, subnet_tag_name):
        """
        Verify if the subnet exists

        Parameters
        ----------
        subnet_tag_name : string
            The name of the subnet

        Returns
        -------
        Boolean : True if the subnet exists
        """
        response = self.client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [subnet_tag_name]}])

        return True if response['Subnets'] else False

    async def subnet_id(self, subnet_tag_name):
        """Get the subnet id

        Parameters
        ----------
        subnet_tag_name : string
            The name of the subnet

        Returns
        -------
        String : Subnet id
        """
        response = self.client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [subnet_tag_name]}])
        if response['Subnets']:
            return response['Subnets'][0]['SubnetId']
        raise subnet_exception.SubnetNameDoesntExists()
