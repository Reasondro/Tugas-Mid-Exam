# Computer Vision Assignment - Tugas Individu IF5152

**Name**: Alessandro Jusack Hasian
**NIM**: 18222025
**Course**: IF5152 Computer Vision
**Assignment**: Aplikasi Sederhana Integratif (Materi Minggu 3-6)

---

## 📋 Project Overview

This project implements a comprehensive Computer Vision application integrating four fundamental CV topics:

1. **Image Filtering** - Gaussian and Median filters
2. **Edge Detection & Sampling** - Sobel and Canny edge detectors
3. **Feature/Interest Points** - Harris corner detection
4. **Camera Geometry & Calibration** - Checkerboard calibration and homography transformations

---

## 🗂️ Project Structure

```
AlessandroJusackHasian_18222025_IF5152_TugasIndividuCV/
├── 01_filtering/
│   ├── filtering.py              # Image filtering implementation
│   ├── outputs/                  # Filtered images and comparisons
│   └── parameters.csv            # Filter parameters table
│
├── 02_edge/
│   ├── edge_detection.py         # Edge detection implementation
│   ├── outputs/                  # Edge maps and comparisons
│   └── thresholds.csv            # Threshold parameters table
│
├── 03_featurepoints/
│   ├── feature_detection.py      # Feature points detection
│   ├── outputs/                  # Marked images and heatmaps
│   └── statistics.csv            # Feature detection statistics
│
├── 04_geometry/
│   ├── calibration.py            # Camera calibration
│   ├── create_checkerboard.py    # Checkerboard generator
│   ├── outputs/                  # Calibration and transformation results
│   └── matrices.csv              # Transformation matrices
│
├── utils.py                      # Shared utility functions
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── REPORT_TEMPLATE.md            # Guide for creating the report
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Extract the Project

```bash
cd "path/to/Tugas-Mid-Exam"
cd AlessandroJusackHasian_18222025_IF5152_TugasIndividuCV
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- opencv-python >= 4.8.0
- scikit-image >= 0.21.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- pandas >= 2.0.0
- scipy >= 1.10.0
- Pillow >= 10.0.0

---

## 💻 How to Run

### Running All Modules

You can run each module independently to generate all outputs:

```bash
# Module 1: Image Filtering
cd 01_filtering
python filtering.py

# Module 2: Edge Detection
cd ../02_edge
python edge_detection.py

# Module 3: Feature Points Detection
cd ../03_featurepoints
python feature_detection.py

# Module 4: Camera Geometry & Calibration
cd ../04_geometry
python calibration.py
```

### Running Individual Modules

Each module can be executed independently and will:
1. Load the mandatory test images (cameraman, coins, checkerboard)
2. Apply the CV algorithms with multiple parameter settings
3. Generate output images and visualizations
4. Save parameter tables as CSV files

---

## 📊 Outputs Generated

### Module 1: Image Filtering (01_filtering/)

**Generated Files:**
- Original images (cameraman, coins, checkerboard)
- Gaussian filtered images (σ = 1, 3, 5)
- Median filtered images (kernel = 3, 5, 7)
- Comparison visualizations for each filter type
- `parameters.csv` - Filter parameters and settings

**Key Features:**
- Multiple filter sizes for comparison
- Side-by-side before/after visualizations
- Detailed parameter tracking

### Module 2: Edge Detection (02_edge/)

**Generated Files:**
- Original images
- Sobel edge maps (kernel sizes: 3, 5)
- Canny edge maps (3 threshold sets: 50/150, 100/200, 150/250)
- Individual method comparisons
- Combined Sobel vs Canny comparisons
- `thresholds.csv` - Threshold parameters and edge pixel statistics

**Key Features:**
- Multiple threshold testing
- Edge pixel percentage analysis
- Method comparison visualizations

### Module 3: Feature Points Detection (03_featurepoints/)

**Generated Files:**
- Original images
- Harris corner marked images
- Response heatmaps (showing corner strength)
- Comprehensive visualizations (original, heatmap, marked)
- Threshold comparison charts (0.01, 0.05, 0.10)
- `statistics.csv` - Feature detection statistics

**Key Features:**
- Harris corner detection with adjustable thresholds
- Heatmap visualizations of corner responses
- Statistical analysis (count, mean/max response)
- Multi-threshold comparison

### Module 4: Camera Geometry & Calibration (04_geometry/)

**Generated Files:**
- Original images
- Calibration checkerboard (auto-generated)
- Checkerboard corners detection visualization
- Undistorted checkerboard image
- Homography transformed images (all test images)
- Calibration visualizations
- Homography transformation visualizations
- `matrices.csv` - Camera matrices and transformation matrices

**Key Features:**
- Automatic checkerboard generation (9x6 pattern)
- Camera calibration with intrinsic matrix estimation
- Distortion coefficient calculation
- Homography transformations for perspective change
- Reprojection error analysis

---

## 🔬 Test Images Used

The project uses standard Computer Vision test images from scikit-image:

1. **cameraman.png** (512x512 grayscale)
   - Classic CV benchmark image
   - Good for general filtering and edge detection testing

2. **coins.png** (303x384 grayscale)
   - Coin detection scenario
   - Excellent for edge detection and feature points

3. **checkerboard.png** (200x200 grayscale)
   - Checkerboard pattern
   - Used for geometry transformations

4. **calibration_checkerboard.png** (500x350, auto-generated)
   - Proper 9x6 checkerboard pattern
   - Specifically for camera calibration

---

## ✨ Unique Features Implemented

### 1. Automatic Parameter Comparison
- Each module tests multiple parameter values automatically
- Generates comparison visualizations for easy analysis

### 2. Comprehensive Visualizations
- Side-by-side comparisons
- Heatmaps for feature responses
- Combined method comparisons (e.g., Sobel vs Canny)

### 3. Statistical Analysis
- Edge pixel percentage tracking
- Feature count and response statistics
- Reprojection error calculation

### 4. Modular Code Architecture
- Centralized utility functions (`utils.py`)
- Clean class-based implementations
- Reusable components across modules

### 5. Automatic Checkerboard Generation
- Creates proper calibration pattern automatically
- Eliminates dependency on external calibration images

### 6. CSV Data Export
- All parameters and statistics saved in CSV format
- Easy to import into report tables
- Facilitates further analysis

---

## 📈 Performance Notes

**Execution Time (approximate):**
- Module 1 (Filtering): ~10-15 seconds
- Module 2 (Edge Detection): ~15-20 seconds
- Module 3 (Feature Points): ~20-25 seconds
- Module 4 (Calibration): ~10-15 seconds

**Total: ~1-2 minutes** for all modules

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Cannot import utils"

**Solution:**
Make sure you're running scripts from their respective directories:
```bash
cd 01_filtering
python filtering.py
```

### Issue: Images not displaying

**Solution:**
The scripts save images to the `outputs/` folder. Check there for generated files. Matplotlib windows are automatically closed to prevent blocking.

### Issue: Permission denied

**Solution:**
Ensure you have write permissions in the project directory.

---

## 📝 Notes for Reviewer

1. **All code is runnable** - Each module can be executed independently
2. **No manual intervention needed** - All parameters are pre-configured
3. **Outputs are auto-generated** - Check the `outputs/` folders in each module
4. **CSV files contain all data** - Easy to verify parameters and results

---

## 🔗 Dependencies

This project uses only standard, well-maintained libraries:
- **OpenCV**: Industry-standard computer vision library
- **scikit-image**: Scientific image processing
- **NumPy**: Numerical computing
- **Matplotlib**: Visualization
- **Pandas**: Data manipulation and CSV export

All dependencies are specified in `requirements.txt` with minimum version requirements.

---

## 📚 References

- **OpenCV Documentation**: https://docs.opencv.org/
- **scikit-image Documentation**: https://scikit-image.org/
- **Computer Vision Course Materials**: IF5152 Lectures Week 3-6

---

## 👤 Author Information

- **Name**: Alessandro Jusack Hasian
- **NIM**: 18222025
- **Email**: [Your Email]
- **Course**: IF5152 Computer Vision
- **Institution**: [Your Institution]

---

## 📅 Project Timeline

- **Assignment Start**: [Date]
- **Implementation**: 2 weeks
- **Submission Deadline**: [Deadline Date]

---

## ✅ Checklist

- [x] Module 1: Image Filtering implemented
- [x] Module 2: Edge Detection implemented
- [x] Module 3: Feature Points implemented
- [x] Module 4: Camera Calibration implemented
- [x] All outputs generated successfully
- [x] CSV tables created for all modules
- [x] README documentation complete
- [x] Code is clean and well-commented
- [ ] Report (05_laporan.pdf) to be created by student

---

## 📞 Support

If you encounter any issues running this code:

1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure you're using Python 3.8 or higher
4. Check that you have sufficient disk space for outputs

---

**Last Updated**: October 25, 2025
**Version**: 1.0
**Status**: Complete ✅
