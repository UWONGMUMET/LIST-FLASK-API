from flask import Blueprint, jsonify, request
from services.Service import get_all_notes_service, get_note_by_id_service, create_note_service, update_note_service, delete_note_service

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/api/bangkitz/db', methods=['GET'])
def get_notes():
    notes = get_all_notes_service()
    notes_list = [
        {
            'b_id': note.b_id, 
            'name': note.name, 
            'role': note.role, 
            'no_study_group': note.no_study_group, 
            'university': note.university, 
            'semester': note.semester
        } 
        for note in notes
    ]
    return jsonify({'notes': notes_list})

@notes_bp.route('/api/bangkitz/db', methods=['POST'])
def create_note_route():
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    no_study_group = data.get('no_study_group')
    university = data.get('university')
    semester = data.get('semester')

    if not all([name, role, no_study_group, university, semester]):
        return jsonify({'error': 'All fields are required'}), 400

    new_note_id = create_note_service(name, role, no_study_group, university, semester)
    return jsonify({'message': 'Note created successfully', 'note_id': new_note_id})

@notes_bp.route('/api/bangkitz/db/<int:note_id>', methods=['PUT'])
def update_note_route(note_id):
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    no_study_group = data.get('no_study_group')
    university = data.get('university')
    semester = data.get('semester')

    if not all([name, role, no_study_group, university, semester]):
        return jsonify({'error': 'All fields are required'}), 400
    
    existing_note = get_note_by_id_service(note_id) 
    if existing_note:
        updated_note = update_note_service(note_id, name, role, no_study_group, university, semester)
        return jsonify({'message': 'Db updated successfully', 'note': updated_note})
    else:
        return jsonify({'error': 'Note not found'}), 404
    
@notes_bp.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note_route(note_id):
    existing_note = get_note_by_id_service(note_id) 
    if existing_note:
        delete_note_service(note_id)
        return jsonify({'message': 'note deleted successfully'})
    else:
        return jsonify({"error": 'note not found'})