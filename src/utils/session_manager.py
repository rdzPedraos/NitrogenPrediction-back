import os
import json
from config import Config

def save_session_data(session_id, session_data):
    session_file = os.path.join(Config.SESSION_FOLDER, f'{session_id}.json')
    with open(session_file, 'w') as f:
        json.dump(session_data, f)

def load_session_data(session_id):
    session_file = os.path.join(Config.SESSION_FOLDER, f'{session_id}.json')
    if not os.path.exists(session_file):
        return None
    with open(session_file, 'r') as f:
        session_data = json.load(f)
    return session_data

def update_session_status(session_id, status):
    session_data = load_session_data(session_id)
    if session_data:
        session_data['status'] = status
        save_session_data(session_id, session_data)

def cleanup_sessions(max_age_seconds=3600):
    import time
    import os

    current_time = time.time()
    for filename in os.listdir(Config.SESSION_FOLDER):
        if filename.endswith('.json'):
            session_file = os.path.join(Config.SESSION_FOLDER, filename)
            session_age = current_time - os.path.getmtime(session_file)
            if session_age > max_age_seconds:
                session_id = filename.replace('.json', '')
                # Eliminar archivo de sesión
                os.remove(session_file)
                # Eliminar directorio de almacenamiento asociado
                storage_path = os.path.join(Config.STORAGE_FOLDER, session_id)
                if os.path.exists(storage_path):
                    shutil.rmtree(storage_path)
