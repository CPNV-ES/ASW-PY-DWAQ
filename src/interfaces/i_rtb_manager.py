from abc import ABC, abstractmethod


class IRtbManager(ABC):
    @abstractmethod
    def create(self, rtb_tag_name, vpc_id):
        pass

    @abstractmethod
    def associate(self, rtb_id, subnet_id):
        pass

    @abstractmethod
    def disassociate(self, association_id):
        pass

    @abstractmethod
    def delete(self, rtb_id):
        pass

    @abstractmethod
    def create_route(self, rtb_id, cidr_block, gateway_id, local_gateway_id):
        pass

    @abstractmethod
    def describe(self, rtb_tag_name):
        pass

