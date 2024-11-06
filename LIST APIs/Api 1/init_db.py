import psycopg2

conn = psycopg2.connect(database='postgres', host='localhost', user='postgres', password='Hasibuanfirman1404', port='5432')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS crudTutorial (
        id serial PRIMARY KEY,
        name varchar(255),
        description varchar(1000)
    )
''')

cur.execute('''
    INSERT INTO crudTutorial (name, description)
    VALUES ('first_name', 'description')
''')

conn.commit()

cur.close()
conn.close()