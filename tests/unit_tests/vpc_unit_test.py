import unittest
import asyncio

import src.aws_vpc_manager as aws_m
import src.exception.vpc_exception


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
        self.__vpc_manager = aws_m.AwsVpcManager(self.__profile_name, self.__region_end_point)
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
        with self.assertRaises(src.exception.vpc_exception.VpcNameAlreadyExists):
            await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        # then : Exception must be thrown

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
        result = await self.__vpc_manager.exists(self.__vpc_tag_name)
        # then
        self.assertTrue(result)

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        response = await self.__vpc_manager.exists(self.__vpc_tag_name)
        if response:
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
