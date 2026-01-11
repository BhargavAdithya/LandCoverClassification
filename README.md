# 🌍 LULC Change Detection Analysis

<div align="center">

![LULC Banner](https://img.shields.io/badge/LULC-Change%20Detection-purple?style=for-the-badge&logo=satellite)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**Analyze Land Use and Land Cover changes using satellite imagery with AI-powered spectral analysis**

### 🌐 Live Application

**Try it now:** [land-cover-classification-two.vercel.app](https://land-cover-classification-two.vercel.app/)

<img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white" />
<img src="https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white" />

</div>

---

## 📖 What is This Project?

Imagine you have two satellite photos of the same place taken years apart. This smart web application **automatically detects and analyzes** all the changes that happened between those two time periods!

### 🎯 Real-World Example:
Think of your hometown in 2016 vs 2023:
- 🏗️ New buildings and shopping malls constructed
- 🌳 Forests cleared for agriculture
- 💧 Rivers changed their course
- 🏙️ Cities expanded into farmlands

This application **automatically identifies and measures** all these changes using artificial intelligence!

### 💡 Who Can Use This?
- 🏛️ **Government agencies** - Urban planning and monitoring
- 🌱 **Environmental researchers** - Track deforestation and ecosystem changes
- 🏢 **Real estate developers** - Analyze urban growth patterns
- 🎓 **Students & researchers** - Academic projects and studies
- 👨‍💼 **Anyone curious** about how their region has changed over time!

---

## ✨ What Can It Do?

### 🎨 Beautiful & Easy Interface
- **Simple drag-and-drop** - No technical knowledge needed
- **Instant validation** - Ensures you upload correct image formats
- **Smart duplicate detection** - Won't let you compare identical images
- **Live progress tracking** - See the analysis happening in real-time
- **Works everywhere** - Desktop, tablet, or mobile phone

### 🔬 Powerful AI Analysis
The application analyzes satellite images using **three advanced scientific formulas**:

| Index | What It Detects | Scientific Name |
|-------|----------------|----------------|
| 🌱 **NDVI** | Vegetation health & density | Normalized Difference Vegetation Index |
| 💦 **NDWI** | Water bodies & moisture | Normalized Difference Water Index |
| 🏗️ **NDBI** | Built-up areas & cities | Normalized Difference Built-up Index |

### 📊 What You Get

**1. Image Previews** 
- See your satellite images in natural colors
- Compare both images side-by-side

**2. Change Detection Map**
- Black & white map showing exactly where changes occurred
- White areas = Changed
- Black areas = No change

**3. Statistical Table**
Shows percentage of each land type in both images:
- 🏙️ Built-up Area (cities, buildings)
- 💧 Water (rivers, lakes, reservoirs)
- 🌳 Forest (dense tree coverage)
- 🌿 Vegetation (farms, grasslands)
- 🏜️ Barren Land (empty/desert areas)

**4. Comparison Graph**
- Visual chart comparing both time periods
- Color-coded for easy understanding

**5. Change Statistics**
- Total area that changed
- Total area that remained same

### 📥 Download Everything
All results can be downloaded:
- 🖼️ Change detection map (PNG image)
- 📈 Comparison graph (PNG image)
- 📊 Statistical data (CSV spreadsheet)

---

## 🎯 How to Use

### Simple 4-Step Process:

**Step 1:** Visit the application in your web browser

**Step 2:** Upload your first satellite image (from the past - e.g., 2016)
- Click "Choose First Image (.TIF)"
- Select your .TIF file
- ✓ Green checkmark appears when ready

**Step 3:** Upload your second satellite image (from recent time - e.g., 2023)
- Click "Choose Second Image (.TIF)"
- Select another .TIF file of the same area
- ✓ Green checkmark appears when ready

**Step 4:** Click "RUN ANALYSIS" and wait 30-60 seconds!

### 📝 Important Notes:
- ✅ Images must be in **.TIF or .TIFF** format
- ✅ Both images should be of the **same geographical area**
- ✅ Images should be from **different time periods**
- ⚠️ Cannot upload two identical images

---

## 📂 Project Structure

### 🎨 Frontend (User Interface)
**Location**: `frontend/` folder

Built with modern React - this is what users see and interact with. Features beautiful animations, file upload system with validation, real-time progress indicators, and responsive design for all devices.

**Hosted on**: Vercel ✅

---

### ⚙️ Backend (Processing Engine)
**Location**: `backend-python/` folder

The brain of the application - Python-based API that receives images, performs spectral analysis, generates RGB previews, creates change detection maps, and calculates all statistics.

**Key Files**:
- `lulc.py` - Core land cover classification algorithms
- `main.py` - API server and request handling

**Hosted on**: Render ✅

---

## 📓 Research & Development Files

### 1. 📔 `landCoverClassification.ipynb`
**Location**: `notebook/landCoverClassification.ipynb`

**What it is**: 
The **original research notebook** where the entire project was developed and tested in **Google Colab**!

**What's inside**:
- Complete step-by-step analysis code
- All mathematical formulas (NDVI, NDWI, NDBI)
- Image processing techniques
- Classification algorithms
- Visualization code
- Test results with sample images

**Why it matters**: 
Scientists and researchers first develop their ideas in interactive notebooks before building web applications. This notebook was used to test different methods, validate accuracy, and fine-tune thresholds. The code in `backend-python/lulc.py` is directly based on this research!

**Want to explore?**: Open it in [Google Colab](https://colab.research.google.com/) or Jupyter Notebook!

---

### 2. 🛰️ `multispectralImage.js`
**Location**: `notebook/multispectralImage.js`

**What it is**: 
A special script to **download satellite images directly from space**! 🚀

**What it does**:
This JavaScript code connects to **Google Earth Engine** (Google's massive satellite database) and automatically:
- Searches for Landsat 8 satellite images
- Filters by your chosen location (anywhere on Earth!)
- Filters by date range (any time period)
- Removes cloudy images (clouds block the view)
- Downloads clean, ready-to-use images

**Why you need it**:
Getting satellite images isn't simple - NASA satellites take millions of photos, each is several gigabytes in size, and many have cloud cover. This script automates everything and gets you perfect, cloud-free images!

**Example usage**:
```javascript
// Get images of Vijayawada city
var location = ee.Geometry.Rectangle([80.5, 16.4, 80.7, 16.6]);
var image2016 = getCleanImage(location, '2016-01-01', '2016-12-31');
var image2023 = getCleanImage(location, '2023-01-01', '2023-12-31');
```

**How to use**:
1. Visit [Google Earth Engine Code Editor](https://code.earthengine.google.com/)
2. Create a free account
3. Copy-paste this code
4. Change coordinates to your area
5. Run it - images download to your Google Drive!

---

## 🛠️ Technologies Used

### Frontend
- **React** - Modern UI library
- **Axios** - API communication
- **CSS3** - Animations and styling

### Backend
- **FastAPI** - Python web framework
- **Rasterio** - Satellite image processing
- **NumPy** - Mathematical calculations
- **Pandas** - Data analysis
- **Matplotlib** - Graph generation
- **Pillow** - Image manipulation

### Deployment
- **Vercel** - Frontend hosting
- **Render** - Backend API hosting

### Data Sources
- **Google Earth Engine** - Satellite database
- **Landsat 8** - NASA satellite imagery

---

## 🎓 The Science Behind It

### Understanding Satellite Images
Regular photos have 3 colors (Red, Green, Blue). Satellite images have **many more bands** including invisible light that shows vegetation health, water content, and building materials!

### The Magic Formulas

**🌱 NDVI (Vegetation Index)**
```
NDVI = (NIR - Red) / (NIR + Red)
```
Healthy plants reflect lots of Near-Infrared (NIR) light. High value = healthy vegetation 🌳, Low value = bare soil 🏜️

**💦 NDWI (Water Index)**
```
NDWI = (Green - NIR) / (Green + NIR)
```
Water absorbs NIR but reflects green light. High value = water bodies 💧, Low value = land 🏞️

**🏗️ NDBI (Built-up Index)**
```
NDBI = (SWIR - NIR) / (SWIR + NIR)
```
Buildings reflect Short-Wave Infrared (SWIR) more than vegetation. High value = cities 🏙️, Low value = natural areas 🌿

### How Classification Works
The AI examines each pixel and categorizes it based on these index values:
- **Built-up Area**: High NDBI + Low NDVI
- **Water**: High NDWI
- **Forest**: Very High NDVI (>0.6)
- **Vegetation**: Medium NDVI (0.2-0.6)
- **Barren Land**: Low NDVI (-0.1 to 0.2)

---

## 📊 Understanding Your Results

### 🗺️ Change Detection Map
A simple black and white image where **white pixels** show areas that changed, and **black pixels** show areas that stayed the same. You can download this and overlay it on Google Maps to see exactly which neighborhoods or regions transformed!

### 📈 Statistics & Percentages
The app shows you the percentage of each land type in both images. For example, if Built-up Area was 4.50% in 2016 and became 6.24% in 2023, that's a **+1.74% increase** - meaning the city expanded! Similarly, you can track if forests decreased, water bodies changed, or farmlands converted to other uses.

### 📊 Comparison Graph
A visual chart with colored dots showing both time periods at once. Blue dots represent the first image, green dots represent the second image. When dots are far apart, it means big changes happened!

---

## 🎯 Real-World Applications

### 🏛️ Government & Planning
Urban planning, infrastructure monitoring, disaster assessment and policy making with evidence-based data.

### 🌱 Environment & Conservation
Deforestation monitoring, wetland conservation, agricultural monitoring and climate change studies.

### 🏢 Commercial Uses
Real estate investment, insurance risk assessment, agriculture yield prediction and mining exploration.

### 🎓 Education & Research
Academic projects, case studies, thesis research and teaching remote sensing concepts.

---

## 🚦 System Requirements

### For Using the Web App
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Satellite images in .TIF format

**That's it!** No installation needed - just visit the website!

---

## 📄 License

This project is licensed under the MIT License - free to use, modify, and distribute!

---

## 📞 Support & Contact

Need help or have questions?
- 📧 Email: bhargavshorinryu03@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/BhargavAdithya/LandCoverClassification/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/BhargavAdithya/LandCoverClassification/discussions)

---

<div align="center">

### 🌟 Star this project if you find it useful!

**Made with ❤️ for a better understanding of our changing planet**

[⬆ Back to Top](#-lulc-change-detection-analysis)

</div>