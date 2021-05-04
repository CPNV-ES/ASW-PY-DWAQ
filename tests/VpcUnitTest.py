import unittest
import Exception

class UnitTestAwsVpcManager(unittest.TestCase):
    """This test class validates the good behavior of the VpcManager class
    """
    @classmethod
    def setUpClass(cls):
        """Setup test vpc properties and instantiate the vpc mnager
        """
        cls.__profile_name = "VIR1_INFRA_DEPLOYMENT"
        cls.__region_end_point = "ap-south-1"
        cls.__vpc_manager = new AwsVpcManager(cls.__profile_name, cls.__region_end_point)
        cls.__vpc_tag_name = "VIR1_SCRUMMASTER"
        cls.__cidr_block = "10.0.0.0/16"

    async def create_vpc_nominal_case_success(self):
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        self.assertTrue(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def create_vpc_already_exists_throw_exception(self):
        """
        This test method tests the vpc creation action.
        We expected the exception "VpcAlreadyExists".
        :return:The return type is mandatory when using async Task test method

        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, self.__cidr_block)
        # when
        with self.assertRaises(Exception.VpcNameAlreadyExists):
            await self.__vpc_manager.create_vpc(self.__vpc_tag_name,self.__cidr_block)
        # then : Exception must be thrown

    async def delete_vpc_nominal_case_success(self):
        """
        This test method tests the vpc deletion action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name,self.__cidr_block)
        # when
        await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)
        # then
        self.assertFalse(await self.__vpc_manager.exists(self.__vpc_tag_name))

    async def exists_vpc_nominal_case_success(self):
        """
        This test method tests the exist action.
        :return: The return type is mandatory when using async Task test method
        """
        # given
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name,self.__cidr_block)
        # when
        result = await self.__vpc_manager.exists(self.__vpc_tag_name)
        # then
        self.assertTrue(result)


    @classmethod
    async def tearDownClass(cls):
        """
        This method is used to clean class properties after each test method
        """
        if (await cls.__vpc_manager.exists(cls.__vpc_tag_name)):
            await cls.__vpc_manager.delete_vpc(cls.__vpc_tag_name)




