import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_FOLDER = BASE_DIR / 'storage'  # Almacenamiento de archivos
MODEL_FOLDER = BASE_DIR / 'models'  # Almacenamiento de modelos entrenados

FILE_TYPES = {
    "BANDS": 'bands',
    "PANELS": 'panels'
}


def listFiles(session_id: str, folder: str=None):
    storage_path = STORAGE_FOLDER / session_id
    if folder: storage_path /= folder

    if not storage_path.exists():
        return []
    
    return [item for item in storage_path.iterdir() if item.is_file()]


def saveBandFile(file, session_id, type, index):
    if type not in FILE_TYPES.values():
        raise ValueError("Invalid type")
    
    storage_path = STORAGE_FOLDER / session_id / "tif"
    storage_path.mkdir(parents=True, exist_ok=True)

    file_path = storage_path / f"{type}_{index}.tif"
    file.save(str(file_path))
    

def getBandFiles(session_id: str, type: str = None):
    files = listFiles(session_id, 'tif')

    if type:
        files = [file for file in files if file.name.startswith(type)]

    # Convertir los objetos Path a cadenas de texto (rutas absolutas)
    return [str(file.resolve()) for file in files]


def saveDataInFile(session_id, data, filename, folder=None):
    storage_path = STORAGE_FOLDER / session_id
    if folder: storage_path /= folder

    storage_path.mkdir(parents=True, exist_ok=True)
    file_path = storage_path / filename

    with open(str(file_path), 'wb') as file:
        file.write(data)


def getDataFromFile(session_id, filename, folder=None):
    file_path = getFilePath(session_id, filename, folder)

    if not file_path:
        return None

    with open(str(file_path), 'rb') as f:
        data = f.read()
    
    return data

def getFilePath(session_id, filename, folder=None):
    storage_path = STORAGE_FOLDER / session_id
    if folder: storage_path /= folder

    file_path = storage_path / filename
    if not file_path.exists():
        return None

    return file_path
