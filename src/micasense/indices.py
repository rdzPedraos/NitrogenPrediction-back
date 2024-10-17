# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:16:02 2022

@author: jchaparro
"""

def vegetation_indices(nir_band, red_band, green_band, blue_band,rededge_band):
    from micasense import plotutils
    import matplotlib.pyplot as plt

    ############### Normalized Difference Vegetation Index  (𝑁𝐷𝑉𝐼) #####################
    
    np.seterr(divide='ignore', invalid='ignore') # ignore divide by zero errors in the index calculation

    # Compute Normalized Difference Vegetation Index (NDVI) from the NIR(3) and RED (2) bands
    ndvi = (im_aligned[:,:,nir_band] - im_aligned[:,:,red_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,red_band])

    # remove shadowed areas (mask pixels with NIR reflectance < 20%))
    if img_type == 'reflectance':
        ndvi = np.ma.masked_where(im_aligned[:,:,nir_band] < 0.30, ndvi) 
    elif img_type == 'radiance':
        lower_pct_radiance = np.percentile(im_aligned[:,:,3],  10.0)
        ndvi = np.ma.masked_where(im_aligned[:,:,nir_band] < lower_pct_radiance, ndvi) 
            
    min_display_ndvi = 0.8 # further mask soil by removing low-ndvi values
    #min_display_ndvi = np.percentile(ndvi.flatten(),  5.0)  # modify with these percentilse to adjust contrast
    max_display_ndvi = np.percentile(ndvi.flatten(), 99.5)  # for many images, 0.5 and 99.5 are good values
    masked_ndvi = np.ma.masked_where(ndvi < min_display_ndvi, ndvi)

    ############## Normalized Difference Red Edge Index  (𝑁𝐷𝑅𝐸)  #################

    # Compute Normalized Difference Red Edge Index from the NIR(3) and RedEdge(4) bands
    rededge_band = [name.lower() for name in capture.band_names()].index('red edge')
    ndre = (im_aligned[:,:,nir_band] - im_aligned[:,:,rededge_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,rededge_band])
    
    # Mask areas with shadows and low NDVI to remove soil
    masked_ndre = np.ma.masked_where(ndvi < min_display_ndvi, ndre)
    
    ################## Green Normalized Difference Vegetation Index  (𝐺𝑁𝐷𝑉𝐼) ######################
    nir_band = [name.lower() for name in capture.band_names()].index('nir')
    green_band = [name.lower() for name in capture.band_names()].index('green')

    gndvi = (im_aligned[:,:,nir_band] - im_aligned[:,:,green_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,green_band])

    masked_gndvi = np.ma.masked_where(ndvi < min_display_ndvi, gndvi)
    
    #################### Chlorophyll vegetation index  (𝐶𝑉𝐼) #############################

    nir_band = [name.lower() for name in capture.band_names()].index('nir')
    green_band = [name.lower() for name in capture.band_names()].index('green')
    red_band = [name.lower() for name in capture.band_names()].index('red')

    cvi =(im_aligned[:,:,nir_band] / im_aligned[:,:,green_band]) * (im_aligned[:,:,red_band] / im_aligned[:,:,green_band])

    masked_cvi = np.ma.masked_where(ndvi < min_display_ndvi, cvi)
    
    ############### Optimized Soil Adjusted Vegetation Index (𝑂𝑆𝐴𝑉𝐼) ########################

    nir_band = [name.lower() for name in capture.band_names()].index('nir')
    red_band = [name.lower() for name in capture.band_names()].index('red')

    osavi = (im_aligned[:,:,nir_band] - im_aligned[:,:,rededge_band]) / (im_aligned[:,:,nir_band] + im_aligned[:,:,rededge_band] + 0.16)

    # Mask areas with shadows and low NDVI to remove soil
    masked_osavi = np.ma.masked_where(ndvi < min_display_ndvi, osavi)
    
    ############### Simplified Canopy Chlorophyll Content Index (𝑆𝐶𝐶𝐶𝐼) ########################
    sccci =  ndre / ndvi 

    # Mask areas with shadows and low NDVI to remove soil
    masked_sccci = np.ma.masked_where(ndvi < min_display_ndvi, sccci)
    
    return masked_ndvi, masked_ndre, masked_gndvi, masked_cvi,  masked_osavi, masked_sccci, masked_savi,  masked_maci, masked_vari, masked_tcari, masked_ipvi
