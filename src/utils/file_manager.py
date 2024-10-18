import os
from config import Config

FILE_TYPES = {
    "BANDS": 'bands',
    "PANELS": 'panels'
}

def save(session_id, file, filename):
    storage_path = os.path.join(Config.STORAGE_FOLDER, session_id)
    os.makedirs(storage_path, exist_ok=True)

    file.save(os.path.join(storage_path, filename))

def saveBandFile(file, session_id, type, index):
    if type not in FILE_TYPES.values():
        raise ValueError("Invalid type")
    save(session_id, file, f"{type}_{index}.tif")
