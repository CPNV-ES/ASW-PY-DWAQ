import unittest
import asyncio

import src.aws_vpc_manager as aws_m


class IntegrationTestAwsVpcManager(unittest.IsolatedAsyncioTestCase):
    """
    This test class validates the good behavior of the VpcManager class
    """

    def setUp(self):
        """
        Setup test vpc properties and instantiate the vpc manager
        """
        self.__profile_name = "VIR1_INFRA_DEPLOYMENT"
        self.__region_end_point = "ap-south-1"
        self.__vpc_manager = aws_m.AwsVpcManager(self.__profile_name, self.__region_end_point)
        self.__vpc_tag_name = "VIR1_SCRUMMASTER"
        self.__cidr_block = "10.0.0.0/16"

    async def test_scenari_nominal_case_success(self):
        """
        This test method try to create a VPC.
        This is the nominal case because all parameters are correctly set.
        :return: The return type is mandatory when using async Task test method
        """

        # Step 1  Create VPC

        # given
        # refer to Setup Method

        # when
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)

        # then
        self.assertTrue(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        response = await self.__vpc_manager.exists(self.__vpc_tag_name)
        if response:
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
