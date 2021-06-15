import boto3
from src.interfaces.i_rtb_manager import IRtbManager


class AwsRtbManager(IRtbManager):

    def __init__(self):
        # AmazonEc2Client
        self.client = boto3.client('ec2', use_ssl=False)
        self.resource = boto3.resource('ec2', use_ssl=False)

    async def create(self, tag_name, vpc_id):
        """
        Create the specified route table
        @param tag_name: name of the route table
        @type tag_name: str
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
                            'Value': tag_name
                        }]
                    }
                ]
            )
        except Exception:
            raise RtbAlreadyExists

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

    async def describe(self, tag_name):
        """
        Describe a specified route table using the name
        @param tag_name: name of the route table
        @type tag_name: str
        @return: Route table properties
        @rtype: array
        """
        return self.client.describe_route_tables(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [tag_name]
                }
            ],
        )

    async def exists(self, tag_name):
        """
        Check if the specified route table using the name exists
        @param tag_name: name of the route table
        @type tag_name: str
        @return: Boolean
        @rtype: bool
        """
        try:
            if await self.get_id(tag_name):
                return True
        except RtbDoesntExists:
            return False

    async def get_assoc_id(self, tag_name):
        """
        Get the association id
        @param tag_name: name of the route table
        @type tag_name: str
        @return: Id of the association
        @rtype: int
        @raise: exception when the route table doesnt exists
        """
        response = await self.describe(tag_name)
        if response['RouteTables'][0]["Associations"]:
            return response['RouteTables'][0]["Associations"][0]["RouteTableAssociationId"]
        else:
            raise RtbDoesntExists

    async def get_id(self, tag_name):
        """
        Get the route table id
        @param tag_name: name of the route table
        @type tag_name: str
        @return: Id of the route table
        @rtype: int
        @raise: exception when the route table doesnt exists
        """
        response = await self.describe(tag_name)
        if response['RouteTables']:
            return response['RouteTables'][0]["RouteTableId"]
        else:
            raise RtbDoesntExists

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
            raise RtbDoesntExists


class RtbAlreadyExists(Exception):
    def __init__(self, expression="RtbAlreadyExists", message="Rtb already exists!"):
        self.expression = expression
        self.message = message


class RtbDoesntExists(Exception):
    def __init__(self, expression="RtbDoesntExists", message="Rtb Doesnt exists!"):
        self.expression = expression
        self.message = message
