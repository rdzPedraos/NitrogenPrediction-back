import cv2
from micasense import capture, imageutils

class ImageProcessor:
    RADIANCE_TYPE = 'radiance'
    REFLECTANCE_TYPE = 'reflectance'

    CONFIG = {
        "match_index": 4,
        "max_alignment_iterations": 20,
        "warp_mode": cv2.MOTION_HOMOGRAPHY,
        "pyramid_levels": 3,
        "image_type": None
    }

    def __init__(self, imagesPath: list, panelsPath: list = []):
        # Perform basic processing
        self.imageCap, self.panelCap = self.process_capture(imagesPath, panelsPath)
        self.band_names = [name.lower() for name in self.imageCap.band_names()]
        self.CONFIG["image_type"] = self.REFLECTANCE_TYPE if self.panelCap else self.RADIANCE_TYPE
        
        # Aligned images
        warp_matrices = self.align_images()

        # Cropped images
        self.im_aligned = self.crop_aligned_images(self.imageCap, warp_matrices)
        

    def process_capture(self, imagesPath: list, panelsPath: list):
        print("Procesando las imágenes y calculando la irradiancia del panel si está disponible.")

        imageCap = capture.Capture.from_filelist(imagesPath)
        panelCap = None

        if self.panelsPath:
            panelCap = capture.Capture.from_filelist(panelsPath)

            panel_reflectance_by_band = panelCap.panel_albedo() or [0.67, 0.69, 0.68, 0.61, 0.67]
            panel_irradiance = self.panelCap.panel_irradiance(panel_reflectance_by_band)

            imageCap.plot_undistorted_reflectance(panel_irradiance)

        return imageCap, panelCap
        

    def align_images(self):
        print("Alineando las imágenes utilizando las configuraciones especificadas.")

        warp_matrices, alignment_pairs = imageutils.align_capture(
            self.imageCap,
            ref_index=self.CONFIG["match_index"],
            warp_mode=self.CONFIG["warp_mode"],
            max_iterations=self.CONFIG["max_alignment_iterations"],
            pyramid_levels=self.CONFIG["pyramid_levels"]
        )

        return warp_matrices
    

    def crop_aligned_images(self, imageCap, warp_matrices): 
        print("Recortando las imágenes alineadas para eliminar áreas sin superposición.")

        cropped_dimensions, edges = imageutils.find_crop_bounds(imageCap, warp_matrices, self.CONFIG["warp_mode"])

        im_aligned = imageutils.aligned_capture(
            imageCap,
            warp_matrices,
            self.CONFIG["warp_mode"],
            cropped_dimensions,
            self.CONFIG["match_index"],
            self.CONFIG["image_type"]
        )

        return im_aligned
