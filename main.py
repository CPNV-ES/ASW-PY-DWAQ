import asyncio
from src.AwsVpcManager import AwsVpcManager


aws_vpc_manager = AwsVpcManager("", "")
asyncio.run(aws_vpc_manager.create_vpc("dylan", "10.0.0.0/24"))
