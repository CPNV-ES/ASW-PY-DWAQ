from abc import ABC, abstractmethod


class IVpcManager(ABC):
    @abstractmethod
    def create_vpc(self, tag_name, cidr_block):
        pass

    @abstractmethod
    def delete_vpc(self, tag_name):
        pass

    @abstractmethod
    def exists(self, tag_name):
        pass

    @abstractmethod
    def get_id(self, tag_name):
        pass
