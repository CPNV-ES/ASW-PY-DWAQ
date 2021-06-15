import unittest

import src.aws_subnet_manager as subnet_manager
import src.aws_vpc_manager as vpc_manager


class IntegrationTestAwsSubnetManager(unittest.IsolatedAsyncioTestCase):
    """
    This test class validates the good behavior of the SubnetManager class
    """

    def setUp(self):
        """
        Setup test subnet properties and instantiate the subnet manager
        + Setup test vpc properties and instantiate the vpc manager
        """
        self.__profile_name = "VIR1_INFRA_DEPLOYMENT"
        self.__region_end_point = "ap-south-1"

        self.__subnet_manager = subnet_manager.AwsSubnetManager()
        self.__subnet_tag_name = "test_subnet"
        self.__subnet_cidr_block = "10.0.2.0/24"

        self.__vpc_manager = vpc_manager.AwsVpcManager()
        self.__vpc_tag_name = "vpc_test_subnet"
        self.__vpc_cidr_block = "10.0.0.0/16"

    async def asyncSetUp(self):
        """
        Setup a new vpc
        """
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__vpc_cidr_block)
        self.__vpc_id = await self.__vpc_manager.get_id(self.__vpc_tag_name)

    async def test_scenario_nominal_case_success(self):
        """
        This test method try to create a Subnet.
        This is the nominal case because all parameters are correctly set.
        :return: The return type is mandatory when using async Task test method
        """

        # Step 1  Create Subnet

        # given
        # refer to Setup Method

        # when
        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)

        # then
        self.assertTrue(await self.__subnet_manager.exists(self.__subnet_tag_name))

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        response_subnet = await self.__subnet_manager.exists(self.__subnet_tag_name)
        if response_subnet:
            await self.__subnet_manager.delete_subnet(self.__subnet_tag_name)

        response_vpc = await self.__vpc_manager.exists(self.__vpc_tag_name)
        if response_vpc:
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
