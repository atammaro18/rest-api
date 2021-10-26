from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

equipments = []


class Equipment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description')

    def get(self, name):
        equipment = next(filter(lambda x: x['name'] == name, equipments), None)
        return {'equipment': None}, 200 if equipment is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, equipments), None):
                return {'message': "An equipment with name '{}' already exists".format(name)}, 400
        
        data = Equipment.parser.parse_args()

        equipment = {'name': name, 'description': data['description']}
        equipments.append(equipment)
        return equipment, 201

    def delete(self, name):
        global equipments
        equipments = list(filter(lambda x: x['name'] != name, equipments))
        return {'message': "Item Deleted"}

    def put(self, name):
        data = Equipment.parser.parse_args()

        equipment = next(filter(lambda x: x['name'] == name, equipments), None)
        if equipment is None:
         equipment = {'name': name, 'description': data['description']}
         equipments.append(equipment)
        else:
         equipment.update(data)
        return equipment


class EquipmentList(Resource):
    def get(self):
        return {'equipments': equipments}



api.add_resource(Equipment, '/equipment/<string:name>')  # http://127.0.0.1:7000/equipment/name
api.add_resource(EquipmentList, '/equipments')

if __name__ == "__main__":
    app.run(port=7000, debug=True)
