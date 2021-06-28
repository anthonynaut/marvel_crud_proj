from flask import Blueprint, request, jsonify
from marvel_crud.helpers import token_required
from marvel_crud.models import db,User,Character,character_schema,character_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}


# CREATE DRONE ENDPOINT
@api.route('/characters', methods = ['POST'])
@token_required
def create_char(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['dimensions']
    date_created = request.json['weight']
    cost_of_prod = request.json['cost_of_prod']
    series = request.json['series']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    character = Character(name,description,comics_appeared_in, super_power, date_created,cost_of_prod,series,user_token = user_token )

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)




# RETRIEVE ALL DRONEs ENDPOINT
@api.route('/characters', methods = ['GET'])
@token_required
def get_character(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = character_schema.dump(characters)
    return jsonify(response)


# RETRIEVE ONE Drone ENDPOINT
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_characters(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE DRONE ENDPOINT
@api.route('/characters/<id>', methods = ['POST','PUT'])
@token_required
def update_character(current_user_token,id):
    character = Character.query.get(id) # GET DRONE INSTANCE

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.date_created = request.json['date_created']
    character.cost_of_prod = request.json['cost_of_prod']
    character.series = request.json['series']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)


# DELETE DRONE ENDPOINT
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)
