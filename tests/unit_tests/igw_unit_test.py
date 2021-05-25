import unittest
import src.aws_internet_gateway_manager as igw_manager
import src.aws_vpc_manager as vpc_manager


class MyTestAwsIgwManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """
        Setup test internet gateway properties and instantiate the internet gateway manager
        + Setup test vpc properties and instantiate the vpc manager
        :return:
        """
        self.__igw_manager = igw_manager.AwsInternetGatewayManager()
        self.__vpc_manager = vpc_manager.AwsVpcManager()
        self.__igw_tag_name = "IGW_UNIT_TEST"
        self.__vpc_tag_name = "IGW_VPC_UNIT_TEST"
        self.__cidr_block = "10.0.0.0/16"

    async def test_create_igw_nominal_case_success(self):
        """
        This test method tests the internet gateway creation action.
        This is the nominal case (all parameters are correctly set).
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)

        self.assertTrue(await self.__igw_manager.exists(self.__igw_tag_name))

    async def test_create_igw_already_exists_throw_exception(self):
        """
        This test method tests the internet gateway creation action.
        We expected the exception "IgwAlreadyExists".
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)

        with self.assertRaises(Exception):
            await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)

    async def test_exists_igw_nominal_case_success(self):
        """
        This test method tests the exist action.
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)

        self.assertTrue(await self.__igw_manager.exists(self.__igw_tag_name))

    async def test_does_not_exist_igw_nominal_case_success(self):
        """
        This test method tests the does not exist action.
        :return:
        """
        self.assertFalse(await self.__igw_manager.exists(self.__igw_tag_name))

    async def test_delete_igw_nominal_case_success(self):
        """
        This test method tests the internet gateway deletion action.
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)

        self.assertFalse(await self.__igw_manager.exists(self.__igw_tag_name))

    async def test_delete_igw_does_not_exist_throw_exception(self):
        """
        This test method tests the internet gateway deletion action.
        We expected the exception "IgwDoesNotExists".
        :return:
        """
        with self.assertRaises(Exception):
            await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)

    async def test_attach_igw_to_vpc_nominal_case_success(self):
        """
        This test method tests the internet gateway attach action.
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        attached_vpc_id = await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        current_vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)

        self.assertEqual(attached_vpc_id, current_vpc_id)

        await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)

    async def test_igw_already_attached_to_vpc_throw_exception(self):
        """
        This test method tests the internet gateway attach action.
        We expected the exception "IgwAlreadyAttached".
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)

        with self.assertRaises(Exception):
            await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)

        await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)

    async def test_detach_igw_from_vpc_nominal_case_success(self):
        """
        This test method tests the internet gateway detach action.
        We expected the exception "IgwNotAttached".
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        detached_vpc_id = await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)
        current_vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)

        self.assertEqual(detached_vpc_id, current_vpc_id)

    async def test_detach_unattached_igw_from_vpc_throw_exception(self):
        """
        This test method tests the internet gateway detach action.
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)

        with self.assertRaises(Exception):
            await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)

    async def test_igw_id_nominal_case_success(self):
        """
        This test method tests the internet gateway get id action.
        We expected the exception "IgwDoesNotExist".
        :return:
        """
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        self.assertTrue(await self.__igw_manager.internet_gateway_id(self.__igw_tag_name))

    async def test_igw_id_does_not_exist_nominal_case_success(self):
        """
        This test method tests the internet gateway get id action.
        :return:
        """
        with self.assertRaises(Exception):
            await self.__igw_manager.internet_gateway_id(self.__igw_tag_name)

    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        if await self.__igw_manager.exists(self.__igw_tag_name):
            await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)

        if await self.__vpc_manager.exists(self.__vpc_tag_name):
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
