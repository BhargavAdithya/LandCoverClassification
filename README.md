# LandCoverClassification
This project uses multispectral images taken by the Landsat-8 satellite at two different times to categorize changes in land cover over time. The spectral indices—NDVI for vegetation, NDWI for water bodies, and NDBI for built-up areas—are calculated as the basis for the classification.
The images, downloaded from Google Earth Engine (refer MultispectralImage.js code), include bands B2, B3, B4, B5, and B6, which are used for calculating NDVI, NDWI, and NDBI. These images are saved in .tif format on Google Drive. The google drive path for the images needs to be updated as per the image location in the google drive. 
# MultispectralImagery
This code downloads multispectral imagery from two different time periods, as specified by the user, for a specific Area of Interst selected or marked on the map.
The user can directly define the Area of Interest (AOI) by drawing a square or polygon on the map. The geometry is automatically saved, and the corresponding indices for that area are exported as a .tif image.
