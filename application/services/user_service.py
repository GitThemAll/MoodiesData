from domains.authetication.repositories import UserRepository
from infra.repositories.users_database import db, UserDB
from application.dto.user_dto import User
from sqlalchemy.exc import IntegrityError

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # Convert UserDB (ORM) to User (domain)
    def to_domain(user_db: UserDB) -> User:
        return User(id=user_db.id, username=user_db.username, email=user_db.email)

    # Service: Get all users
    def get_all_users(self) -> list[User]:
        user_dbs = UserDB.query.all()
        return [self.to_domain(u) for u in user_dbs]

    def create_user_with_password(self, username, email, password) -> User:
        user = UserDB(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
            return User(id=user.id, username=user.username, email=user.email)
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User already exists")

    def login_user(self, email, password) -> User | None:
        user = UserDB.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return User(id=user.id, username=user.username, email=user.email)
        return None

#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository

#     def get_user(self, user_id: int):
#         return self.user_repository.get_user_by_id(user_id)