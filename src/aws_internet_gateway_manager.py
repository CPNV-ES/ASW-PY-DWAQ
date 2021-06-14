import boto3
from src.aws_vpc_manager import AwsVpcManager
import src.exception.vpc_exception as vpc_exception
import src.exception.igw_exception as igw_exception


class AwsInternetGatewayManager:

    def __init__(self):
        # TODO DRY principle not respected, those items can be centralized
        self.client = boto3.client("ec2", use_ssl=False)
        self.resource = boto3.resource("ec2", use_ssl=False)

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
            raise igw_exception.IgwNameAlreadyExists
        else:
            # TODO, DRY -> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.add_tags_to_resource
            self.client.create_internet_gateway(
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
        igws_list = list(self.resource.internet_gateways.filter(Filters=filter))

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
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))

            self.resource.InternetGateway(igws_list[0].id).delete()
        else:
            raise igw_exception.IgwNameDoesNotExist

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
                igws_list = list(self.resource.internet_gateways.filter(Filters=filter))
                vpc_id = await vpc_manager.vpc_id(vpc_tag_name)

                try:
                    self.resource.InternetGateway(igws_list[0].id).attach_to_vpc(VpcId=vpc_id)
                    return vpc_id
                except Exception:
                    raise igw_exception.IgwAlreadyAttached
            else:
                raise vpc_exception.VpcNameDoesNotExist
        else:
            raise igw_exception.IgwNameDoesNotExist

    async def detach_from_vpc(self, igw_tag_name):
        """
        Detach the specified internet gateway from the vpc
        @param igw_tag_name: name of the internet gateway
        @type igw_tag_name: str
        @return: attached vpc id
        @rtype: int
        @raise: exception when the specified internet gateway does not exist
        @raise: exception when the specified internet gateway is not attached
        """
        if await self.exists(igw_tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))

            try:
                attached_vpc_id = self.resource.InternetGateway(igws_list[0].id).attachments[0]["VpcId"]
                self.resource.InternetGateway(igws_list[0].id).detach_from_vpc(VpcId=attached_vpc_id)
                return attached_vpc_id
            except IndexError:
                raise igw_exception.IgwNotAttached
        else:
            raise igw_exception.IgwNameDoesNotExist

    # TODO must be a private method (__), what do you think ?
    async def internet_gateway_id(self, igw_tag_name):
        """
        Get the id of the specified internet gateway
        @param igw_tag_name: name of the internet gateway
        @type igw_tag_name: str
        @return: id of the internet gateway
        @rtype: int
        @raise: exception when the specified internet gateway does not exist
        """
        if await self.exists(igw_tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))
            return igws_list[0].id
        raise igw_exception.IgwNameDoesNotExist
