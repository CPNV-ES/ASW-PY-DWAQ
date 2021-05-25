import boto3
import json
from src.interfaces.i_vpc_manager import IVpcManager
from src.exception.vpc_exception import VpcNameAlreadyExists

class AwsVpcManager(IVpcManager):
    def __init__(self, aws_profile_name, aws_region_end_point):
        self.aws_profile_name = aws_profile_name
        self.aws_region_end_point = aws_region_end_point
        # AmazonEc2Client
        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')
        # Vpcs list
        self.vpcs = None

    async def create_vpc(self, vpc_tag_name, cidr_block):
        """Create a new vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        cidr_block : string
            The primary IPv4 CIDR block for the VPC
        """
        if not await self.exists(vpc_tag_name):
            vpc = self.resource.create_vpc(CidrBlock=cidr_block)
            vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_tag_name}])
            vpc.wait_until_available()
        else:
            raise VpcNameAlreadyExists('AwsVpcManager', 'Already exists')

    async def delete_vpc(self, vpc_tag_name):
        """Delete a vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        if await self.exists(vpc_tag_name):
            vpc_id = await self.vpc_id(vpc_tag_name)
            self.client.delete_vpc(VpcId=vpc_id)
        else:
            print("Vpc " + vpc_tag_name + " does not exists")

    async def exists(self, vpc_tag_name):
        """Verify if the vpc exists

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc

        Returns
        -------
        Boolean : True if the vpc exists
        """
        return True if await self.vpc_id(vpc_tag_name) else False

    async def describe_vpcs(self):
        """Retrieve all the vpcs
        """
        vpcs = list(self.resource.vpcs.filter(Filters=[]))
        response = None
        for vpc in vpcs:
            response = self.client.describe_vpcs(
                VpcIds=[
                    vpc.id,
                ]
            )
        return json.dumps(response, sort_keys=True, indent=4)

    async def vpc_id(self, vpc_tag_name):
        """Get the vpc id

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        filter = [{'Name': 'tag:Name', 'Values': [vpc_tag_name]}]
        vpcs_list = list(self.resource.vpcs.filter(Filters=filter))

        if vpcs_list:
            return vpcs_list[0].id

        return None
