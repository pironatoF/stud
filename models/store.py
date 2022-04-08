from db import db
from typing import Union, Dict, List, Any, Type
JsonType = Union[Dict[str, Any], List[Any],
                 int, str, float, bool, Type[None]]


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price):
        # self.id = _id implicit creation
        self.name = name

    def json(self) -> JsonType:
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name: str) -> object:
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()