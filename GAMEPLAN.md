# Computer Vision Assignment - Implementation Game Plan

**Course**: IF5152 Computer Vision
**Assignment**: Tugas Individu - Aplikasi Sederhana Integratif (Materi Minggu 3-6)
**Deadline**: 2 weeks
**Date Created**: 2025-10-24

---

## 📋 Project Overview

Create an integrated Computer Vision application that implements:
1. **Image Filtering** (Gaussian, Median/Sobel)
2. **Edge Detection & Sampling** (Sobel, Canny)
3. **Feature/Interest Points** (Harris, SIFT, or FAST)
4. **Camera Geometry & Calibration** (Checkerboard-based)

---

## 🎯 Main Objectives

- ✅ Complete all 4 CV modules with working code
- ✅ Use mandatory test images (cameraman, coins, checkerboard)
- ✅ Generate all required outputs (images, tables, parameters)
- ✅ Create proper folder structure
- ✅ Write comprehensive documentation
- ✅ Prepare report template with analysis sections

---

## 📁 Required Folder Structure

```
Nama_NIM_IF5152_TugasIndividuCV/
├── 01_filtering/
│   ├── filtering.py (or .ipynb)
│   ├── outputs/
│   │   ├── cameraman_original.png
│   │   ├── cameraman_gaussian.png
│   │   ├── cameraman_median.png
│   │   ├── coins_original.png
│   │   ├── coins_gaussian.png
│   │   └── ... (all filtered outputs)
│   └── parameters.csv
│
├── 02_edge/
│   ├── edge_detection.py (or .ipynb)
│   ├── outputs/
│   │   ├── cameraman_sobel.png
│   │   ├── cameraman_canny.png
│   │   └── ... (all edge detection outputs)
│   └── thresholds.csv
│
├── 03_featurepoints/
│   ├── feature_detection.py (or .ipynb)
│   ├── outputs/
│   │   ├── cameraman_harris_marked.png
│   │   └── ... (all feature marked outputs)
│   └── statistics.csv
│
├── 04_geometry/
│   ├── calibration.py (or .ipynb)
│   ├── outputs/
│   │   ├── checkerboard_overlay.png
│   │   └── transformation_result.png
│   └── matrices.csv
│
├── 05_laporan.pdf (TO BE CREATED BY STUDENT)
├── README.md
└── requirements.txt
```

---

## 🗓️ Implementation Timeline

### Phase 1: Setup & Foundation (30 min)
**Status**: IN PROGRESS

- [ ] Create folder structure
- [ ] Install required libraries
- [ ] Load and verify test images (cameraman, coins, checkerboard)
- [ ] Create requirements.txt
- [ ] Setup utility functions for saving outputs

**Deliverables**:
- Folder structure created
- Test images loaded successfully
- requirements.txt

---

### Phase 2: Module 1 - Image Filtering (30 min)
**Status**: PENDING

**Requirements**:
- Implement at least 2 different filters: Gaussian & Median
- Process all test images (cameraman, coins, checkerboard)
- Generate before/after comparisons
- Create parameter table (CSV)

**Implementation Steps**:
1. Create `01_filtering/filtering.py`
2. Implement Gaussian filter with different sigma values
3. Implement Median filter with different kernel sizes
4. Apply filters to all test images
5. Save outputs with clear naming
6. Generate parameters.csv with columns: [Image, Filter_Type, Parameter_Name, Parameter_Value]

**Code Structure**:
```python
# Header comment with Name, NIM, Fitur unik
# Import libraries
# Load images
# Apply Gaussian filter
# Apply Median filter
# Save outputs
# Generate parameter table
```

**Deliverables**:
- `filtering.py` with clean, commented code
- Before/after images in `outputs/`
- `parameters.csv`

---

### Phase 3: Module 2 - Edge Detection (30 min)
**Status**: PENDING

**Requirements**:
- Implement 2 methods: Sobel & Canny
- Test with different thresholds/parameters
- Apply to all test images
- Create threshold/sampling table

**Implementation Steps**:
1. Create `02_edge/edge_detection.py`
2. Implement Sobel edge detection
3. Implement Canny edge detection with multiple thresholds
4. Apply to all test images
5. Save edge maps
6. Generate thresholds.csv with columns: [Image, Method, Threshold_Low, Threshold_High, Notes]

**Deliverables**:
- `edge_detection.py`
- Edge detection outputs in `outputs/`
- `thresholds.csv`

---

### Phase 4: Module 3 - Feature Points (40 min)
**Status**: PENDING

**Requirements**:
- Detect features using Harris corner detection
- Mark features on images
- Generate statistics (count, response values)

**Implementation Steps**:
1. Create `03_featurepoints/feature_detection.py`
2. Implement Harris corner detection
3. Mark detected corners on images
4. Calculate statistics (number of features, mean/max response)
5. Save marked images
6. Generate statistics.csv with columns: [Image, Method, Feature_Count, Mean_Response, Max_Response, Threshold_Used]

**Deliverables**:
- `feature_detection.py`
- Marked images in `outputs/`
- `statistics.csv`

---

### Phase 5: Module 4 - Camera Geometry & Calibration (40 min)
**Status**: PENDING

**Requirements**:
- Checkerboard corner detection
- Calculate transformation matrix
- Show overlay/projection results
- Save matrix parameters

**Implementation Steps**:
1. Create `04_geometry/calibration.py`
2. Detect checkerboard corners
3. Perform simple calibration or homography
4. Apply transformation
5. Generate overlay visualization
6. Save transformation matrices
7. Generate matrices.csv with transformation parameters

**Deliverables**:
- `calibration.py`
- Overlay images in `outputs/`
- `matrices.csv`

---

### Phase 6: Documentation (30 min)
**Status**: PENDING

**Requirements**:
- Comprehensive README.md with installation & running instructions
- Report template (Markdown format) to help fill 05_laporan.pdf

**README.md Contents**:
1. Project title and description
2. Installation instructions
3. How to run each module
4. Expected outputs
5. Dependencies
6. Unique features implemented

**Report Template Contents**:
1. Cover page guidance
2. Table of contents structure
3. Workflow pipeline section
4. Process & results template for each module
5. Parameter analysis prompts
6. Comparison & reflection sections
7. Tips for filling each section

**Deliverables**:
- `README.md`
- `REPORT_TEMPLATE.md` (guide for creating 05_laporan.pdf)

---

## 📊 Grading Rubric Reference

| Aspect | Weight | Requirements |
|--------|--------|--------------|
| Filtering | 15% | 2 filters, before/after outputs, parameter table |
| Edge Detection | 15% | 2 methods, threshold effects, outputs & table on all images |
| Feature Points | 15% | Marking, statistics, parameter analysis |
| Geometry/Calib | 15% | Overlay results, transformation matrix, clear parameters |
| Modular Code | 10% | Folder structure, documentation, runnable scripts |
| Report Structure | 15% | Cover, TOC, subsections, images, tables, parameter analysis |
| Reflection/Innovation | 15% | Comparison, personal design narrative, innovations, error solutions |

**Total**: 100%

---

## 🔧 Technical Stack

**Required Libraries**:
- Python 3.8+
- OpenCV (`cv2`)
- scikit-image (`skimage`)
- NumPy
- Matplotlib
- Pandas (for CSV tables)

---

## ✨ Unique Features to Implement

To get extra points in "Reflection/Innovation" (15%):

1. **Interactive parameter tuning** (if using Jupyter notebook)
2. **Side-by-side comparison visualizations**
3. **Automatic parameter optimization** (find best threshold, etc.)
4. **Performance metrics** (execution time, quality scores)
5. **Additional test on personal images** (1-2 bonus images)
6. **Color image handling** (if applicable)

---

## 🚨 Important Notes

1. **MANDATORY**: Use cameraman.png, coins.png, checkerboard.png for ALL features
2. **Optional**: Add 1-2 personal images for bonus exploration
3. **Format**: Strictly follow folder structure (score = 0 if wrong format!)
4. **Code Header**: Every script must have:
   ```python
   # Nama: [Your Name]
   # NIM: [Your NIM]
   # Fitur unik: [Unique features you implemented]
   ```
5. **Documentation**: README must allow reviewer to run all scripts
6. **Report**: Minimum 10 pages, follow exact structure from assignment

---

## 📝 Checklist Before Submission

- [ ] All 4 modules implemented and tested
- [ ] Folder structure exactly matches requirements
- [ ] All code files have proper headers
- [ ] All outputs generated successfully
- [ ] CSV/table files created for each module
- [ ] README.md complete with instructions
- [ ] Report template provided with guidance
- [ ] Code is modular and well-commented
- [ ] All scripts can be run by reviewer
- [ ] Personal reflection and analysis notes prepared

---

## 🎓 Student Tasks After Implementation

After I complete the code implementation, YOU need to:

1. **Review and test** all scripts
2. **Add personal images** (optional, for bonus)
3. **Run all modules** and verify outputs
4. **Fill in personal analysis** in each CSV/table
5. **Create 05_laporan.pdf** using the template provided:
   - Write theoretical explanations
   - Add screenshots from outputs
   - Analyze parameter effects
   - Write comparison section
   - Add personal reflection on design choices
   - Document any errors/challenges faced
6. **Add your Name & NIM** to all code headers
7. **Final review** before submission

---

## 📞 Questions to Answer in Report

For each module, analyze:

1. **Filtering**: How do different filter sizes affect the output? Gaussian vs Median trade-offs?
2. **Edge Detection**: How do threshold values affect edge detection? Sobel vs Canny differences?
3. **Feature Points**: How many features detected? Why more/less on different images?
4. **Calibration**: What transformation matrix was obtained? What does it represent?

---

## 🏁 Success Criteria

✅ All code runs without errors
✅ All outputs generated in correct folders
✅ All tables/CSV files created
✅ Code is clean, modular, and commented
✅ README explains everything clearly
✅ Report template helps structure the PDF
✅ Student can explain the code and results

---

**Last Updated**: 2025-10-24
**Status**: Phase 1 - IN PROGRESS
