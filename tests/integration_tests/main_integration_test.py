import unittest

import src.aws_vpc_manager as vpc_m
import src.aws_rtb_manager as rtb_m
import src.aws_internet_gateway_manager as igw_m
import src.aws_subnet_manager as subnet_m

import src.exception.rtb_exception as rtb_exception


class IntegrationTestAwsRtbManager(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.__vpc_tag_name = "VPC_INTEGRATION_TEST"
        self.__rtb_tag_name = "RTB_PUBLIC_SUBNET_INTEGRATION_TEST"
        self.__private_subnet_tag_name = "PRIVATE_SUBNET_INTEGRATION_TEST"
        self.__public_subnet_tag_name = "PUBLIC_SUBNET_INTEGRATION_TEST"
        self.__igw_tag_name = "IGW_INTEGRATION_TEST"

        self.__rtb_manager = rtb_m.AwsRtbManager()
        self.__vpc_manager = vpc_m.AwsVpcManager()
        self.__subnet_manager = subnet_m.AwsSubnetManager()
        self.__igw_manager = igw_m.AwsInternetGatewayManager()

        self.__rtb_id = None
        self.__vpc_id = None
        self.__private_subnet_id = None
        self.__public_subnet_id = None
        self.__igw_id = None
        self.__igw_cidr_block = "0.0.0.0/0"

    async def test_scenario_nominal_case_success(self):

        # Create the VPC
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, "10.0.0.0/16")
        self.__vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)

        # Create the private subnet "10.0.0.0/24"
        await self.__subnet_manager.create_subnet(self.__private_subnet_tag_name, "10.0.0.0/24", self.__vpc_id)
        self.__public_subnet_id = await self.__subnet_manager.subnet_id(self.__public_subnet_tag_name)

        # Create the private subnet "10.0.1.0/24"
        await self.__subnet_manager.create_subnet(self.__private_subnet_tag_name, "10.0.1.0/24", self.__vpc_id)
        self.__private_subnet_id = await self.__subnet_manager.subnet_id(self.__private_subnet_tag_name)

        # Create the Internet Gateway and attach it to the vpc
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        self.__igw_id = await self.__igw_manager.internet_gateway_id(self.__igw_tag_name)



    async def asyncTearDown(self):
        """
        This method is used to clean class properties after each test method
        """
        if await self.__igw_manager.exists(self.__igw_tag_name):
            await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)
            await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)

        if await self.__subnet_manager.exists(self.__subnet_tag_name):
            await self.__subnet_manager.delete_subnet(self.__subnet_tag_name)

        if await self.__rtb_manager.exists(self.__rtb_tag_name):
            await self.__rtb_manager.delete(self.__rtb_id)

        if await self.__vpc_manager.exists(self.__vpc_tag_name):
            await self.__vpc_manager.delete_vpc(self.__vpc_tag_name)


if __name__ == '__main__':
    unittest.main()
