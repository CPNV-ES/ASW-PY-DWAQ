import unittest

import src.aws_vpc_manager as vpc_m
import src.aws_rtb_manager as rtb_m
import src.aws_internet_gateway_manager as igw_m
import src.aws_subnet_manager as subnet_m

import src.exception.rtb_exception as rtb_exception


class IntegrationTestAwsRtbManager(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.__rtb_tag_name = "RTB_INTEGRATION_TEST"
        self.__vpc_tag_name = "VPC_INTEGRATION_TEST"
        self.__subnet_tag_name = "SUBNET_INTEGRATION_TEST"
        self.__igw_tag_name = "IGW_INTEGRATION_TEST"

        self.__rtb_manager = rtb_m.AwsRtbManager()
        self.__vpc_manager = vpc_m.AwsVpcManager()
        self.__subnet_manager = subnet_m.AwsSubnetManager()
        self.__igw_manager = igw_m.AwsInternetGatewayManager()

        self.__rtb_id = None
        self.__vpc_id = None
        self.__subnet_id = None
        self.__igw_id = None
        self.__igw_cidr_block = "0.0.0.0/0"

    async def asyncSetUp(self):
        await self.__vpc_manager.create_vpc(self.__vpc_tag_name, "10.0.0.0/16")
        self.__vpc_id = await self.__vpc_manager.vpc_id(self.__vpc_tag_name)

        await self.__subnet_manager.create_subnet(self.__subnet_tag_name, "10.0.0.0/24", self.__vpc_id)
        self.__subnet_id = await self.__subnet_manager.subnet_id(self.__subnet_tag_name)

        await self.__igw_manager.create_internet_gateway(self.__igw_tag_name)
        await self.__igw_manager.attach_to_vpc(self.__igw_tag_name, self.__vpc_tag_name)
        self.__igw_id = await self.__igw_manager.internet_gateway_id(self.__igw_tag_name)

    async def test_scenario_nominal_case_success(self):

        # Create the route table
        await self.__rtb_manager.create(self.__rtb_tag_name, self.__vpc_id)
        self.__rtb_id = await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name)
        self.assertTrue(await self.__rtb_manager.exists(self.__rtb_tag_name))

        # Associate subnet to route table
        await self.__rtb_manager.associate(await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name), self.__subnet_id)
        self.assertTrue(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))

        # Disassociate the subnet
        await self.__rtb_manager.disassociate(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))
        self.assertFalse(await self.__rtb_manager.get_assoc_id(self.__rtb_tag_name))

        # Create route with Internet Gateway
        await self.__rtb_manager.create_route_igw(self.__rtb_id, self.__igw_cidr_block, self.__igw_id)
        answer = await self.__rtb_manager.describe(self.__rtb_tag_name)
        self.assertTrue(answer['RouteTables'][0]["Routes"][1])

        # Delete route table
        await self.__igw_manager.detach_from_vpc(self.__igw_tag_name)
        await self.__igw_manager.delete_internet_gateway(self.__igw_tag_name)
        await self.__subnet_manager.delete_subnet(self.__subnet_tag_name)
        await self.__rtb_manager.delete(self.__rtb_id)
        self.assertFalse(await self.__rtb_manager.get_rtb_id(self.__rtb_tag_name))

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
