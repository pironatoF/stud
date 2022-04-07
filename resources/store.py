from models.store import StoreModel
from flask_jwt import jwt_required
from flask_restful import Resource  # , reqparse
from typing import Union, Dict, List, Any, Type
JsonType = Union[Dict[str, Any], List[Any],
                 int, str, float, bool, Type[None]]


class StoreList(Resource):
    def get(self) -> JsonType:
        stores = StoreModel.query.all()
        if stores:
            return {'stores': [store.json() for store in stores]}, 200
        return {'message': 'no stores'}, 404


class Store(Resource):

    @jwt_required
    def get(self, name: str) -> JsonType:
        store = StoreModel.find_by_name(name)
        if store:
            return {"store": store.json()}, 200
        return {'message': 'store not found'}, 404

    def post(self, name: str) -> JsonType:
        store = StoreModel.find_by_name(name)
        if store:
            return {
                'message': f"A store with name {store.name!r} already exist!"
                }, 400
        try:
            store = StoreModel(name)
            store.save()
        except:
            return {'message': "An error occurred inserting stores"}, 500
        return {"store": store.json()}, 201

    def delete(self, name: str) -> JsonType:
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {'message': f'store {name!r} deleted'}
        return {'message': f'store {name!r} not found'}, 404
