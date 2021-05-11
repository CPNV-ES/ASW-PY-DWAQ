class AwsVpcManager():
    # AmazonEc2Client
    __client = None
    # Vpcs list
    __vpcs = None

    def __init__(self, aws_profile_name, aws_region_end_point):
        pass

    async def create_vpc(self, vpc_tag_name, cidr_block):
        """Create a new vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        cidr_block : string
            The primary IPv4 CIDR block for the VPC
        """
        pass

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
