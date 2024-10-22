import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_FOLDER = BASE_DIR / 'storage'  # Almacenamiento de archivos
MODEL_FOLDER = BASE_DIR / 'models'  # Almacenamiento de modelos entrenados

FILE_TYPES = {
    "BANDS": 'bands',
    "PANELS": 'panels'
}


def saveBandFile(file, session_id, type, index):
    if type not in FILE_TYPES.values():
        raise ValueError("Invalid type")
    
    storage_path = os.path.join(STORAGE_FOLDER, session_id, "tif")
    os.makedirs(storage_path, exist_ok=True)

    file_path = os.path.join(storage_path, f"{type}_{index}.tif")
    file.save(file_path)
    

def getBandFiles(session_id: str, type: str = None):
    storage_path = os.path.join(STORAGE_FOLDER, session_id, "tif")    
    return [os.path.join(storage_path, file) for file in os.listdir(storage_path) if type is None or file.startswith(type)]


def saveDataInFile(session_id, data, filename, folder=None):
    storage_path = os.path.join(STORAGE_FOLDER, session_id)
    if(folder): storage_path = os.path.join(storage_path, folder)

    os.makedirs(storage_path, exist_ok=True)

    file_path = os.path.join(storage_path, filename)
    with open(file_path, 'wb') as file:
        file.write(data)


def getDataFromFile(session_id, filename, folder=None):
    storage_path = os.path.join(STORAGE_FOLDER, session_id)
    if(folder): storage_path = os.path.join(storage_path, folder)
    file_path = os.path.join(storage_path, filename)

    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as f:
        data = f.read()
    return data
