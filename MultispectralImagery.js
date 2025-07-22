// Step 1: Define Time Range
function getDateRangeInput(startDate, endDate) {
  return { dateRange: [startDate, endDate] };
}

var timeRanges = getDateRangeInput('2022-01-01', '2022-12-31');

// Step 2: Load Landsat 8 Multispectral Imagery
var image = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT")
  .filterBounds(geometry)  
  .filterDate(timeRanges.dateRange[0], timeRanges.dateRange[1])
  .filter(ee.Filter.lt('CLOUD_COVER', 1))  
  .select(['B2', 'B3', 'B4', 'B5', 'B6'])  
  .median()  
  .clip(geometry);

// Export Landsat 8 Image
Export.image.toDrive({
  image: image,
  description: 'L8_Data' + timeRanges.dateRange[0].split('-')[0],  
  scale: 30,  
  region: geometry,
  maxPixels: 1e9
});

// Step 3: Load ESA WorldCover Land Cover Mask (2021)
var landCover = ee.Image("ESA/WorldCover/v200/2021")
  .select('Map')
  .clip(geometry)
  .resample('bilinear')  // Resamples to match Landsat-8 resolution
  .reproject({crs: image.projection(), scale: 30});

// Define Land Cover Classes & Colors
var landCoverClasses = {
  'Water': 80,        // Blue
  'Built-up': 50,     // Red
  'Forest': 10,       // Dark Green
  'Vegetation': 40,   // Light Green
  'Barren Land': 60   // Brown
};

var landCoverPalette = {
  80: '#0000FF',  // Water -> Blue
  50: '#FF0000',  // Built-up -> Red
  10: '#006400',  // Forest -> Dark Green
  40: '#00FF00',  // Vegetation -> Light Green
  60: '#8B4513'   // Barren Land -> Brown
};

// Function to Generate Binary Masks
function createLandCoverMask(image, classValue) {
  return image.eq(classValue).selfMask();
}

// Generate Masks for Different Classes
var builtUpMask = createLandCoverMask(landCover, landCoverClasses['Built-up']);
var waterMask = createLandCoverMask(landCover, landCoverClasses['Water']);
var forestMask = createLandCoverMask(landCover, landCoverClasses['Forest']);
var vegetationMask = createLandCoverMask(landCover, landCoverClasses['Vegetation']);
var barrenMask = createLandCoverMask(landCover, landCoverClasses['Barren Land']);

Export.image.toDrive({
  image: builtUpMask,
  description: 'Built_Up_Mask',
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});

Export.image.toDrive({
  image: waterMask,
  description: 'Water_Mask',
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});

Export.image.toDrive({
  image: forestMask,
  description: 'Forest_Mask',
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});

Export.image.toDrive({
  image: vegetationMask,
  description: 'Vegetation_Mask',
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});

Export.image.toDrive({
  image: barrenMask,
  description: 'Barren_Mask',
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});

// Step 4: Display Results
Map.centerObject(geometry, 10);
Map.addLayer(image, {}, 'Landsat 8 Image');
Map.addLayer(waterMask, {palette: [landCoverPalette[80]]}, 'Water');
Map.addLayer(builtUpMask, {palette: [landCoverPalette[50]]}, 'Built-up');
Map.addLayer(forestMask, {palette: [landCoverPalette[10]]}, 'Forest');
Map.addLayer(vegetationMask, {palette: [landCoverPalette[40]]}, 'Vegetation');
Map.addLayer(barrenMask, {palette: [landCoverPalette[60]]}, 'Barren Land');
