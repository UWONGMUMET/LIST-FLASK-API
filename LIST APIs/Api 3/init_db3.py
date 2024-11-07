import psycopg2

conn = psycopg2.connect(
    database='postgres',
    host='localhost',
    user='postgres',
    password='Hasibuanfirman1404',
    port='5432'
)

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        poke_id SERIAL PRIMARY KEY,
        poke_name VARCHAR(255),
        poke_type VARCHAR(255),
        poke_evolution INTEGER
    )
''')

pokemon_data = [
    ('Pikachu', 'Electric', 1),
    ('Charmander', 'Fire', 1),
    ('Bulbasaur', 'Grass', 1)
]

cur.executemany('''
    INSERT INTO pokemon (poke_name, poke_type, poke_evolution)
    VALUES (%s, %s, %s)
''', pokemon_data)

conn.commit()
cur.close()
conn.close()