from domains.authetication.usermodel import User
from domains.authetication.repositories import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {
            1: User(1, "Alice", "alice@example.com"),
            2: User(2, "Bob", "bob@example.com")
        }

    def get_user_by_id(self, user_id: int) -> User:
        return self.users.get(user_id)