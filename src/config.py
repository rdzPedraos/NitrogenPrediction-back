from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = 'your_secret_key'
    STORAGE_FOLDER = BASE_DIR / 'storage'  # Almacenamiento de archivos
    SESSION_FOLDER = BASE_DIR / 'sessions'  # Almacenamiento de datos de sesión
    MODEL_FOLDER = BASE_DIR / 'models'  # Almacenamiento de modelos entrenados

