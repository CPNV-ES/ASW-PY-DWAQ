import boto3


class AwsVpcManager:
    def __init__(self, aws_profile_name, aws_region_end_point):
        self.aws_profile_name = aws_profile_name
        self.aws_region_end_point = aws_region_end_point
        # AmazonEc2Client
        self.client = boto3.resource('ec2')
        # Vpcs list
        self.vpcs = None

    async def create_vpc(self, vpc_tag_name, cidr_block):
        """Create a new vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        cidr_block : string
            The primary IPv4 CIDR block for the VPC
        """

        vpc = self.client.create_vpc(CidrBlock=cidr_block)
        vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_tag_name}])
        vpc.wait_until_available()

    async def delete_vpc(self, vpc_tag_name):
        """Delete a vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        pass

    async def exists(self, vpc_tag_name):
        """Verify if the vpc exists

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc

        Returns
        -------
        Boolean : True if the vpc exists
        """
        return False
        pass

    async def __describe_vpcs(self):
        """Describe a vpc
        """
        pass

    async def __vpc_id(self, vpc_tag_name):
        """Get the vpc id

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        pass
