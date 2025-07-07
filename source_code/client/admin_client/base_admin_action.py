from abc import ABC, abstractmethod

class IAdminAction(ABC):
    def __init__(self, api_client, get_current_user):
        self.api_client = api_client
        self.get_current_user = get_current_user

    @abstractmethod
    def execute(self):
        pass
