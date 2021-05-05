from abc import ABC, abstractmethod


class IVpcManager(ABC):
    @abstractmethod
    def create_vpc(self, vpc_tag_name, cidr_block):
        pass

    @abstractmethod
    def delete_vpc(self, vpc_tag_name):
        pass

    @abstractmethod
    def exists(self, vpc_tag_name):
        pass
