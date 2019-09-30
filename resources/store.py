from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {'error': 'Error finding item in database'}, 500

        if store:
            return store.json()

        return {'message': 'Store not found'}, 200

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'error': "A store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'error': 'An error occurred inserting store into database'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        store.delete()
        return {'message': 'Store Deleted'}, 200


class StoreList(Resource):
    def get(self):
        return [store.json() for store in StoreModel.query.all()]
