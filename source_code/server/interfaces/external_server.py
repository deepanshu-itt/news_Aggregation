from abc import ABC, abstractmethod


class IExternalServer(ABC):

    @abstractmethod
    def create(self, name, api_key, base_url, status='active'):
        pass


    @abstractmethod
    def find_by_id(self, server_id):
        pass


    @abstractmethod
    def find_by_name(self, name):
        pass


    @abstractmethod
    def get_all(self):
        pass


    @abstractmethod
    def update_status(self, server_id, status, new_api_key=None):
        pass


    @abstractmethod
    def update_last_accessed(self, server_id):
        pass
