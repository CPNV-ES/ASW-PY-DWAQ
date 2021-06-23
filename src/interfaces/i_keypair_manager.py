from abc import ABC, abstractmethod


class IKeypairManager(ABC):
    @abstractmethod
    def create(self, name):
        pass

    @abstractmethod
    def exists(self, name):
        pass

    @abstractmethod
    def delete(self, id):
        pass