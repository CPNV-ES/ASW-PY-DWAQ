from abc import ABC, abstractmethod


class IRtbManager(ABC):
    @abstractmethod
    def create_rtb(self, rtb_tag_name, vpc_id):
        pass

    @abstractmethod
    def associate_rtb(self, rtb_id, subnet_id):
        pass

    @abstractmethod
    def disassociate_rtb(self, association_id):
        pass

    @abstractmethod
    def delete_rtb(self, rtb_id):
        pass

    @abstractmethod
    def rtb_exists(self, rtb_tag_name):
        pass

    @abstractmethod
    def create_route(self, rtb_id, cidr_block, gateway_id):
        pass

    @abstractmethod
    def describe_rtb(self, rtb_tag_name):
        pass
