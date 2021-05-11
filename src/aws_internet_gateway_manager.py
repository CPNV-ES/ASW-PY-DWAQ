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
