
from abc import ABC, abstractmethod
from domains.authetication.usermodel import User

#repository interface
class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass