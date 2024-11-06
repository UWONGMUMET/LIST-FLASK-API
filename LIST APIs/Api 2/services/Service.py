from repository.DbRepository import get_all_notes, get_note_by_id, create_note, update_note, delete_note

def get_all_notes_service():
    return get_all_notes()

def get_note_by_id_service(note_id):
    return get_note_by_id(note_id)

def create_note_service(name, role, no_study_group, university, semester):
    return create_note(name, role, no_study_group, university, semester)

def update_note_service(note_id, name, role, no_study_group, university, semester):
    return update_note(note_id, name, role, no_study_group, university, semester)

def delete_note_service(note_id):
    return delete_note(note_id)
