import numpy as np
import joblib
import os

from config import Config

# Cargar los modelos entrenados al iniciar el módulo
xgb_model = joblib.load(Config.MODEL_FOLDER / 'model_XGBR_train.pkl')
pca_model = joblib.load(Config.MODEL_FOLDER / 'pca_model.pkl')
scaler = joblib.load(Config.MODEL_FOLDER / 'scaler.pkl')

def predict_nitrogen(session_data, roi):
    try:
        x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']

        # Cargar los índices necesarios
        indices = {}
        for index_name in ['ndvi', 'ndre']:  # Agrega otros índices si los necesitas
            index_path = session_data.get(index_name)
            if not index_path or not os.path.exists(index_path):
                return {'error': f'{index_name.upper()} data not found'}
            index_data = np.load(index_path)
            indices[index_name] = index_data

        # Extraer el ROI y calcular estadísticas
        stats = {}
        for index_name, index_data in indices.items():
            roi_data = index_data[y:y+h, x:x+w]
            stats[index_name] = calculate_statistics(roi_data)

        # Preparar datos para la predicción
        X_new = extract_features_from_stats(stats)
        X_new_scaled = scaler.transform([X_new])
        X_new_pca = pca_model.transform(X_new_scaled)
        prediction = xgb_model.predict(X_new_pca)

        return {'prediction': float(prediction[0]), 'stats': stats}

    except Exception as e:
        return {'error': str(e)}

def calculate_statistics(roi_data):
    return {
        'max': float(np.max(roi_data)),
        'min': float(np.min(roi_data)),
        'mean': float(np.mean(roi_data)),
        'std': float(np.std(roi_data)),
        'var': float(np.var(roi_data))
    }

def extract_features_from_stats(stats):
    X_new = []
    for index_name in stats:
        for stat_name in ['max', 'min', 'mean', 'std', 'var']:
            X_new.append(stats[index_name][stat_name])
    return X_new
