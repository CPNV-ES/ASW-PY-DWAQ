import unittest

import src.aws_internet_gateway_manager as igw_manager
import src.aws_vpc_manager as vpc_manager


class IntegrationTestAwsIgwManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """
        Setup test internet gateway properties and instantiate the internet gateway manager
        + Setup test vpc properties and instantiate the vpc manager
        :return:
        """
        self.__igw_manager = igw_manager.AwsInternetGatewayManager()
        self.__vpc_manager = vpc_manager.AwsVpcManager()
        self.__igw_tag_name =
        # TODO VPC must be created only one time. Take a look on "SetupClass" mechanism
        self.__vpc_tag_name = "IGW_VPC_INTEGRATION_TEST"
        self.__cidr_block = "10.0.0.0/16"

    async def test_scenari_nominal_case_success(self):
        """
        This test method creates an internet gateway and a vpc
        Then attaches the gateway to the vpc
        This is the nominal case because all parameters are correctly set.
        :return: The return type is mandatory when using async Task test method
        """
        # Test internet gateway creation
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        self.assertTrue(await self.__igw_manager.exists(self.__igw_tag_name))

        # Test vpc creation
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        self.assertTrue(await self.__vpc_manager.exists(self.__vpc_tag_name))

        # Test attach internet gateway to vpc
        attached_vpc_id = await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        current_vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)
        self.assertEqual(attached_vpc_id, current_vpc_id)

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)
        await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)

        # TODO VPC must be deleted only one time. Take a look on "TearDownClass" mechanism
        await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)

if __name__ == '__main__':
    unittest.main()
