// Before running the code, select a region of interest on the map. 
// The selected region will be saved as a geometry in the "geometry" variable.
// This geometry will be used to filter the Landsat 8 image collection.

// Two time periods
var period1 = {
  start: '2021-01-01', // Start date for the first period
  end:   '2021-12-31' // End date for the first period
};

var period2 = {
  start: '2023-01-01', // Start date for the second period
  end:   '2023-12-31' // End date for the second period
};

// ===============================
// FUNCTION TO LOAD LANDSAT 8
// ===============================

function getLandsatImage(startDate, endDate) {
  return ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterBounds(geometry)
    .filterDate(startDate, endDate)
    .filter(ee.Filter.lt('CLOUD_COVER', 5))
    .select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6'])
    .median()
    .clip(geometry)
    .multiply(0.0000275)
    .add(-0.2);
}

// ===============================
// LOAD IMAGES
// ===============================

var image_2021 = getLandsatImage(period1.start, period1.end);
var image_2023 = getLandsatImage(period2.start, period2.end);

// Rename bands
image_2021 = image_2021.rename(['B2', 'B3', 'B4', 'B5', 'B6']);
image_2023 = image_2023.rename(['B2', 'B3', 'B4', 'B5', 'B6']);

// ===============================
// DISPLAY ON MAP
// ===============================

Map.centerObject(geometry, 10);

var visParams = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 0.3
};

Map.addLayer(image_2021, visParams, 'Landsat 8 (2021)');
Map.addLayer(image_2023, visParams, 'Landsat 8 (2023)');

// ===============================
// EXPORT TO GOOGLE DRIVE
// ===============================

Export.image.toDrive({
  image: image_2021,
  description: 'Landsat8_2021_B2_B6',
  folder: 'GEE_Landsat',
  fileNamePrefix: 'Landsat8_2021_B2_B6',
  region: geometry,
  scale: 30,
  crs: 'EPSG:4326',
  maxPixels: 1e13
});

Export.image.toDrive({
  image: image_2023,
  description: 'Landsat8_2023_B2_B6',
  folder: 'GEE_Landsat',
  fileNamePrefix: 'Landsat8_2023_B2_B6',
  region: geometry,
  scale: 30,
  crs: 'EPSG:4326',
  maxPixels: 1e13
});