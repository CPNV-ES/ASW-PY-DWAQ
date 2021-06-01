import boto3
import json
from src.interfaces.i_vpc_manager import IVpcManager
import src.exception.vpc_exception as vpc_exception


class AwsVpcManager(IVpcManager):
    def __init__(self):
        # AmazonEc2Client
        self._client = boto3.client('ec2')
        self._resource = boto3.resource('ec2')
        # Vpcs list
        self.vpcs = None

    async def create_vpc(self, vpc_tag_name, cidr_block):
        """
        Create a new vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        cidr_block : string
            The primary IPv4 CIDR block for the VPC
        """
        if not await self.exists(vpc_tag_name):
            vpc = self._resource.create_vpc(CidrBlock=cidr_block)
            vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_tag_name}])
            vpc.wait_until_available()
        else:
            raise vpc_exception.VpcNameAlreadyExists('AwsVpcManager', 'Already exists')

    async def delete_vpc(self, vpc_tag_name):
        """
        Delete a vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        if await self.exists(vpc_tag_name):
            vpc_id = await self.vpc_id(vpc_tag_name)
            self._client.delete_vpc(VpcId=vpc_id)
        else:
            raise vpc_exception.VpcNameDoesntExists('AwsVpcManager', 'Vpc "' + vpc_tag_name + '" doesn\'t exists')

    async def exists(self, vpc_tag_name):
        """
        Verify if the vpc exists

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc

        Returns
        -------
        Boolean : True if the vpc exists
        """
        response = self._client.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': [vpc_tag_name]}])
        return True if response['Vpcs'] else False

    async def describe_vpcs(self):
        """
        Retrieve all the vpcs
        """
        vpcs = list(self._resource.vpcs.filter(Filters=[]))
        response = None
        for vpc in vpcs:
            response = self._client.describe_vpcs(
                VpcIds=[
                    vpc.id,
                ]
            )
        return json.dumps(response, sort_keys=True, indent=4)

    async def vpc_id(self, vpc_tag_name):
        """
        Get the vpc id

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        response = self._client.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': [vpc_tag_name]}])
        if response['Vpcs']:
            return response['Vpcs'][0]['VpcId']
        raise vpc_exception.VpcNameDoesntExists('AwsVpcManager', 'Vpc "' + vpc_tag_name + '" doesn\'t exists')