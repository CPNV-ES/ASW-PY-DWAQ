import asyncio
from AwsVpcManager import AwsVpcManager


aws_vpc_manager = AwsVpcManager("", "")
asyncio.run(aws_vpc_manager.exists(""))

