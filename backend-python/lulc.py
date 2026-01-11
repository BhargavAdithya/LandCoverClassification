import numpy as np
import rasterio
import pandas as pd
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_and_preprocess(image_path):
    """
    Read and preprocess multispectral image
    
    Args:
        image_path (str): Path to the raster image
        
    Returns:
        numpy.ndarray: Preprocessed image array (H, W, Bands)
    """
    try:
        with rasterio.open(image_path) as src:
            image = src.read()
            image = np.moveaxis(image, 0, -1)
            logger.info(f"Loaded image with shape: {image.shape}")
        
        # Normalize to 0-1 range
        image = image.astype(np.float32)
        if image.max() > 1.0:
            image = image / 255.0
        
        return image
    except Exception as e:
        logger.error(f"Error reading image {image_path}: {str(e)}")
        raise


def generate_rgb_preview(image_path, output_path):
    """
    Generate an RGB preview using bands for visualization
    Creates a natural color composite (true color) with transparent background
    
    Args:
        image_path (str): Path to input multispectral image
        output_path (str): Path to save RGB preview
    """
    try:
        with rasterio.open(image_path) as src:
            # Check number of bands available
            num_bands = src.count
            logger.info(f"Image has {num_bands} bands")
            
            if num_bands >= 3:
                # For natural color (true color), typically bands are ordered as:
                # Band 1 = Blue, Band 2 = Green, Band 3 = Red (for many processed TIFs)
                red = src.read(3).astype(np.float64)
                green = src.read(2).astype(np.float64)
                blue = src.read(1).astype(np.float64)
                
                logger.info(f"Using bands 3,2,1 for RGB")
                logger.info(f"Red band - min: {red.min()}, max: {red.max()}, mean: {red.mean()}")
                logger.info(f"Green band - min: {green.min()}, max: {green.max()}, mean: {green.mean()}")
                logger.info(f"Blue band - min: {blue.min()}, max: {blue.max()}, mean: {blue.mean()}")
            elif num_bands == 1:
                # Grayscale image
                gray = src.read(1).astype(np.float64)
                red = green = blue = gray
            else:
                logger.warning("Insufficient bands for RGB preview")
                placeholder = np.zeros((100, 100, 3), dtype=np.uint8)
                Image.fromarray(placeholder).save(output_path)
                return
        
        # Create a mask for valid data (non-zero pixels)
        valid_mask = (red > 0) | (green > 0) | (blue > 0)
        
        # Stack bands
        rgb = np.dstack((red, green, blue))
        
        # Remove any NaN or infinite values
        rgb = np.nan_to_num(rgb, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Apply percentile-based histogram stretch for each band
        for i in range(3):
            band = rgb[:, :, i]
            # Get valid (non-zero) values for percentile calculation
            valid_pixels = band[band > 0]
            
            if len(valid_pixels) > 0:
                # Use 2nd and 98th percentile for contrast stretching
                p2 = np.percentile(valid_pixels, 2)
                p98 = np.percentile(valid_pixels, 98)
                
                logger.info(f"Band {i} - p2: {p2:.2f}, p98: {p98:.2f}")
                
                # Clip and normalize to 0-1 range
                band_clipped = np.clip(band, p2, p98)
                if (p98 - p2) > 0:
                    band_normalized = (band_clipped - p2) / (p98 - p2)
                else:
                    band_normalized = band_clipped
                    
                rgb[:, :, i] = band_normalized
            else:
                rgb[:, :, i] = 0
        
        # Clip to 0-1 range
        rgb = np.clip(rgb, 0, 1)
        
        # Convert to 8-bit
        rgb_8bit = (rgb * 255).astype(np.uint8)
        
        # Create RGBA image with alpha channel for transparency
        rgba = np.dstack((rgb_8bit, np.zeros(rgb_8bit.shape[:2], dtype=np.uint8)))
        
        # Set alpha channel: 255 (opaque) for valid data, 0 (transparent) for no-data
        rgba[:, :, 3] = np.where(valid_mask, 255, 0)
        
        logger.info(f"Final RGBA - shape: {rgba.shape}, valid pixels: {np.sum(valid_mask)}")
        
        # Save image as PNG (supports transparency)
        Image.fromarray(rgba, mode='RGBA').save(output_path)
        logger.info(f"RGB preview with transparency saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error generating RGB preview: {str(e)}", exc_info=True)
        # Create a gray placeholder on error
        placeholder = np.ones((500, 500, 3), dtype=np.uint8) * 128
        Image.fromarray(placeholder).save(output_path)


def apply_histogram_stretch(image, percentile_low=2, percentile_high=98):
    """
    Apply percentile-based histogram stretching for better contrast
    
    Args:
        image (numpy.ndarray): Input image
        percentile_low (int): Lower percentile for clipping
        percentile_high (int): Upper percentile for clipping
        
    Returns:
        numpy.ndarray: Stretched image
    """
    stretched = np.zeros_like(image)
    for i in range(image.shape[-1]):
        band = image[:, :, i]
        p_low = np.percentile(band, percentile_low)
        p_high = np.percentile(band, percentile_high)
        stretched[:, :, i] = np.clip((band - p_low) / (p_high - p_low), 0, 1)
    return stretched


def calculate_ndvi(image):
    """
    Calculate Normalized Difference Vegetation Index
    NDVI = (NIR - Red) / (NIR + Red)
    
    Args:
        image (numpy.ndarray): Multispectral image
        
    Returns:
        numpy.ndarray: NDVI values
    """
    if image.shape[2] < 4:
        logger.warning(f"Insufficient bands for NDVI calculation. Image has {image.shape[2]} bands, need at least 4")
        # Return zeros array as fallback
        return np.zeros((image.shape[0], image.shape[1]))
    
    nir = image[:, :, 3]   # B4 (NIR band)
    red = image[:, :, 2]   # B3 (Red band)
    
    ndvi = (nir - red) / (nir + red + 1e-8)
    return np.clip(ndvi, -1, 1)


def calculate_ndwi(image):
    """
    Calculate Normalized Difference Water Index
    NDWI = (Green - NIR) / (Green + NIR)
    
    Args:
        image (numpy.ndarray): Multispectral image
        
    Returns:
        numpy.ndarray: NDWI values
    """
    if image.shape[2] < 4:
        logger.warning(f"Insufficient bands for NDWI calculation. Image has {image.shape[2]} bands, need at least 4")
        # Return zeros array as fallback
        return np.zeros((image.shape[0], image.shape[1]))
    
    green = image[:, :, 1]  # B2 (Green band)
    nir = image[:, :, 3]    # B4 (NIR band)
    
    ndwi = (green - nir) / (green + nir + 1e-8)
    return np.clip(ndwi, -1, 1)


def calculate_ndbi(image):
    """
    Calculate Normalized Difference Built-up Index
    NDBI = (SWIR - NIR) / (SWIR + NIR)
    
    Args:
        image (numpy.ndarray): Multispectral image
        
    Returns:
        numpy.ndarray: NDBI values
    """
    if image.shape[2] < 5:
        logger.warning(f"Insufficient bands for NDBI calculation. Image has {image.shape[2]} bands, need at least 5")
        # Return zeros array as fallback
        return np.zeros((image.shape[0], image.shape[1]))
    
    swir = image[:, :, 4]   # B5 (SWIR band)
    nir = image[:, :, 3]    # B4 (NIR band)
    
    ndbi = (swir - nir) / (swir + nir + 1e-8)
    return np.clip(ndbi, -1, 1)


def classify_land_cover(ndvi, ndwi, ndbi):
    """
    Classify land cover based on spectral indices
    
    Args:
        ndvi (numpy.ndarray): NDVI values
        ndwi (numpy.ndarray): NDWI values
        ndbi (numpy.ndarray): NDBI values
        
    Returns:
        tuple: Binary masks for (built_up, water, forest, vegetation, barren)
    """
    # Primary classification
    built_up = (ndbi > 0).astype(float)
    forest = (ndvi > 0.5).astype(float)
    vegetation = ((ndvi > 0.1) & (ndvi <= 0.5)).astype(float)
    water = (ndwi > 0).astype(float)
    barren = ((ndvi >= -0.1) & (ndvi <= 0.1)).astype(float)
    
    # Priority-based masking
    vegetation[built_up > 0] = 0
    forest[built_up > 0] = 0
    barren[built_up > 0] = 0
    
    forest[water > 0] = 0
    vegetation[water > 0] = 0
    barren[water > 0] = 0
    built_up[water > 0] = 0
    
    return built_up, water, forest, vegetation, barren


def calculate_land_cover_percentages(built_up, water, forest, vegetation, barren):
    """
    Calculate percentage of each land cover class
    
    Args:
        built_up, water, forest, vegetation, barren (numpy.ndarray): Binary masks
        
    Returns:
        dict: Percentages for each class
    """
    total_pixels = built_up.size
    
    return {
        "Built-up Area": np.sum(built_up) / total_pixels * 100,
        "Water": np.sum(water) / total_pixels * 100,
        "Forest": np.sum(forest) / total_pixels * 100,
        "Vegetation": np.sum(vegetation) / total_pixels * 100,
        "Barren Land": np.sum(barren) / total_pixels * 100
    }


def create_change_map(masks1, masks2, output_path="change_map.png"):
    """
    Create a binary change detection map (white = change, black = no change)
    
    Args:
        masks1 (tuple): Land cover masks from image 1
        masks2 (tuple): Land cover masks from image 2
        output_path (str): Path to save change map
        
    Returns:
        numpy.ndarray: Change map array
    """
    built1, water1, forest1, veg1, bar1 = masks1
    built2, water2, forest2, veg2, bar2 = masks2
    
    # Detect changes with threshold
    change_threshold = 0.1
    
    built_up_change = (np.abs(built2 - built1) > change_threshold)
    water_change = (np.abs(water2 - water1) > change_threshold)
    forest_change = (np.abs(forest2 - forest1) > change_threshold)
    vegetation_change = (np.abs(veg2 - veg1) > change_threshold)
    barren_change = (np.abs(bar2 - bar1) > change_threshold)
    
    # Combine all changes
    total_change = built_up_change | water_change | forest_change | vegetation_change | barren_change
    
    # Create binary change map (white = change, black = no change)
    change_map = np.zeros((total_change.shape[0], total_change.shape[1]), dtype=np.uint8)
    change_map[total_change] = 255  # White for changes
    
    # Save as black and white image
    Image.fromarray(change_map).save(output_path)
    
    logger.info(f"Change map saved to {output_path}")
    return change_map


def generate_comparison_graph(perc1, perc2, output_path="comparison_graph.png", file1_name="Image 1", file2_name="Image 2"):
    """
    Generate a scatter plot comparing land cover percentages between two images
    
    Args:
        perc1 (dict): Land cover percentages for image 1
        perc2 (dict): Land cover percentages for image 2
        output_path (str): Path to save the graph
        file1_name (str): Name of first image file
        file2_name (str): Name of second image file
    """
    categories = list(perc1.keys())
    image1_percentages = list(perc1.values())
    image2_percentages = list(perc2.values())
    
    # Plotting the scatter plot
    plt.figure(figsize=(10, 6))
    
    # Scatter plot for Image 1
    plt.scatter(categories, image1_percentages, marker='o', label=file1_name, color='blue', s=100)
    
    # Scatter plot for Image 2
    plt.scatter(categories, image2_percentages, marker='o', label=file2_name, color='green', s=100)
    
    # Adding labels and title
    plt.xlabel('Land Cover Categories', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.title('Land Cover Changes', fontsize=14)
    
    # Set y-axis scale to 0-100 with intervals of 10
    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))  # Y-axis ticks at intervals of 10
    
    # Display values at each point, dynamically adjusting label positions to avoid overlap
    for i, category in enumerate(categories):
        if image1_percentages[i] > image2_percentages[i]:
            plt.text(i, image1_percentages[i] + 2, f'{image1_percentages[i]:.2f}%', color='blue', ha='center', fontsize=10)
            plt.text(i, image2_percentages[i] + 10, f'{image2_percentages[i]:.2f}%', color='green', ha='center', fontsize=10)
        else:
            plt.text(i, image1_percentages[i] + 10, f'{image1_percentages[i]:.2f}%', color='blue', ha='center', fontsize=10)
            plt.text(i, image2_percentages[i] + 2, f'{image2_percentages[i]:.2f}%', color='green', ha='center', fontsize=10)
    
    # Show gridlines for better visualization
    plt.grid(True)
    
    # Adding a legend to distinguish between Image 1 and Image 2
    plt.legend(loc='upper right')
    
    # Display the plot
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Comparison graph saved to {output_path}")


def run_lulc_change_analysis(image1_path, image2_path, output_dir="./outputs", file1_name="Image 1", file2_name="Image 2"):
    """
    Main function to run complete LULC change detection analysis
    
    Args:
        image1_path (str): Path to first image
        image2_path (str): Path to second image
        output_dir (str): Directory to save outputs
        file1_name (str): Original filename of first image
        file2_name (str): Original filename of second image
        
    Returns:
        dict: Analysis results including percentages and change statistics
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("Starting LULC Change Detection Analysis")
    logger.info(f"File 1: {file1_name}")
    logger.info(f"File 2: {file2_name}")
    logger.info("=" * 60)
    
    # Step 1: Generate RGB previews
    logger.info("STEP 1/7: Generating RGB previews")
    generate_rgb_preview(image1_path, f"{output_dir}/preview_image1.png")
    generate_rgb_preview(image2_path, f"{output_dir}/preview_image2.png")
    
    # Step 2: Read and preprocess images
    logger.info("STEP 2/7: Reading and preprocessing images")
    image1 = read_and_preprocess(image1_path)
    image2 = read_and_preprocess(image2_path)
    
    # Step 3: Calculate spectral indices
    logger.info("STEP 3/7: Calculating spectral indices (NDVI, NDWI, NDBI)")
    ndvi1 = calculate_ndvi(image1)
    ndvi2 = calculate_ndvi(image2)
    ndwi1 = calculate_ndwi(image1)
    ndwi2 = calculate_ndwi(image2)
    ndbi1 = calculate_ndbi(image1)
    ndbi2 = calculate_ndbi(image2)
    
    # Step 4: Classify land cover
    logger.info("STEP 4/7: Classifying land cover")
    masks1 = classify_land_cover(ndvi1, ndwi1, ndbi1)
    masks2 = classify_land_cover(ndvi2, ndwi2, ndbi2)
    
    # Step 5: Create change map
    logger.info("STEP 5/7: Creating change detection map")
    create_change_map(masks1, masks2, f"{output_dir}/change_map.png")
    
    # Step 6: Calculate percentages
    logger.info("STEP 6/7: Calculating land cover percentages")
    perc1 = calculate_land_cover_percentages(*masks1)
    perc2 = calculate_land_cover_percentages(*masks2)
    
    # Calculate changes
    change_stats = {k: perc2[k] - perc1[k] for k in perc1}
    
    # Log results
    logger.info("\n" + "=" * 60)
    logger.info("LAND COVER ANALYSIS RESULTS")
    logger.info("=" * 60)
    for category in perc1.keys():
        logger.info(f"{category:20s} | Image1: {perc1[category]:6.2f}% | Image2: {perc2[category]:6.2f}% | Change: {change_stats[category]:+6.2f}%")
    
    # Step 7: Generate comparison graph and save results
    logger.info("\nSTEP 7/7: Generating comparison graph and saving results")
    generate_comparison_graph(perc1, perc2, f"{output_dir}/comparison_graph.png", file1_name, file2_name)
    
    # Save change matrix
    df = pd.DataFrame({
        "Category": list(perc1.keys()),
        "Image 1 (%)": list(perc1.values()),
        "Image 2 (%)": list(perc2.values()),
        "Change (%)": list(change_stats.values()),
        "Absolute Change (%)": [abs(v) for v in change_stats.values()]
    })
    df.to_csv(f"{output_dir}/change_matrix.csv", index=False)
    
    logger.info("=" * 60)
    logger.info("Analysis Complete!")
    logger.info(f"All outputs saved to: {output_dir}")
    logger.info("=" * 60)
    
    return {
        "image1": perc1,
        "image2": perc2,
        "change": change_stats,
        "total_change_area": sum(abs(v) for v in change_stats.values()) / 2
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        img1_path = sys.argv[1]
        img2_path = sys.argv[2]
        results = run_lulc_change_analysis(img1_path, img2_path)
        print("\nFinal Results:", results)
    else:
        print("Usage: python lulc.py <image1_path> <image2_path>")