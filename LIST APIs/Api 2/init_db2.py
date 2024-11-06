import psycopg2 

conn = psycopg2.connect(
    database='postgres', 
    host='localhost', 
    user='postgres', 
    password='Hasibuanfirman1404', 
    port='5432'
)

with conn.cursor() as cur:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bangkitz (
            b_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            role VARCHAR(255),
            no_study_group INTEGER,
            university VARCHAR(255),
            semester INTEGER
        )
    ''')

    cur.execute('''
        INSERT INTO bangkitz (name, role, no_study_group, university, semester)
        VALUES ('firman hasibuan', 'machine learning', 14, 'unair', 5)
    ''')

conn.commit()
conn.close()