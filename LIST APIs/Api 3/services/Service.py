from repository.PokeRepository import get_all_pokemon, get_pokemon_by_id, create_pokemon, update_pokemon, delete_pokemon

def get_all_pokemon_service():
    return get_all_pokemon()

def get_pokemon_by_id_service(poke_id):
    return get_pokemon_by_id(poke_id)

def create_pokemon_service(poke_name, poke_type, poke_evolution):
    return create_pokemon(poke_name, poke_type, poke_evolution)

def update_pokemon_service(poke_id, poke_name, poke_type, poke_evolution):
    update_pokemon(poke_id, poke_name, poke_type, poke_evolution)

def delete_pokemon_service(poke_id):
    delete_pokemon(poke_id)
