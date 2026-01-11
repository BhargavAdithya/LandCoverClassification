from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
import logging

from lulc import run_lulc_change_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create outputs directory
OUTPUT_DIR = "./outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def validate_tif_file(file: UploadFile) -> bool:
    """
    Validate if uploaded file is a TIF/TIFF image
    
    Args:
        file (UploadFile): Uploaded file
        
    Returns:
        bool: True if valid TIF file, False otherwise
    """
    filename = file.filename.lower()
    is_valid = filename.endswith(('.tif', '.tiff'))
    logger.info(f"Validating file: {file.filename}, is_valid: {is_valid}")
    return is_valid


@app.post("/analyze")
async def analyze(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """
    Analyze two multispectral images for land cover change detection
    
    Args:
        image1: First TIF image
        image2: Second TIF image
        
    Returns:
        dict: Analysis results and output file paths
    """
    logger.info(f"Received files: {image1.filename}, {image2.filename}")
    logger.info(f"Content types: {image1.content_type}, {image2.content_type}")
    
    # Validate file types
    if not validate_tif_file(image1):
        logger.error(f"Invalid file type for image1: {image1.filename}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type for Image 1: {image1.filename}. Please upload a valid .TIF or .TIFF file."
        )
    
    if not validate_tif_file(image2):
        logger.error(f"Invalid file type for image2: {image2.filename}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type for Image 2: {image2.filename}. Please upload a valid .TIF or .TIFF file."
        )
    
    # Save uploaded files
    image1_path = "image1.tif"
    image2_path = "image2.tif"
    
    try:
        logger.info("Saving uploaded files...")
        
        with open(image1_path, "wb") as f:
            shutil.copyfileobj(image1.file, f)
        
        with open(image2_path, "wb") as f:
            shutil.copyfileobj(image2.file, f)
        
        logger.info(f"Files saved. Size 1: {os.path.getsize(image1_path)} bytes")
        logger.info(f"Files saved. Size 2: {os.path.getsize(image2_path)} bytes")
        
        logger.info("Starting LULC analysis...")
        
        # Run analysis with original filenames
        results = run_lulc_change_analysis(
            image1_path, 
            image2_path, 
            OUTPUT_DIR,
            image1.filename,
            image2.filename
        )
        
        logger.info("Analysis completed successfully")
        
        # Return results and public file URLs
        return {
            "results": results,
            "outputs": {
                "preview_image1": f"/static/preview_image1.png",
                "preview_image2": f"/static/preview_image2.png",
                "change_map": f"/static/change_map.png",
                "comparison_graph": f"/static/comparison_graph.png",
                "change_matrix": f"/static/change_matrix.csv"
            }
        }
    
    except Exception as e:
        logger.error(f"Analysis failed with error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup uploaded temporary files
        if os.path.exists(image1_path):
            os.remove(image1_path)
            logger.info("Cleaned up image1.tif")
        if os.path.exists(image2_path):
            os.remove(image2_path)
            logger.info("Cleaned up image2.tif")


# Serve output files
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")


@app.get("/")
async def root():
    return {"message": "LULC Change Detection API is running"}