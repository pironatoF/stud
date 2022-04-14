from db import db
from typing import Union, Dict, List, Any, Type
JsonType = Union[Dict[str, Any], List[Any],
                 int, str, float, bool, Type[None]]


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        # self.id = _id implicit creation
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> JsonType:
        return {
            "id": self.id, "name": self.name, "price": self.price,
            "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name: str) -> object:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
