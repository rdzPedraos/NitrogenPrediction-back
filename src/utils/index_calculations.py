import numpy as np
import micasense.imageutils as imageutils

def calculate_indices(im_aligned, cap):
    indices = {}
    nir_band = [name.lower() for name in cap.band_names()].index('nir')
    red_band = [name.lower() for name in cap.band_names()].index('red')
    rededge_band = [name.lower() for name in cap.band_names()].index('red edge')
    green_band = [name.lower() for name in cap.band_names()].index('green')
    blue_band = [name.lower() for name in cap.band_names()].index('blue')

    # NDVI
    ndvi = (im_aligned[:, :, nir_band] - im_aligned[:, :, red_band]) / \
           (im_aligned[:, :, nir_band] + im_aligned[:, :, red_band])
    indices['ndvi'] = ndvi

    # NDRE
    ndre = (im_aligned[:, :, nir_band] - im_aligned[:, :, rededge_band]) / \
           (im_aligned[:, :, nir_band] + im_aligned[:, :, rededge_band])
    indices['ndre'] = ndre

    # Agrega más índices si es necesario

    return indices

def generate_rgb_image(im_aligned, cap):
    rgb_band_indices = [cap.band_names().index('Red'),
                        cap.band_names().index('Green'),
                        cap.band_names().index('Blue')]

    im_display = np.zeros((im_aligned.shape[0], im_aligned.shape[1], 3), dtype=np.float32)
    im_min = np.percentile(im_aligned[:, :, rgb_band_indices].flatten(), 0.5)
    im_max = np.percentile(im_aligned[:, :, rgb_band_indices].flatten(), 99.5)

    for i, band_index in enumerate(rgb_band_indices):
        im_display[:, :, i] = imageutils.normalize(im_aligned[:, :, band_index], im_min, im_max)

    gamma = 1.4
    im_display = im_display ** (1.0 / gamma)
    im_display[im_display < 0] = 0
    im_display[im_display > 1] = 1

    return im_display
