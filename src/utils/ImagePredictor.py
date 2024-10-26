import numpy as np
import pandas as pd
import joblib
from utils.ImageGenerator import ImageGenerator
from utils.FileManager import MODEL_FOLDER

class ImagePredictor:
    def __init__(self, image_processor: ImageGenerator):
        self.image_processor = image_processor
        self.roi_indices = {}
        self.statistics = {}

        print("Cargando modelos pre-entrenados.")
        self.pca_model = joblib.load(MODEL_FOLDER / 'pca_model.pkl')
        self.scaler = joblib.load(MODEL_FOLDER / 'scaler.pkl')
        self.regression_model = joblib.load(MODEL_FOLDER / 'model_XGBR_train.pkl')
        

    def set_roi(self, roi_coordinates):
        """
        Establece la ROI utilizando las coordenadas proporcionadas.
        roi_coordinates: lista o tupla {x, y, width, height}
        """

        print("Extrayendo ROI de los índices.")

        x1 = int(roi_coordinates['x'])
        y1 = int(roi_coordinates['y'])
        x2 = x1 + int(roi_coordinates['width'])
        y2 = y1 + int(roi_coordinates['height'])

        self.roi_indices = {}
        for index_name, index_data in self.image_processor.indices.items():
            # Asegurarse de que index_data es un array numpy
            roi = index_data[y1:y2, x1:x2]
            self.roi_indices[index_name] = roi


    def compute_statistics(self):
        if not self.roi_indices:
            raise ValueError("ROI no extraída. Llama a extract_roi_from_indices primero.")

        print("Calculando estadísticas del ROI.")

        self.statistics = {}
        for index_name, roi_data in self.roi_indices.items():
            # Asegurarse de manejar datos enmascarados correctamente
            #roi_data_flat = roi_data.compressed() if np.ma.is_masked(roi_data) else roi_data.flatten()
            
            stats = {
                f'max_{index_name}': roi_data.max(),
                f'min_{index_name}': roi_data.min(),
                f'avg_{index_name}': roi_data.mean(),
                f'std_{index_name}': roi_data.std(),
                f'var_{index_name}': roi_data.var(),
            }
            self.statistics.update(stats)


    def prepare_data_for_prediction(self, data_iot):
        if not self.statistics:
            raise ValueError("No hay estadísticas para preparar. Llama a compute_statistics primero.")
        
        print("Preparando datos para predicción.")

        # Crear un DataFrame con las estadísticas
        df_stats = pd.DataFrame([self.statistics])

        # Crear un DataFrame con los datos de IoT
        df_iot = pd.DataFrame([data_iot])

        inputs = pd.concat([df_iot, df_stats], axis=1)

        # Reordenar y validar que contenga las columnas para que coincidan con el orden de entrenamiento
        inputs = inputs[['soil_humedity', 'soil_temperature', 'pH', 'avg_spad',
                         'max_ndvi', 'min_ndvi', 'avg_ndvi', 'std_ndvi', 'var_ndvi',
                         'max_ndre', 'min_ndre', 'avg_ndre', 'std_ndre', 'var_ndre',
                         'max_gndvi', 'min_gndvi', 'avg_gndvi', 'std_gndvi', 'var_gndvi',
                         'max_evi2', 'min_evi2', 'avg_evi2', 'std_evi2', 'var_evi2',
                         'max_cvi', 'min_cvi', 'avg_cvi', 'std_cvi', 'var_cvi',
                         'max_osavi', 'min_osavi', 'avg_osavi', 'std_osavi', 'var_osavi',
                         'max_sccci', 'min_sccci', 'avg_sccci', 'std_sccci', 'var_sccci',
                         'max_savi', 'min_savi', 'avg_savi', 'std_savi', 'var_savi',
                         'max_maci', 'min_maci', 'avg_maci', 'std_maci', 'var_maci',
                         'max_vari', 'min_vari', 'avg_vari', 'std_vari', 'var_vari',
                         'max_tcari', 'min_tcari', 'avg_tcari', 'std_tcari', 'var_tcari',
                         'max_ipvi', 'min_ipvi', 'avg_ipvi', 'std_ipvi', 'var_ipvi',
                         'max_arvi', 'min_arvi', 'avg_arvi', 'std_arvi', 'var_arvi',
                         'max_gci', 'min_gci', 'avg_gci', 'std_gci', 'var_gci',
                         'max_reci', 'min_reci', 'avg_reci', 'std_reci', 'var_reci',
                         'max_mcari', 'min_mcari', 'avg_mcari', 'std_mcari', 'var_mcari'
                        ]]

        return inputs


    def predict(self, data_iot):
        X = self.prepare_data_for_prediction(data_iot).values

        print("Realizando predicción.")

        # Escalar los datos utilizando el escalador entrenado
        X_scaled = self.scaler.transform(X)

        # Aplicar PCA utilizando el modelo PCA entrenado
        X_pca = self.pca_model.transform(X_scaled)

        # Realizar la predicción con el modelo de regresión
        prediction = self.regression_model.predict(X_pca)
        return prediction[0]
