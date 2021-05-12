import boto3
from src.interfaces.i_rtb_manager import IRtbManager


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2')

    async def create_rtb(self, rtb_tag_name, vpc_id):
        # Todo: Need to throw exception if's already created
        self.client.create_route_table(
            DryRun=True | False,
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'Tags': [{
                        'Key': 'Name',
                        'Value': rtb_tag_name
                    }]
                }
            ]
        )
        pass

    async def associate_rtb(self, rtb_id, subnet_id):
        # Todo: Need to throw exception if an error is returned
        self.client.associate_route_table(
            DryRun=True | False,
            RouteTableId=rtb_id,
            SubnetId=subnet_id,
        )
        pass

    async def disassociate_rtb(self, association_id):
        pass

    async def delete_rtb(self, rtb_id):
        pass

    async def rtb_exists(self, rtb_tag_name):
        pass

    async def create_route(self, rtb_id, cidr_block, gateway_id):
        pass

    async def describe_rtb(self, rtb_tag_name):
        self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [rtb_tag_name]
                }
            ],
            DryRun=True | False
        )
        pass
