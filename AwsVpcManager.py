class AwsVpcManager:

    def __init__(self, aws_profile_name, aws_region_end_point):
        pass

    def create_vpc(self, vpc_tag_name, cidr_block):
        """Create a new vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        cidr_block : string
            Range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block;
            for example, 10.0. 0.0/16 . This is the primary CIDR block for your VPC.
        """
        pass

    def delete_vpc(self, vpc_tag_name):
        """Delete a vpc

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        pass

    def exists(self, vpc_tag_name):
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

    def __describe_vpcs(self):
        """Describe a vpc
        """
        pass

    def __vpc_id(self, vpc_tag_name):
        """Get the vpc id

        Parameters
        ----------
        vpc_tag_name : string
            The name of the vpc
        """
        pass
