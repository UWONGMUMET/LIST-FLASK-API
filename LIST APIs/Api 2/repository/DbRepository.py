import psycopg2
from models.Note import Db

def db_conn():
    return psycopg2.connect(
        database='postgres',
        host='localhost',
        user='postgres',
        password='Hasibuanfirman1404',
        port='5432'
    )

def get_all_notes():
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM bangkitz')
            data = cur.fetchall()

    notes = [
        Db(b_id=note[0], name=note[1], role=note[2], no_study_group=note[3], university=note[4], semester=note[5])
        for note in data
    ]
    return notes

def get_note_by_id(note_id):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM bangkitz WHERE b_id = %s', (note_id,))
            note_data = cur.fetchone()

    if note_data:
        return Db(
            b_id=note_data[0],
            name=note_data[1],
            role=note_data[2],
            no_study_group=note_data[3],
            university=note_data[4],
            semester=note_data[5]
        )
    return None

def create_note(name, role, no_study_group, university, semester):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO bangkitz (name, role, no_study_group, university, semester)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING b_id
                ''', 
                (name, role, no_study_group, university, semester)
            )
            new_note_id = cur.fetchone()[0]
            conn.commit()

    return new_note_id

def update_note(note_id, name, role, no_study_group, university, semester):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                UPDATE bangkitz
                SET name = %s, role = %s, no_study_group = %s, university = %s, semester = %s
                WHERE b_id = %s
                ''', 
                (name, role, no_study_group, university, semester, note_id)
            )
            conn.commit()

def delete_note(note_id):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM bangkitz WHERE b_id = %s', (note_id,))
            conn.commit()