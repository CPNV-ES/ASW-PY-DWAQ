from abc import ABC, abstractmethod


class IIgwManager(ABC):
    @abstractmethod
    def create_internet_gateway(self, igw_tag_name):
        pass

    @abstractmethod
    def internet_gateway_exists(self, igw_tag_name):
        pass

    @abstractmethod
    def delete_internet_gateway(self, igw_tag_name):
        pass

    @abstractmethod
    def attach_internet_gateway_to_vpc(self, igw_tag_name, vpc_tag_name):
        pass

    @abstractmethod
    def detach_internet_gateway_from_vpc(self, igw_tag_name):
        pass
