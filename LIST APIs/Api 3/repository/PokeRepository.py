import psycopg2
from models.Poke import Poke

def db_conn():
    return psycopg2.connect(database='postgres', host='localhost', user='postgres', password='Hasibuanfirman1404', port='5432')


def get_all_pokemon():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemon")
    data = cur.fetchall()
    cur.close()
    conn.close()

    pokemon_list = [Poke(poke_id=row[0], poke_name=row[1], poke_type=row[2], poke_evolution=row[3]) for row in data]
    return pokemon_list


def get_pokemon_by_id(poke_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemon WHERE poke_id = %s", (poke_id,))
    poke_data = cur.fetchone()
    cur.close()
    conn.close()

    if poke_data:
        return Poke(poke_id=poke_data[0], poke_name=poke_data[1], poke_type=poke_data[2], poke_evolution=poke_data[3])
    else:
        return None


def create_pokemon(poke_name, poke_type, poke_evolution):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO pokemon (poke_name, poke_type, poke_evolution) VALUES (%s, %s, %s) RETURNING poke_id",
                (poke_name, poke_type, poke_evolution))
    new_pokemon_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_pokemon_id


def update_pokemon(poke_id, poke_name, poke_type, poke_evolution):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE pokemon SET poke_name = %s, poke_type = %s, poke_evolution = %s WHERE poke_id = %s",
                (poke_name, poke_type, poke_evolution, poke_id))
    conn.commit()
    cur.close()
    conn.close()


def delete_pokemon(poke_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM pokemon WHERE poke_id = %s", (poke_id,))
    conn.commit()
    cur.close()
    conn.close()
