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

        if not await self.exists(vpc_tag_name):
            vpc = self.client.create_vpc(CidrBlock=cidr_block)
            vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_tag_name}])
            vpc.wait_until_available()
        else:
            print("Vpc " + vpc_tag_name + " already exists")

    async def delete_vpc(self, vpc_tag_name):
        """Delete a vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """

        if await self.exists(vpc_tag_name):
            self.client.delete_vpc()
        else:
            print("Vpc " + vpc_tag_name + " does not exists")

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

        if await self.__vpc_id(vpc_tag_name):
            return True

        return False

    async def describe_vpcs(self):
        """Retrieve the values of the vpc attributes
        """
        pass

    async def __vpc_id(self, vpc_tag_name):
        """Get the vpc id

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """

        filter = [{'Name': 'tag:Name', 'Values': [vpc_tag_name]}]
        vpcs_list = list(self.client.vpcs.filter(Filters=filter))

        if vpcs_list:
            return vpcs_list[0].id

        return False
