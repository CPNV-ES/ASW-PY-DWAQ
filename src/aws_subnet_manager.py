import boto3
from src.interfaces.i_subnet_manager import ISubnetManager
import src.exception.subnet_exception as subnet_exception


class AwsSubnetManager(ISubnetManager):
    def __init__(self, aws_profile_name, aws_region_end_point):
        self.aws_profile_name = aws_profile_name
        self.aws_region_end_point = aws_region_end_point
        # AmazonEc2Client
        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')

    async def create_subnet(self, subnet_tag_name, cidr_block, vpc_id):
        """Create a new subnet

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
            raise subnet_exception.SubnetNameAlreadyExists('Subnet creation error!',
                                                           'Subnet "' + subnet_tag_name + '" already exists')
        else:
            subnet = self.resource.create_subnet(CidrBlock=cidr_block, VpcId=vpc_id)
            subnet.create_tags(Tags=[{'Key': 'Name', 'Value': subnet_tag_name}])

    async def delete_subnet(self, subnet_tag_name):
        pass

    async def exists(self, subnet_tag_name):
        """Verify if the subnet exists

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
