from abc import ABC, abstractmethod


class IIgwManager(ABC):
    @abstractmethod
    def create_internet_gateway(self, tag_name):
        pass

    @abstractmethod
    def exists(self, tag_name):
        pass

    @abstractmethod
    def delete_internet_gateway(self, tag_name):
        pass

    @abstractmethod
    def attach_to_vpc(self, igw_tag_name, vpc_tag_name):
        pass

    @abstractmethod
    def detach_from_vpc(self, tag_name):
        pass

    @abstractmethod
    def get_id(self, tag_name):
        pass
