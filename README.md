# 🌍 LULC Change Detection Analysis

<div align="center">

![LULC Banner](https://img.shields.io/badge/LULC-Change%20Detection-purple?style=for-the-badge&logo=satellite)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**Analyze Land Use and Land Cover changes using satellite imagery with AI-powered spectral analysis**

[🚀 Live Application](https://land-cover-classification-two.vercel.app/) | [📡 API Endpoint](https://landcoverclassification.onrender.com)

<img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white" />
<img src="https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white" />

---

### 🌐 Live Deployment Status

| Component | URL | Status |
|-----------|-----|--------|
| **🎨 Frontend** | [land-cover-classification-two.vercel.app](https://land-cover-classification-two.vercel.app/) | ✅ **Live & Running** |
| **⚙️ Backend API** | [landcoverclassification.onrender.com](https://landcoverclassification.onrender.com) | ✅ **Live & Running** |

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

## 🎯 How to Use the Application

### Simple 4-Step Process:

**Step 1: Open the Application**
Visit: [land-cover-classification-two.vercel.app](https://land-cover-classification-two.vercel.app/)

**Step 2: Upload First Image**
- Click on "Choose First Image (.TIF)"
- Select your satellite image from 2016 (or any past date)
- You'll see a ✓ checkmark when uploaded successfully

**Step 3: Upload Second Image**
- Click on "Choose Second Image (.TIF)"
- Select your satellite image from 2023 (or any recent date)
- You'll see a ✓ checkmark when uploaded successfully

**Step 4: Analyze!**
- Click the "RUN ANALYSIS" button
- Wait 30-60 seconds while AI processes your images
- View all the results on the same page!

### 📝 Important Notes:
- ✅ Images must be in **.TIF or .TIFF** format
- ✅ Both images should be of the **same geographical area**
- ✅ Images should be from **different time periods**
- ⚠️ Cannot upload two identical images

---

## 📂 Project Components

### 🎨 Frontend (User Interface)
**Location**: `frontend/` folder

Built with modern React, this is what users see and interact with:
- Beautiful animated interface
- File upload system with validation
- Real-time progress indicators
- Interactive result displays
- Responsive design for all devices

**Hosted on**: Vercel ✅

---

### ⚙️ Backend (Processing Engine)
**Location**: `backend-python/` folder

The brain of the application - Python-based API that:
- Receives uploaded satellite images
- Performs spectral analysis using scientific algorithms
- Generates RGB previews from multispectral data
- Creates change detection maps
- Calculates statistics and percentages
- Returns all results to the frontend

**Key Files**:
- `lulc.py` - Core land cover classification algorithms
- `main.py` - API server and request handling

**Hosted on**: Render ✅

---

## 📓 Research & Development Files

### 1. 📔 `landCoverClassification.ipynb`
**Location**: `notebook/landCoverClassification.ipynb`

**What it is**: 
This is the **original research notebook** where the entire project was developed and tested!

**What's inside**:
- Complete step-by-step analysis code
- All the mathematical formulas (NDVI, NDWI, NDBI)
- Image processing techniques
- Classification algorithms
- Visualization code
- Test results with sample images

**How it was used**:
Scientists and researchers first develop their ideas in these interactive notebooks before building web applications. This notebook was created in **Google Colab** (a free online Python environment) to:
- Test different analysis methods
- Validate accuracy of results
- Fine-tune classification thresholds
- Generate visualizations

**For developers**: The code in `backend-python/lulc.py` is directly based on this notebook!

**Want to explore?**: Open it in [Google Colab](https://colab.research.google.com/) or Jupyter Notebook to see the research process!

---

### 2. 🛰️ `multispectralImage.js`
**Location**: `notebook/multispectralImage.js`

**What it is**: 
A special script to **download satellite images directly from space**! 🚀

**What's inside**:
JavaScript code that connects to **Google Earth Engine** (Google's massive satellite database) to:
- Search for Landsat 8 satellite images
- Filter by location (any place on Earth!)
- Filter by date (any time period)
- Remove cloudy images (clouds block the view)
- Process and download clean images

**Why it's needed**:
To analyze land changes, you need satellite images! But getting these images isn't simple:
- NASA satellites take millions of photos
- Each photo is several gigabytes in size
- Images often have cloud cover
- Need specialized software to access them

This script **automates everything** and gets you perfect, cloud-free images!

**How it works**:
```javascript
// Example: Get images of Vijayawada city
var location = ee.Geometry.Rectangle([80.5, 16.4, 80.7, 16.6]);
var image2016 = getCleanImage(location, '2016-01-01', '2016-12-31');
var image2023 = getCleanImage(location, '2023-01-01', '2023-12-31');
// Downloads ready-to-use satellite images!
```

**Want to use it?**:
1. Go to [Google Earth Engine Code Editor](https://code.earthengine.google.com/)
2. Create a free account
3. Copy-paste the code from this file
4. Change the coordinates to your area of interest
5. Run it - images download to your Google Drive!

---

## 🛠️ Technologies Powering This App

### 🎨 Frontend Technologies
- **React** - Modern JavaScript library for beautiful interfaces
- **Axios** - Handles communication with backend
- **CSS3** - Advanced animations and styling

### ⚙️ Backend Technologies
- **FastAPI** - Lightning-fast Python web framework
- **Rasterio** - Reads and processes satellite images
- **NumPy** - Mathematical calculations
- **Pandas** - Data analysis and statistics
- **Matplotlib** - Creates graphs and visualizations
- **Pillow** - Image processing and manipulation

### 🚀 Deployment
- **Vercel** - Hosts the frontend (free, fast, reliable)
- **Render** - Hosts the backend API (free tier)

### 🛰️ Data Sources
- **Google Earth Engine** - Satellite image database
- **Landsat 8** - NASA satellite providing free imagery
- **Google Colab** - Free cloud computing for research

---

## 🎓 How Does The Science Work?

### Understanding Satellite Images

Regular photos have 3 colors (Red, Green, Blue). Satellite images have **many more bands** including invisible light like:
- Near-Infrared (NIR) - shows vegetation health
- Short-Wave Infrared (SWIR) - shows water content and buildings

### The Magic Formulas

**🌱 NDVI (Vegetation Index)**
```
NDVI = (NIR - Red) / (NIR + Red)
```
- Healthy plants reflect lots of NIR light
- Value ranges: -1 to +1
- High value = healthy vegetation 🌳
- Low value = bare soil or buildings 🏜️

**💦 NDWI (Water Index)**
```
NDWI = (Green - NIR) / (Green + NIR)
```
- Water absorbs NIR but reflects green light
- Value ranges: -1 to +1
- High value = water bodies 💧
- Low value = land 🏞️

**🏗️ NDBI (Built-up Index)**
```
NDBI = (SWIR - NIR) / (SWIR + NIR)
```
- Buildings reflect SWIR more than vegetation
- Value ranges: -1 to +1
- High value = cities and buildings 🏙️
- Low value = natural areas 🌿

### Classification Logic

The AI categorizes each pixel based on these index values:
- **Built-up Area**: High NDBI + Low NDVI
- **Water**: High NDWI
- **Forest**: Very High NDVI (>0.6)
- **Vegetation**: Medium NDVI (0.2-0.6)
- **Barren Land**: Low NDVI (-0.1 to 0.2)

---

## 📊 Understanding Your Results

### The Change Map
- **White pixels** = Something changed here!
- **Black pixels** = No change detected
- Download and overlay on Google Maps for geographic context

### The Statistics Table
Example output:
| Category | Image 1 (2016) | Image 2 (2023) | Change |
|----------|----------------|----------------|--------|
| Built-up Area | 4.50% | 6.24% | **+1.74%** ⬆️ |
| Water | 0.07% | 0.12% | **+0.05%** ⬆️ |
| Forest | 0.01% | 0.01% | 0.00% ➡️ |
| Vegetation | 0.00% | 0.00% | 0.00% ➡️ |
| Barren Land | 0.11% | 0.15% | **+0.04%** ⬆️ |

**Interpretation**: 
- Urban area increased by 1.74% (city expansion!)
- Water bodies slightly increased (new reservoir?)
- Forest remained stable

---

## 🚦 System Requirements

### For Using the Web App
- **Any modern web browser** (Chrome, Firefox, Safari, Edge)
- **Internet connection**
- **Satellite images in .TIF format**

That's it! No installation needed - just visit the website!

### For Developers (Running Locally)
- Python 3.8 or higher
- Node.js 14 or higher
- 4GB RAM minimum
- 2GB free disk space

---

## 🎯 Real-World Applications

### 🏛️ Government & Planning
- **Urban planning** - Track city expansion
- **Infrastructure monitoring** - Roads, dams, airports
- **Disaster assessment** - Flood impact, fire damage
- **Policy making** - Evidence-based decisions

### 🌱 Environment & Conservation
- **Deforestation monitoring** - Illegal logging detection
- **Wetland conservation** - Track water body changes
- **Agricultural monitoring** - Crop health assessment
- **Climate change studies** - Long-term land cover trends

### 🏢 Commercial Uses
- **Real estate** - Investment opportunity identification
- **Insurance** - Risk assessment and claims verification
- **Agriculture** - Yield prediction and monitoring
- **Mining** - Resource exploration and impact assessment

### 🎓 Education & Research
- **Academic projects** - Geography, environmental science
- **Case studies** - Urban development patterns
- **Thesis research** - Land use change analysis
- **Teaching tool** - Remote sensing education

---

## 🎨 Screenshots & Examples

### Upload Interface
Clean and intuitive - just drag and drop your images!

### Analysis in Progress
Watch as the AI processes your images with real-time updates.

### Results Dashboard
Comprehensive results with multiple visualization options.

---

## 🤝 Contributing

This is an open-source project! Contributions are welcome:
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code improvements

---

## 📄 License

This project is licensed under the MIT License - free to use, modify, and distribute!

---

## 📞 Support & Contact

Need help or have questions?
- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/lulc-app/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/lulc-app/discussions)

---

## 🙏 Acknowledgments

- **NASA** - For free Landsat 8 satellite imagery
- **Google Earth Engine** - For powerful satellite data processing
- **USGS** - For maintaining satellite image archives
- **Open Source Community** - For amazing tools and libraries

---

<div align="center">

### 🌟 Star this project if you find it useful!

**Made with ❤️ for a better understanding of our changing planet**

[⬆ Back to Top](#-lulc-change-detection-analysis)

</div>