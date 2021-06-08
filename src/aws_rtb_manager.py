import boto3
from src.interfaces.i_rtb_manager import IRtbManager
import src.exception.rtb_exception as rtb_exception


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2', use_ssl=False)
        self.resource = boto3.resource('ec2', use_ssl=False)

    async def create(self, rtb_tag_name, vpc_id):
        """
        Create the specified route table
        @param rtb_tag_name: name of the route table
        @type rtb_tag_name: str
        @param vpc_id: the id of the vpc to attach
        @type vpc_id: int
        @return: none
        @rtype: none
        @raise: exception when the route table already exists
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
        Associate the specified route table to the specified subnet
        @param rtb_id: id of the route table for the association
        @type rtb_id: int
        @param subnet_id: id of the subnet for the association
        @type subnet_id: int
        @return: none
        @rtype: none
        """
        self.client.associate_route_table(
            RouteTableId=rtb_id,
            SubnetId=subnet_id,
        )

    async def disassociate(self, association_id):
        """
        Disassociate the specified association
        @param association_id: id of the association
        @type association_id: int
        @return: none
        @rtype: none
        """
        self.client.disassociate_route_table(
            AssociationId=association_id,
        )

    async def delete(self, rtb_id):
        """
        Delete the specified rtb
        @param rtb_id: id of the route table for the deletion
        @type rtb_id: int
        @return: none
        @rtype: none
        """
        self.client.delete_route_table(
            RouteTableId=rtb_id,
        )

    async def create_route_igw(self, rtb_id, cidr_block, gateway_id):
        """
        Create route with a gateway
        @param rtb_id: id of the route table to use it to create route
        @type rtb_id: int
        @param cidr_block: IPv4 CIDR block for the route
        @type cidr_block: str
        @param gateway_id: id of gateway to attach it to the route
        @type gateway_id: int
        @return: none
        @rtype: none
        """
        self.client.create_route(
            DestinationCidrBlock=cidr_block,
            RouteTableId=rtb_id,
            GatewayId=gateway_id,
        )

    async def describe(self, rtb_tag_name):
        """
        Describe a specified route table using the name
        @param rtb_tag_name: name of the route table
        @type rtb_tag_name: str
        @return: Route table properties
        @rtype: array
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
        Check if the specified route table using the name exists
        @param rtb_tag_name: name of the route table
        @type rtb_tag_name: str
        @return: Boolean
        @rtype: bool
        """
        return True if await self.get_rtb_id(rtb_tag_name) else False

    async def get_assoc_id(self, rtb_tag_name):
        """
        Get the association id
        @param rtb_tag_name: name of the route table
        @type rtb_tag_name: str
        @return: Id of the association
        @rtype: int
        @raise: exception when the route table doesnt exists
        """
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["Associations"][0]["RouteTableAssociationId"]
        except IndexError:
            raise rtb_exception.RtbDoesntExists

    async def get_rtb_id(self, rtb_tag_name):
        """
        Get the route table id
        @param rtb_tag_name: name of the route table
        @type rtb_tag_name: str
        @return: Id of the route table
        @rtype: int
        @raise: exception when the route table doesnt exists
        """
        response = await self.describe(rtb_tag_name)
        try:
            return response['RouteTables'][0]["RouteTableId"]
        except IndexError:
            raise rtb_exception.RtbDoesntExists

    async def get_main_rtb_id_from_vpc(self, vpc_id):
        """
        Get the main route table id attached to a specified vpc
        @param vpc_id: id of the vpc
        @type vpc_id: int
        @return: Id of the main route table
        @rtype: int
        @raise: exception when the route table doesnt exists
        """
        main_route_table = self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id', 'Values': [vpc_id]
                },
                {
                    'Name': 'association.main', 'Values': ["true"]

                }
            ])
        try:
            return main_route_table['RouteTables'][0]['Associations'][0]['RouteTableId']
        except IndexError:
            raise rtb_exception.RtbDoesntExists
