import os
from config import Config

def save(session_id, file, filename):
    storage_path = os.path.join(Config.STORAGE_FOLDER, session_id)
    os.makedirs(storage_path, exist_ok=True)

    file.save(os.path.join(storage_path, filename))
