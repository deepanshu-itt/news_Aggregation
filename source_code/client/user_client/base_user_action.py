from abc import ABC, abstractmethod


class IUserAction(ABC):

    @abstractmethod
    def run(self,  *args, **kwargs):
        pass
