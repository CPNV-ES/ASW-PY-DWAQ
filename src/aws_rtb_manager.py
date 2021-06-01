import boto3
from src.interfaces.i_rtb_manager import IRtbManager
import src.exception.rtb_exception as rtb_exception


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')

    async def create(self, rtb_tag_name, vpc_id):
        """
        Create the specified route table associated to the vpc
        """
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
            raise rtb_exception.RtbAlreadyExists

    async def associate(self, rtb_id, subnet_id):
        """
        Associate the specified route table with the subnet
        """
        self.client.associate_route_table(
            RouteTableId=rtb_id,
            SubnetId=subnet_id,
        )

    async def disassociate(self, association_id):
        """
        Dissociate the specified route table
        """
        self.client.disassociate_route_table(
            AssociationId=association_id,
        )

    async def delete(self, rtb_id):
        """
        Delete the specified route table
        """
        self.client.delete_route_table(
            RouteTableId=rtb_id,
        )

    async def create_route_igw(self, rtb_id, cidr_block, gateway_id):
        """
        Create the specified route table with the internet gateway
        """
        self.client.create_route(
            DestinationCidrBlock=cidr_block,
            RouteTableId=rtb_id,
            GatewayId=gateway_id,
        )

    async def describe(self, rtb_tag_name):
        """
        Describe the specified route table
        """
        return self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [rtb_tag_name]
                }
            ],
        )

    async def exists(self, rtb_tag_name):
        """
        Check if the specified route table exists
        :return: Boolean
        """
        return True if await self.get_rtb_id(rtb_tag_name) else False

    async def get_assoc_id(self, rtb_tag_name):
        """
        Get the specified route table association id
        :return: Int
        """
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["Associations"][0]["RouteTableAssociationId"]
        except IndexError:
            return None

    async def get_rtb_id(self, rtb_tag_name):
        """
        Get the specified route table id
        :return: Int
        """
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["RouteTableId"]
        except IndexError:
            return None

    async def get_main_rtb_id_from_vpc(self, vpc_id):
        main_route_table = self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'association.main', 'Values': ["true"]

                }
            ])  # You can try "false" too
        pass
