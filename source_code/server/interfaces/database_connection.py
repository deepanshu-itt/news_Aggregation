from abc import ABC, abstractmethod
from dto.cursor_dto import CursorDto
class IDatabaseConnection(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def execute_query(self, cursor_params: CursorDto):
        pass