import boto3
from src.interfaces.i_rtb_manager import IRtbManager
import src.exception.rtb_exception as rtb_exception


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2')

    async def create(self, rtb_tag_name, vpc_id):
        try:
            self.client.create_route_table(
                VpcId=vpc_id,
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [{
                            'Key': 'Name',
                            'Value': rtb_tag_name
                        }]
                    }
                ]
            )
        except Exception:
            raise rtb_exception.AlreadyExists
        pass

    async def associate(self, rtb_id, subnet_id):
        self.client.associate_route_table(
            RouteTableId=rtb_id,
            SubnetId=subnet_id,
        )
        pass

    async def disassociate(self, association_id):
        self.client.disassociate_route_table(
            AssociationId=association_id,
        )
        pass

    async def delete(self, rtb_id):
        self.client.delete_route_table(
            RouteTableId=rtb_id,
        )
        pass

    async def create_route_igw(self, rtb_id, cidr_block, gateway_id):
        self.client.create_route(
            DestinationCidrBlock=cidr_block,
            RouteTableId=rtb_id,
            GatewayId=gateway_id,
        )
        pass

    async def describe(self, rtb_tag_name):
        return self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [rtb_tag_name]
                }
            ],
        )

    async def exists(self, rtb_tag_name):
        return True if await self.get_rtb_id(rtb_tag_name) else False

    async def get_assoc_id(self, rtb_tag_name):
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["Associations"][0]["RouteTableAssociationId"]
        except IndexError:
            return None

    async def get_rtb_id(self, rtb_tag_name):
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["RouteTableId"]
        except IndexError:
            return None
