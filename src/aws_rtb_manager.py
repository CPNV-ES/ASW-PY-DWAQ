import boto3
from src.interfaces.i_rtb_manager import IRtbManager


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2')

    async def create(self, rtb_tag_name, vpc_id):
        # Todo: Need to throw exception if's already created
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
        pass

    async def associate(self, rtb_id, subnet_id):
        # Todo: Need to throw exception if an error is returned
        self.client.associate_route_table(
            RouteTableId=rtb_id,
            SubnetId=subnet_id,
        )
        pass

    async def disassociate(self, association_id):
        # Todo: Need to throw exception if an error is returned
        self.client.disassociate_route_table(
            AssociationId=association_id,
        )
        pass

    async def delete(self, rtb_id):
        # Todo: Need to throw exception if an error is returned
        self.client.delete_route_table(
            RouteTableId=rtb_id,
        )
        pass

    async def create_route(self, rtb_id, cidr_block, gateway_id, local_gateway_id):
        self.client.create_route(
            DestinationCidrBlock=cidr_block,
            RouteTableId=rtb_id,
            GatewayId=gateway_id,
            LocalGatewayId=local_gateway_id,
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

    async def get_assoc_id(self, rtb_tag_name):
        # Todo: Get id from the json
        response = await self.describe(rtb_tag_name)
        if response:
            return response['RouteTables'][0]["Associations"][0]["RouteTableAssociationId"]

        return None

    async def get_rtb_id(self, rtb_tag_name):
        # Todo: Get id from the json
        response = await self.describe(rtb_tag_name)
        if response:
            return response['RouteTables'][0]["Associations"][0]["RouteTableId"]

        return None
