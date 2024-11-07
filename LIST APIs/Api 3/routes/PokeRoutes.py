from flask import Blueprint, jsonify, request
from services.Service import get_all_pokemon_service, get_pokemon_by_id_service, create_pokemon_service, update_pokemon_service, delete_pokemon_service

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/api/v1/pokemon', methods=['GET'])
def get_pokemon():
    pokemon = get_all_pokemon_service()
    pokemon_list = [{'id': p.poke_id, 'name': p.poke_name, 'type': p.poke_type, 'evolution': p.poke_evolution} for p in pokemon]
    return jsonify({'pokemon': pokemon_list})

@pokemon_bp.route('/api/v1/pokemon', methods=['POST'])
def create_pokemon_route():
    data = request.get_json()
    poke_name = data.get('name')
    poke_type = data.get('type')
    poke_evolution = data.get('evolution')
    
    if not poke_name or not poke_type or not poke_evolution:
        return jsonify({'error': 'name, type, and evolution are required'}), 400
    
    new_pokemon_id = create_pokemon_service(poke_name, poke_type, poke_evolution)
    return jsonify({'message': 'Pokemon created successfully', 'poke_id': new_pokemon_id})

@pokemon_bp.route('/api/v1/pokemon/<int:poke_id>', methods=['GET'])
def get_pokemon_by_id_route(poke_id):
    pokemon = get_pokemon_by_id_service(poke_id)
    if pokemon:
        return jsonify({'pokemon': {'id': pokemon.poke_id, 'name': pokemon.poke_name, 'type': pokemon.poke_type, 'evolution': pokemon.poke_evolution}})
    else:
        return jsonify({'error': 'Pokemon not found'}), 404

@pokemon_bp.route('/api/v1/pokemon/<int:poke_id>', methods=['PUT'])
def update_pokemon_route(poke_id):
    data = request.get_json()
    poke_name = data.get('name')
    poke_type = data.get('type')
    poke_evolution = data.get('evolution')

    if not poke_name or not poke_type or not poke_evolution:
        return jsonify({'error': 'name, type, and evolution are required'}), 400
    
    existing_pokemon = get_pokemon_by_id_service(poke_id)
    if existing_pokemon:
        update_pokemon_service(poke_id, poke_name, poke_type, poke_evolution)
        return jsonify({'message': 'Pokemon updated successfully', 'pokemon': {'id': poke_id, 'name': poke_name, 'type': poke_type, 'evolution': poke_evolution}})
    else:
        return jsonify({'error': 'Pokemon not found'}), 404

@pokemon_bp.route('/api/v1/pokemon/<int:poke_id>', methods=['DELETE'])
def delete_pokemon_route(poke_id):
    existing_pokemon = get_pokemon_by_id_service(poke_id)
    if existing_pokemon:
        delete_pokemon_service(poke_id)
        return jsonify({'message': 'Pokemon deleted successfully'})
    else:
        return jsonify({'error': 'Pokemon not found'}), 404
