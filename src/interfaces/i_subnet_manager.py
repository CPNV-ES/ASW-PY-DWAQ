from abc import ABC, abstractmethod


class ISubnetManager(ABC):
    @abstractmethod
    def create_subnet(self, tag_name, cidr_block, vpc_id):
        pass

    @abstractmethod
    def delete_subnet(self, tag_name):
        pass

    @abstractmethod
    def exists(self, tag_name):
        pass

    @abstractmethod
    def get_id(self, tag_name):
        pass
