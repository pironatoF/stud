from models.item import ItemModel
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from typing import Union, Dict, List, Any, Type
JsonType = Union[Dict[str, Any], List[Any],
                 int, str, float, bool, Type[None]]


class ItemList(Resource):
    def get(self) -> JsonType:
        items = ItemModel.query.all()
        if items:
            return {'items': [item.json() for item in items]}, 200
        return {'message': 'no items'}, 404


class Item(Resource):
    """Item Resource
    NOTE for jwt_required decorator below:
    i have to call () because im gettin error by passing name params
    to resource method ( @TODO investigate)
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="This item need a store_id"
    )

    @ jwt_required()
    def get(self, name: str) -> JsonType:
        item = ItemModel.find_by_name(name)
        if item:
            return {"item": item.json()}, 200
        return {'message': 'Item not found'}, 404

    def post(self, name: str) -> JsonType:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f"An item with name {item.name!r} already exist!"}, 400
        try:
            new_item = ItemModel(name, data.get('price'), data.get('store_id'))
            new_item.save()
        except:
            return {'message': "An error occurred inserting items"}, 500
        return {"item": new_item.json()}, 201

    def delete(self, name: str) -> JsonType:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message': f'Item {name!r} deleted'}
        return {'message': f'Item {name!r} not found'}, 404

    def put(self, name: str) -> JsonType:
        """
        create/update Item Resource
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data.get('price')
            item.save()
            return {"item": item.json()}, 200
        item = ItemModel(name, data.get('price'), data.get('store_id'))
        item.save()
        return {"item": item.json()}  # implicit item, 200
