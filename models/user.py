import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str) -> object:
        # self.id = _id implicit created
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> object:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> object:
        return cls.query.filter_by(id=_id).first()
    """
    @jwt_required()
    def get(self) -> JsonType:
        user = current_identity
        print(user)
        return {'test'}
    """
