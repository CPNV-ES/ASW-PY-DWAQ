import unittest

import src.aws_subnet_manager as subnet_manager
import src.aws_vpc_manager as vpc_manager
import src.exception.subnet_exception as subnet_exception


class UnitTestAwsSubnetManager(unittest.IsolatedAsyncioTestCase):
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

        self.__subnet_manager = subnet_manager.AwsSubnetManager(self.__profile_name, self.__region_end_point)
        self.__subnet_tag_name = "test_subnet"
        self.__subnet_cidr_block = "10.0.2.0/24"

        self.__vpc_manager = vpc_manager.AwsVpcManager(self.__profile_name, self.__region_end_point)
        self.__vpc_tag_name = "vpc_test_subnet"
        self.__vpc_cidr_block = "10.0.0.0/16"

    async def asyncSetUp(self):
        """
        Setup a new vpc
        """
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__vpc_cidr_block)
        self.__vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)

    async def test_create_subnet_nominal_case_success(self):
        """
        This test method tests the subnet creation action.
        This is the nominal case (all parameters are correctly set).
        :return: The return type is mandatory when using async Task test method
        """
        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)
        self.assertTrue(await self.__subnet_manager.exists(self.__subnet_tag_name))

    async def test_create_subnet_already_exists_throw_exception(self):
        """
        This test method tests the subnet creation action.
        We expected the exception "SubnetAlreadyExists".
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)
        # when
        with self.assertRaises(subnet_exception.SubnetNameAlreadyExists):
            await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)
        # then : Exception must be thrown

    async def test_delete_subnet_nominal_case_success(self):
        """
        This test method tests the subnet deletion action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)
        # when
        await self.__subnet_manager.delete_subnet(self.__subnet_tag_name)

        # then
        self.assertFalse(await self.__subnet_manager.exists(self.__subnet_tag_name))

    async def test_exists_subnet_nominal_case_success(self):
        """
        This test method tests the exist action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, self.__subnet_cidr_block, self.__vpc_id)
        # when
        result = await self.__subnet_manager.exists(self.__subnet_tag_name)
        # then
        self.assertTrue(result)

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
