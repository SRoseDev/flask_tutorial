from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank")
    parser.add_argument('store_id', type=int, required=True, help="Evey item needs a store_id")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'error': 'Error finding item in database'}, 500

        if item:
            return item.json()

        return {'message': 'Item not found'}, 200

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'error': "An item with name '{}' already exists".format(name)}, 400

        json_data = Item.parser.parse_args()
        item = ItemModel(None, name, json_data['price'], json_data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'error': 'An error occurred inserting item into database'}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        item.delete()
        return {'message': 'Item Deleted'}, 200

    @jwt_required()
    def put(self, name):
        json_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(None, name, json_data['price'], json_data['store_id'])
                item.save_to_db()
            except:
                return {'error': 'An error occurred inserting item into database'}, 500

        else:
            try:
                item.price = json_data['price']
                item.save_to_db()
            except:
                return {'error': 'An error occurred updating item into database'}, 500

        return item.json()


class ItemList(Resource):
    def get(self):

        return [item.json() for item in ItemModel.query.all()], 200

