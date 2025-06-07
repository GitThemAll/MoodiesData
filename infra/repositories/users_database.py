from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from application.dto.user_dto import User

db = SQLAlchemy()

class UserDB(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add(self, user: User):
        user_db = UserDB(username=user.username, email=user.email)
        user_db.set_password(user.password)
        db.session.add(user_db)
        db.session.commit()

    def find_by_email(self, email: str) -> User | None:
        user_db = UserDB.query.filter_by(email=email).first()
        if not user_db:
            return None
        return User(id=user_db.id, username=user_db.username, email=user_db.email)

    def get_user_by_id(self, user_id: int) -> User | None:
        user_db = UserDB.query.get(user_id)
        if not user_db:
            return None
        return User(id=user_db.id, username=user_db.username, email=user_db.email)
