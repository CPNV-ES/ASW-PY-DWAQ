import boto3
from src.aws_vpc_manager import AwsVpcManager


class AwsInternetGatewayManager:
    def __init__(self):
        self.client = boto3.client("ec2")
        self.resource = boto3.resource("ec2")

    async def create_internet_gateway(self, tag_name):
        """
        Create a new internet gateway
        :param tag_name:
        :return:
        """
        if await self.exists(tag_name):
            raise Exception("The specified internet gateway already exist")
        else:
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
        :param tag_name:
        :return:
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
        :param tag_name:
        :return:
        """
        if await self.exists(tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [tag_name]}]
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))

            self.resource.InternetGateway(igws_list[0].id).delete()
        else:
            raise Exception("The specified internet gateway does not exist")

    async def attach_to_vpc(self, igw_tag_name, vpc_tag_name):
        """
        Attach the specified internet gateway to the specified vpc
        :param igw_tag_name:
        :param vpc_tag_name:
        :return:
        """
        if await self.exists(igw_tag_name):
            vpc_manager = AwsVpcManager(None, None)

            if await vpc_manager.exists(vpc_tag_name):
                filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
                igws_list = list(self.resource.internet_gateways.filter(Filters=filter))
                vpc_id = await vpc_manager.vpc_id(vpc_tag_name)

                try:
                    self.resource.InternetGateway(igws_list[0].id).attach_to_vpc(VpcId=vpc_id)
                    return vpc_id
                except Exception:
                    raise Exception("The specified internet gateway is already attached")
            else:
                raise Exception("The specified vpc does not exist")
        else:
            raise Exception("The specified internet gateway does not exist")

    async def detach_from_vpc(self, igw_tag_name):
        """
        Detach the specified internet gateway from the vpc
        :param igw_tag_name:
        :return:
        """
        if await self.exists(igw_tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))

            try:
                attached_vpc_id = self.resource.InternetGateway(igws_list[0].id).attachments[0]["VpcId"]
                self.resource.InternetGateway(igws_list[0].id).detach_from_vpc(VpcId=attached_vpc_id)
                return attached_vpc_id
            except IndexError:
                raise Exception("The specified internet gateway is not attached to any vpc")
        else:
            raise Exception("The specified internet gateway does not exist")

    async def internet_gateway_id(self, igw_tag_name):
        if await self.exists(igw_tag_name):
            filter = [{'Name': 'tag:Name', 'Values': [igw_tag_name]}]
            igws_list = list(self.resource.internet_gateways.filter(Filters=filter))
            return igws_list[0].id
        raise Exception("The specified internet gateway does not exist")
