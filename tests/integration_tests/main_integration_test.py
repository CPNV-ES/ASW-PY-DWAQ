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
        self.__main_rtb_id = None
        self.__vpc_id = None
        self.__private_subnet_id = None
        self.__public_subnet_id = None
        self.__igw_id = None

    async def test_scenario_nominal_case_success(self):
        # Create the VPC
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, "10.0.0.0/16")
        self.__vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)
        self.__main_rtb_id = await self.__rtb_manager.get_main_rtb_id_from_vpc(self.__vpc_id)

        # Create the public subnet "10.0.0.0/24"
        await self.__subnet_manager.create_subnet(self.__public_subnet_tag_name, "10.0.0.0/24", self.__vpc_id)
        self.__public_subnet_id = await self.__subnet_manager.subnet_id(self.__public_subnet_tag_name)

        # Create the private subnet "10.0.1.0/24"
        await self.__subnet_manager.create_subnet(self.__private_subnet_tag_name, "10.0.1.0/24", self.__vpc_id)
        self.__private_subnet_id = await self.__subnet_manager.subnet_id(self.__private_subnet_tag_name)

        # Create the Internet Gateway and attach it to the vpc
        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        self.__igw_id = await self.__igw_manager.internet_gateway_id(self.__igw_tag_name)

        # Create the route table for the internet gateway
        await self.__rtb_manager.create(self.__rtb_tag_name, self.__vpc_id)
        self.__rtb_id = await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name)
        self.assertTrue(await self.__rtb_manager.exists(self.__rtb_tag_name))

        # Associate subnets to the corresponding routes tables
        await self.__rtb_manager.associate(self.__main_rtb_id, self.__private_subnet_id)
        await self.__rtb_manager.associate(self.__rtb_id, self.__public_subnet_id)

        # Create the IGW route
        await self.__rtb_manager.create_route_igw(self.__rtb_id, "0.0.0.0/0", self.__igw_id)


if __name__ == '__main__':
    unittest.main()
