from abc import ABC, abstractmethod


class ISubnetManager(ABC):
    @abstractmethod
    def create_subnet(self, subnet_tag_name, cidr_block, vpc_id):
        pass

    @abstractmethod
    def delete_subnet(self, subnet_tag_name):
        pass

    @abstractmethod
    def exists(self, subnet_tag_name):
        pass
