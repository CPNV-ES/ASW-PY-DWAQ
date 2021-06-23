from abc import ABC

from src.aws_manager import AwsManager
from src.aws_vpc_manager import AwsVpcManager
from src.interfaces.i_igw_manager import IIgwManager


class AwsInternetGatewayManager(IIgwManager, ABC, AwsManager):
    def __init__(self):
        AwsManager.__init__(self)

    async def create_internet_gateway(self, tag_name):
        """
        Create a new internet gateway
        @param tag_name: name of the internet gateway
        @type tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the specified internet gateway already exists
        """
        if await self.exists(tag_name):
            raise IgwNameAlreadyExists
        else:
            self._client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': tag_name
                            },
                        ]
                    },
                ]
            )

    async def exists(self, tag_name):
        """
        Define if the internet gateway exists or not
        @param tag_name: name of the internet gateway
        @type tag_name: str
        @return: true or false
        @rtype: bool
        @raise: return false when the index of the internet gateway list is out of range
        """
        filter = [{'Name': 'tag:Name', 'Values': [tag_name]}]
        igws_list = list(self._resource.internet_gateways.filter(Filters=filter))

        try:
            if igws_list[0].id:
                return True
        except IndexError:
            return False

    async def delete_internet_gateway(self, tag_name):
        """
        Delete the specified internet gateway
        @param tag_name: name of the internet gateway
        @type tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the specified internet gateway does not exist
        """
        if await self.exists(tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [tag_name]}]
            igws_list = list(self._resource.internet_gateways.filter(Filters=filter))

            self._resource.InternetGateway(igws_list[0].id).delete()
        else:
            raise IgwNameDoesNotExist

    async def attach_to_vpc(self, igw_tag_name, vpc_tag_name):
        """
        Attach the specified internet gateway to the specified vpc
        @param igw_tag_name: name of the internet gateway
        @type igw_tag_name: str
        @param vpc_tag_name: name of the vpc
        @type vpc_tag_name: str
        @return: none
        @rtype: none
        @raise: exception when the specified internet gateway does not exist
        @raise: exception when the specified vpc does not exist
        @raise: exception when the specified internet gateway is already attached
        """
        if await self.exists(igw_tag_name):
            vpc_manager = AwsVpcManager()

            if await vpc_manager.exists(vpc_tag_name):
                filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
                igws_list = list(self._resource.internet_gateways.filter(Filters=filter))
                vpc_id = await vpc_manager.get_id(vpc_tag_name)

                try:
                    self._resource.InternetGateway(igws_list[0].id).attach_to_vpc(VpcId=vpc_id)
                    return vpc_id
                except Exception:
                    raise IgwAlreadyAttached
            else:
                raise AwsVpcManager.VpcNameDoesNotExist
        else:
            raise IgwNameDoesNotExist

    async def detach_from_vpc(self, tag_name):
        """
        Detach the specified internet gateway from the vpc
        @param tag_name: name of the internet gateway
        @type tag_name: str
        @return: attached vpc id
        @rtype: int
        @raise: exception when the specified internet gateway does not exist
        @raise: exception when the specified internet gateway is not attached
        """
        if await self.exists(tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [tag_name]}]
            igws_list = list(self._resource.internet_gateways.filter(Filters=filter))

            try:
                attached_vpc_id = self._resource.InternetGateway(igws_list[0].id).attachments[0]["VpcId"]
                self._resource.InternetGateway(igws_list[0].id).detach_from_vpc(VpcId=attached_vpc_id)
                return attached_vpc_id
            except IndexError:
                raise IgwNotAttached
        else:
            raise IgwNameDoesNotExist

    async def get_id(self, tag_name):
        """
        Get the id of the specified internet gateway
        @param tag_name: name of the internet gateway
        @type tag_name: str
        @return: id of the internet gateway
        @rtype: int
        @raise: exception when the specified internet gateway does not exist
        """
        if await self.exists(tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [tag_name]}]
            igws_list = list(self._resource.internet_gateways.filter(Filters=filter))
            return igws_list[0].id
        raise IgwNameDoesNotExist


class IgwNameAlreadyExists(Exception):
    def __init__(self, expression="IgwNameAlreadyExists", message="Igw already exists!"):
        self.expression = expression
        self.message = message


class IgwNameDoesNotExist(Exception):
    def __init__(self, expression="IgwNameDoesNotExist", message="Igw doesn't exists!"):
        self.expression = expression
        self.message = message


class IgwAlreadyAttached(Exception):
    def __init__(self, expression="IgwAlreadyAttached", message="Igw is already attached!"):
        self.expression = expression
        self.message = message


class IgwNotAttached(Exception):
    def __init__(self, expression="IgwNotAttached", message="Igw is not attached to a vpc!"):
        self.expression = expression
        self.message = message
