# src/routes/upload_route.py
from flask import request, jsonify, current_app
from utils.image_processing import process_images
import uuid
import os

from . import main_blueprint
from utils.session_manager import save_session_data

@main_blueprint.route('/upload', methods=['POST'])
def upload_images():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    session_id = str(uuid.uuid4())

    # Directorio para almacenar archivos de la sesión
    storage_path = os.path.join(current_app.config['STORAGE_FOLDER'], session_id)
    os.makedirs(storage_path, exist_ok=True)

    # Guardar archivos subidos
    for file in files:
        filename = file.filename
        filepath = os.path.join(storage_path, filename)
        file.save(filepath)

    # Almacenar información de la sesión en un archivo
    session_data = {
        'session_id': session_id,
        'status': 'processing',
        'storage_path': storage_path,
        'images': {},
        'im_aligned_path': '',
        'stats': {}
    }
    save_session_data(session_id, session_data)

    # Procesar las imágenes
    process_images(session_id)

    return jsonify({'session_id': session_id}), 200
