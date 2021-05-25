import unittest

import src.aws_rtb_manager as vpc_m
import src.aws_rtb_manager as rtb_m

import src.exception.rtb_exception as rtb_exception


class UnitTestAwsVpcManager(unittest.IsolatedAsyncioTestCase):
    """
    This test class validates the good behavior of the VpcManager class
    """

    async def setUp(self):
        """
        Setup test vpc properties and instantiate the vpc manager
        """
        self.__rtb_tag_name = "RTB_UNIT_TEST"
        self.__rtb_manager = rtb_m.AwsRtbManager()
        self.__rtb_id = None
        self.__vpc_id = "vpc-08cbe426abe1bdb8e"
        self.__subnet_id = "subnet-0007f8fa46bd64863"
        self.__igw_id = "igw-01c180d79312e77bd"
        self.__igw_cidr_block = "0.0.0.0/0"

    async def asyncSetUp(self):
        self.__rtb_id = await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name)

    async def test_create_rtb_nominal_case_success(self):
        """
        This test method tests the vpc creation action.
        This is the nominal case (all parameters are correctly set).
        :return: The return type is mandatory when using async Task test method
        """
        await self.__rtb_manager.create(self.__rtb_tag_name, self.__vpc_id)
        self.assertTrue(await self.__rtb_manager.exists(self.__rtb_tag_name))

    async def test_associate_subnet_nominal_case_success(self):
        """
        This test method tests the vpc creation action.
        This is the nominal case (all parameters are correctly set).
        :return: The return type is mandatory when using async Task test method
        """
        await self.__rtb_manager.associate(await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name), self.__subnet_id)
        self.assertTrue(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))
        await self.__rtb_manager.disassociate(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))

    async def test_disassociate_subnet_nominal_case_success(self):
        await self.__rtb_manager.associate(await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name), self.__subnet_id)
        await self.__rtb_manager.disassociate(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))
        self.assertFalse(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))

    async def test_create_route_igw_nominal_case_success(self):
        await self.__rtb_manager.create_route_igw(self.__rtb_id, self.__igw_cidr_block, self.__igw_id)
        answer = await self.__rtb_manager.describe(self.__rtb_tag_name)
        self.assertTrue(answer['RouteTables'][0]["Routes"][1])


if __name__ == '__main__':
    unittest.main()
