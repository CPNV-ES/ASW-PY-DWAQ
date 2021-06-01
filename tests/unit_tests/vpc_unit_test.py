import unittest

import src.aws_vpc_manager as aws_m

from src.exception.vpc_exception import VpcNameAlreadyExists


class UnitTestAwsVpcManager(unittest.IsolatedAsyncioTestCase):
    """
    This test class validates the good behavior of the VpcManager class
    """

    def setUp(self):
        """
        Setup test vpc properties and instantiate the vpc manager
        """
        self.__profile_name = "VIR1_INFRA_DEPLOYMENT"
        self.__region_end_point = "ap-south-1"
        self.__vpc_manager = aws_m.AwsVpcManager()
        self.__vpc_tag_name = "VIR1_SCRUMMASTER"
        self.__cidr_block = "10.0.0.0/16"

    async def test_create_vpc_nominal_case_success(self):
        """
        This test method tests the vpc creation action.
        This is the nominal case (all parameters are correctly set).
        :return: The return type is mandatory when using async Task test method
        """
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)

        self.assertTrue(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def test_create_vpc_already_exists_throw_exception(self):
        """
        This test method tests the vpc creation action.
        We expected the exception "VpcAlreadyExists".
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        # when

        # then : Exception must be thrown
        with self.assertRaises(VpcNameAlreadyExists):
            await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)

    async def test_delete_vpc_nominal_case_success(self):
        """
        This test method tests the vpc deletion action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        # when
        await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)
        # then
        self.assertFalse(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def test_exists_vpc_nominal_case_success(self):
        """
        This test method tests the exist action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        # when
        # then
        self.assertTrue(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        if await self.__vpc_manager.exists(self.__vpc_tag_name):
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
