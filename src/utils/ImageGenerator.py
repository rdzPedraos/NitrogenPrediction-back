from io import BytesIO
import cv2
import joblib
import pickle
import imageio
import numpy as np
import matplotlib.pyplot as plt

from micasense import imageutils, plotutils
from utils.ImageProcessor import ImageProcessor
from utils.FileManager import saveDataInFile, getDataFromFile
#from osgeo import gdal

class ImageGenerator:
    FILTERS_KEY = {
        "ndvi": "Normalized Difference Vegetation Index",
        "ndre": "Normalized Difference Red Edge",
        "gndvi": "Green Normalized Difference Vegetation Index",
        "evi2": "Enhanced Vegetation Index 2",
        "cvi": "Chlorophyll Vegetation Index",
        "osavi": "Optimized Soil-Adjusted Vegetation Index",
        "sccci": "Simple Ratio Chlorophyll Carotenoid Index",
        "savi": "Soil-Adjusted Vegetation Index",
        "maci": "Modified Anthocyanin Chlorophyll Index",
        "vari": "Visible Atmospherically Resistant Index",
        "tcari": "Transformed Chlorophyll Absorption in Reflectance Index",
        "ipvi": "Infrared Percentage Vegetation Index",
        "arvi": "Atmospherically Resistant Vegetation Index",
        "gci": "Green Chlorophyll Index",
        "reci": "Red Edge Chlorophyll Index",
        "mcari": "Modified Chlorophyll Absorption Ratio Index",
    }

    indices = None

    # Data de imagen RGB corregida
    gamma_corr_rgb = None

    def __init__(self, processor: ImageProcessor, session_id: str):
        self.processor = processor
        self.session_id = session_id

        self.figsize = (16, 13)
        self.roi = None
        self.roi_indices = {}


    def generate_rgb(self):
        # Si la imagen RGB ya ha sido generada, devolverla
        if self.gamma_corr_rgb is not None:
            return self.gamma_corr_rgb

        print("Generando la imagen RGB corregida para visualización.")
        processor = self.processor
        im_al = processor.imageAligned

        rgb_band_indices = [
            processor.BAND_INDEXES['red'],
            processor.BAND_INDEXES['green'],
            processor.BAND_INDEXES['blue']
        ]

        im_display = np.zeros_like(im_al, dtype=np.float32)

        im_min = np.percentile(im_al[:, :, rgb_band_indices].flatten(), 0.5)
        im_max = np.percentile(im_al[:, :, rgb_band_indices].flatten(), 99.5)

        for i in rgb_band_indices:
            im_display[:, :, i] = imageutils.normalize(im_al[:, :, i], im_min, im_max)

        rgb = im_display[:, :, rgb_band_indices]

        # Unsharp mask
        gaussian_rgb = cv2.GaussianBlur(rgb, (9, 9), 10.0)
        unsharp_rgb = cv2.addWeighted(rgb, 1.5, gaussian_rgb, -0.5, 0)
        unsharp_rgb = np.clip(unsharp_rgb, 0, 1)

        # Gamma correction
        gamma = 1.4
        self.gamma_corr_rgb = unsharp_rgb ** (1.0 / gamma)
        return self.gamma_corr_rgb


    def compute_indices(self):
        if(self.indices):
            return self.indices
        
        print("Calculando los índices de vegetación.")

        processor = self.processor
        b_indexes = processor.BAND_INDEXES
        im_al = processor.imageAligned

        nir_band = im_al[:, :, b_indexes["nir"]]
        red_band = im_al[:, :, b_indexes["red"]]
        green_band = im_al[:, :, b_indexes["green"]]
        rededge_band = im_al[:, :, b_indexes["red-edge"]]
        blue_band = im_al[:, :, b_indexes["blue"]]

        np.seterr(divide='ignore', invalid='ignore')

        L = 0.7
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        ndre = (nir_band - rededge_band) / (nir_band + rededge_band)

        self.indices = {
            "ndvi": ndvi,
            "ndre": ndre,
            "gndvi" : (nir_band - green_band) / (nir_band + green_band),
            "evi2" : 2.5 * (nir_band - red_band) / (nir_band + 2.4 * red_band + 1),
            "cvi" : (nir_band / green_band) * (red_band / green_band),
            "osavi" : (nir_band - red_band) / (nir_band + red_band + 0.16),
            "sccci" : ndre / ndvi,
            "savi" : ((nir_band - red_band) / (nir_band + red_band + L)) * (1 + L),
            "maci" : nir_band / green_band,
            "vari" : (green_band - red_band) / (green_band + red_band - blue_band),
            "tcari" : 3 * ((rededge_band - red_band) - 0.2 * (rededge_band - green_band) * (rededge_band / red_band)),
            "ipvi" : nir_band / (nir_band + red_band),
            "arvi" : (nir_band - (2 * red_band) + blue_band / (nir_band + (2 * red_band) + blue_band)),
            "gci" : (nir_band / green_band) - 1,
            "reci" : (nir_band / rededge_band) - 1,
            "mcari" : ((rededge_band - red_band) - 0.2 * (rededge_band - green_band)) * (rededge_band / red_band),
        }

        return self.indices


    def mask_indices(self, min_ndvi=0.8):
        print("Aplicando una máscara a los índices para filtrar suelos y sombras.")
        indices = self.compute_indices()

        ndvi = indices['ndvi']
        if self.processor.CONFIG["image_type"] == self.processor.REFLECTANCE_TYPE:
            ndvi_mask = np.ma.masked_where(ndvi < min_ndvi, ndvi)
        else:
            lower_pct_radiance = np.percentile(ndvi, 10.0)
            ndvi_mask = np.ma.masked_where(ndvi < lower_pct_radiance, ndvi)

        for key, value in indices.items():
            self.indices[key] = np.ma.masked_where(ndvi_mask.mask, value)


    def save_rgb_image(self):
        print("Guardando la imagen RGB")

        # Generar la imagen RGB y escalar los valores
        rgb_image_array = (255 * self.generate_rgb()).astype('uint8')

        # Especificar el formato 'PNG' al escribir la imagen
        rgb_image_bytes = imageio.imwrite("<bytes>", rgb_image_array, format='PNG')

        # Guardar los bytes de la imagen utilizando el FileManager
        saveDataInFile(self.session_id, rgb_image_bytes, "rgb.png", folder="images")


    def generate_and_save_index_outputs(self):
        print("Generando y guardando imágenes e histogramas para cada índice.")

        # Asegurarse de que los índices han sido calculados y enmascarados
        indices = self.compute_indices()

        for index_type, index_data in indices.items():
            print(f"Procesando el índice: {index_type.upper()}")

            # Asegurarse de que hay datos válidos
            index_flat = index_data.compressed()
            if index_flat.size == 0:
                print(f"No hay datos válidos para el índice {index_type}. Se omite.")
                continue

            # Generar y guardar la imagen del índice superpuesto sobre la imagen RGB
            self._generate_and_save_index_image(index_type, index_data)

            # Generar y guardar el histograma del índice
            self._generate_and_save_index_histogram(index_type, index_flat)


    def _generate_and_save_index_histogram(self, index_name, index_flat):
        # Calcular el mínimo y máximo para el rango del histograma
        index_hist_min = index_flat.min()
        index_hist_max = index_flat.max()

        # Crear la figura y el eje
        fig, axis = plt.subplots(1, 1, figsize=(10, 4))

        # Generar el histograma
        axis.hist(index_flat, bins=512, range=(index_hist_min, index_hist_max), color='blue', alpha=0.7)

        # Establecer el título y las etiquetas
        axis.set_title(f"{index_name.upper()} Histogram")
        axis.set_xlabel(f"Values for {index_name.upper()}")
        axis.set_ylabel("Frecuency")

        # Agregar cuadrícula para mejor visualización
        axis.grid(True)

        # Guardar la figura en un buffer
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        histogram_image_bytes = buf.read()

        # Utilizar el FileManager para guardar la imagen
        filename = f'{index_name}.png'
        saveDataInFile(self.session_id, histogram_image_bytes, filename, folder="histograms")
        plt.close(fig)  # Cerrar la figura para liberar memoria

        print(f"-- Histograma del índice {index_name} guardado como {filename}")
    

    def _generate_and_save_index_image(self, index_name, index_data):
        # Calcular percentiles para normalizar el índice
        min_display = np.percentile(index_data.compressed(), 5)
        max_display = np.percentile(index_data.compressed(), 95)

        # Generar la figura y el eje utilizando plot_overlay_withcolorbar
        fig, ax = plotutils.plot_overlay_withcolorbar(
            self.generate_rgb(),
            index_data,
            figsize=self.figsize,
            title='',
            vmin=min_display,
            vmax=max_display
        )

        # Remover el título y los ejes
        ax.set_title('')
        ax.axis('off')

        # Remover la barra de color si existe
        if len(fig.axes) > 1:
            cbar = fig.axes[-1]
            fig.delaxes(cbar)

        # Ajustar la figura para eliminar márgenes
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

        # Guardar la figura en un buffer
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        index_image_bytes = buf.read()

        # Utilizar el FileManager para guardar la imagen
        filename = f'{index_name}.png'
        saveDataInFile(self.session_id, index_image_bytes, filename, folder="images")
        plt.close(fig)  # Cerrar la figura para liberar memoria

        print(f"-- Imagen del índice {index_name} guardada como {filename}")

    
    def save_indices(self):
        print("Guardando los índices calculados.")

        # Serializar los índices a bytes utilizando pickle
        indices_data = pickle.dumps(self.indices)
        
        # Utilizar el FileManager para guardar los datos en la sesión
        saveDataInFile(self.session_id, indices_data, 'indices.pkl')


    def load_indices(self):
        print("Cargando los índices calculados.")

        indices_data = getDataFromFile(self.session_id, 'indices.pkl')
        if indices_data is None:
            raise FileNotFoundError(f"No se encontraron índices para la sesión {self.session_id}")

        # Deserializar los índices
        self.indices = joblib.loads(indices_data)
        print(f"Índices cargados para la sesión {self.session_id}")
