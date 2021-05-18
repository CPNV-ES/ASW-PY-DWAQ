import boto3


class AwsInternetGatewayManager:
    def __init__(self, aws_profile_name, aws_region_end_point):
        self.aws_profile_name = aws_profile_name
        self.aws_region_end_point = aws_region_end_point
        self.client = boto3.client("ec2")
        self.resource = boto3.resource("ec2")

    async def create_internet_gateway(self, tag_name):
        """Create a new internet gateway

        Parameters
        ----------
        tag_name : string
            The name of the internet gateway
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
