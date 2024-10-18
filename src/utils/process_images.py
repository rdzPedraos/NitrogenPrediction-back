from extensions import logger

from utils.file_manager import get_all_files
from micasense import capture


def separe_data(files: list):
    bands = filter(lambda file: file.startswith('bands'), files)
    panels = filter(lambda file: file.startswith('panels'), files)

    return list(bands), list(panels)

def process_images(files: list):
    bands, panels = separe_data(files)

    panelCap = capture.Capture.from_filelist(panels)
    bandsCap = capture.Capture.from_filelist(bands)

    if panelCap.panel_albedo() is not None:
        panel_reflectance_by_band = panelCap.panel_albedo()
    else:
        # raise IOError("Comment this lne and set panel_reflectance_by_band here")
        #panel_reflectance_by_band = [0.65]*len(imageNames)
        panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67]

    panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)    
    capture.plot_undistorted_reflectance(panel_irradiance)

    logger.info("prepare images: ")
