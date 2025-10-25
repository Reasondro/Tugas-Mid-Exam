# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Comprehensive camera calibration with homography transformation and reprojection error analysis

"""
Module 4: Camera Geometry & Calibration
Implements checkerboard detection, calibration, and geometric transformations
"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_test_images, save_image

class CameraCalibrator:
    """
    Camera calibration and geometry transformation class
    """

    def __init__(self, output_dir="outputs"):
        """
        Initialize CameraCalibrator

        Args:
            output_dir (str): Directory to save outputs
        """
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.matrices = []

    def detect_checkerboard_corners(self, image, image_name, pattern_size=(9, 6)):
        """
        Detect checkerboard corners

        Args:
            image (numpy.ndarray): Input image
            image_name (str): Name of the image
            pattern_size (tuple): Number of internal corners (cols, rows)

        Returns:
            tuple: (success, corners, marked_image)
        """
        print(f"\n📌 Detecting checkerboard corners on {image_name}...")

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            color_img = image.copy()
        else:
            gray = image.copy()
            color_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        # Find checkerboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            # Refine corner locations
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Draw corners on image
            marked_image = color_img.copy()
            cv2.drawChessboardCorners(marked_image, pattern_size, corners_refined, ret)

            print(f"  ✓ Found {len(corners_refined)} corners")
            return True, corners_refined, marked_image
        else:
            print(f"  ✗ Checkerboard pattern not found")
            return False, None, color_img

    def simple_camera_calibration(self, image, image_name, pattern_size=(9, 6), square_size=1.0):
        """
        Perform simple camera calibration using single checkerboard image

        Args:
            image (numpy.ndarray): Checkerboard image
            image_name (str): Name of the image
            pattern_size (tuple): Number of internal corners
            square_size (float): Size of checkerboard square in arbitrary units

        Returns:
            tuple: (ret, camera_matrix, dist_coeffs, rvecs, tvecs)
        """
        print(f"\n📌 Performing camera calibration on {image_name}...")

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()

        # Prepare object points (3D points in real world space)
        objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
        objp *= square_size

        # Find corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            # Refine corners
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Calibrate camera (using single image)
            objpoints = [objp]
            imgpoints = [corners_refined]

            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                objpoints, imgpoints, gray.shape[::-1], None, None
            )

            if ret:
                print(f"  ✓ Calibration successful!")
                print(f"  ✓ Camera matrix:\n{mtx}")
                print(f"  ✓ Distortion coefficients: {dist.ravel()}")

                # Calculate reprojection error
                mean_error = 0
                imgpoints2, _ = cv2.projectPoints(objp, rvecs[0], tvecs[0], mtx, dist)
                error = cv2.norm(imgpoints[0], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
                print(f"  ✓ Reprojection error: {error:.4f}")

                return ret, mtx, dist, rvecs, tvecs, error
            else:
                print(f"  ✗ Calibration failed")
                return False, None, None, None, None, None
        else:
            print(f"  ✗ Cannot find checkerboard pattern")
            return False, None, None, None, None, None

    def apply_homography_transformation(self, image, image_name):
        """
        Apply homography transformation to simulate perspective change

        Args:
            image (numpy.ndarray): Input image
            image_name (str): Name of the image

        Returns:
            tuple: (transformed_image, homography_matrix)
        """
        print(f"\n📌 Applying homography transformation on {image_name}...")

        h, w = image.shape[:2]

        # Define source points (corners of image)
        src_points = np.float32([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]
        ])

        # Define destination points (perspective transformation)
        # This simulates a camera viewing from an angle
        offset = min(w, h) * 0.15
        dst_points = np.float32([
            [offset, offset],
            [w - offset, offset * 0.5],
            [w - offset * 1.5, h - offset],
            [offset * 0.5, h - offset * 0.5]
        ])

        # Calculate homography matrix
        H, _ = cv2.findHomography(src_points, dst_points)

        # Apply transformation
        transformed = cv2.warpPerspective(image, H, (w, h))

        print(f"  ✓ Homography transformation applied")
        print(f"  ✓ Homography matrix:\n{H}")

        return transformed, H

    def create_calibration_visualization(self, original, corners_img, undistorted, image_name):
        """
        Create calibration visualization

        Args:
            original (numpy.ndarray): Original image
            corners_img (numpy.ndarray): Image with detected corners
            undistorted (numpy.ndarray): Undistorted image
            image_name (str): Name of the image
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Original
        if len(original.shape) == 2:
            axes[0].imshow(original, cmap='gray')
        else:
            axes[0].imshow(original)
        axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        # With corners
        axes[1].imshow(corners_img)
        axes[1].set_title('Detected Corners', fontsize=12, fontweight='bold')
        axes[1].axis('off')

        # Undistorted
        if len(undistorted.shape) == 2:
            axes[2].imshow(undistorted, cmap='gray')
        else:
            axes[2].imshow(undistorted)
        axes[2].set_title('Undistorted Image', fontsize=12, fontweight='bold')
        axes[2].axis('off')

        plt.suptitle(f'Camera Calibration - {image_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()

        output_path = self.output_dir / f"{image_name}_calibration_visualization.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"  ✓ Calibration visualization saved: {output_path.name}")

    def create_homography_visualization(self, original, transformed, H, image_name):
        """
        Create homography transformation visualization

        Args:
            original (numpy.ndarray): Original image
            transformed (numpy.ndarray): Transformed image
            H (numpy.ndarray): Homography matrix
            image_name (str): Name of the image
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))

        # Original
        if len(original.shape) == 2:
            axes[0].imshow(original, cmap='gray')
        else:
            axes[0].imshow(original)
        axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')

        # Transformed
        if len(transformed.shape) == 2:
            axes[1].imshow(transformed, cmap='gray')
        else:
            axes[1].imshow(transformed)
        axes[1].set_title('Perspective Transformed', fontsize=14, fontweight='bold')
        axes[1].axis('off')

        plt.suptitle(f'Homography Transformation - {image_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()

        output_path = self.output_dir / f"{image_name}_homography_visualization.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"  ✓ Homography visualization saved: {output_path.name}")

    def save_matrices_table(self):
        """
        Save transformation matrices to CSV file
        """
        df = pd.DataFrame(self.matrices)
        csv_path = Path(__file__).parent / "matrices.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✅ Matrices table saved: {csv_path}")
        print(f"\nMatrices summary:")
        print(df.to_string(index=False))

def main():
    """
    Main function to run camera calibration experiments
    """
    print("=" * 70)
    print("MODULE 4: CAMERA GEOMETRY & CALIBRATION")
    print("=" * 70)

    # Initialize calibrator
    calibrator = CameraCalibrator()

    # Create proper calibration checkerboard first
    print("\n📐 Creating calibration checkerboard...")
    from create_checkerboard import create_checkerboard
    calib_checkerboard = create_checkerboard(pattern_size=(9, 6), square_size=50)

    # Load test images
    print("\n📂 Loading test images...")
    images = load_test_images()

    # Select test images
    test_images = {
        'cameraman': images['cameraman'],
        'coins': images['coins'],
        'checkerboard': images['checkerboard'],
        'calibration_checkerboard': calib_checkerboard  # Add the proper checkerboard
    }

    # Save original images
    print("\n💾 Saving original images...")
    for name, img in test_images.items():
        output_path = calibrator.output_dir / f"{name}_original.png"
        save_image(img, str(output_path))

    # Process checkerboard for calibration
    print(f"\n{'='*70}")
    print(f"Processing: CALIBRATION CHECKERBOARD (Calibration)")
    print(f"{'='*70}")

    checkerboard_img = test_images['calibration_checkerboard']

    # Detect corners
    ret, corners, marked = calibrator.detect_checkerboard_corners(
        checkerboard_img, 'calibration_checkerboard', pattern_size=(9, 6)
    )

    if ret:
        # Save marked image
        output_path = calibrator.output_dir / "checkerboard_corners_detected.png"
        save_image(marked, str(output_path))

        # Perform calibration
        ret_cal, mtx, dist, rvecs, tvecs, error = calibrator.simple_camera_calibration(
            checkerboard_img, 'calibration_checkerboard', pattern_size=(9, 6)
        )

        if ret_cal:
            # Undistort image
            h, w = checkerboard_img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

            if len(checkerboard_img.shape) == 3:
                gray_check = cv2.cvtColor(checkerboard_img, cv2.COLOR_RGB2GRAY)
            else:
                gray_check = checkerboard_img

            undistorted = cv2.undistort(gray_check, mtx, dist, None, newcameramtx)

            # Save undistorted
            output_path = calibrator.output_dir / "checkerboard_undistorted.png"
            save_image(undistorted, str(output_path))

            # Create visualization
            calibrator.create_calibration_visualization(
                checkerboard_img, marked, undistorted, 'calibration_checkerboard'
            )

            # Store matrix info
            calibrator.matrices.append({
                'Image': 'calibration_checkerboard',
                'Transformation_Type': 'Camera Calibration',
                'Matrix_Type': 'Camera Matrix (K)',
                'Matrix_Values': str(mtx.tolist()),
                'Reprojection_Error': error,
                'Notes': 'Intrinsic camera parameters'
            })

            calibrator.matrices.append({
                'Image': 'calibration_checkerboard',
                'Transformation_Type': 'Camera Calibration',
                'Matrix_Type': 'Distortion Coefficients',
                'Matrix_Values': str(dist.ravel().tolist()),
                'Reprojection_Error': error,
                'Notes': 'Lens distortion parameters'
            })

    # Apply homography transformations to all images
    for name, img in test_images.items():
        print(f"\n{'='*70}")
        print(f"Processing: {name.upper()} (Homography)")
        print(f"{'='*70}")

        # Apply homography
        transformed, H = calibrator.apply_homography_transformation(img, name)

        # Save transformed image
        output_path = calibrator.output_dir / f"{name}_homography_transformed.png"
        save_image(transformed, str(output_path))

        # Create visualization
        calibrator.create_homography_visualization(img, transformed, H, name)

        # Store matrix info
        calibrator.matrices.append({
            'Image': name,
            'Transformation_Type': 'Homography',
            'Matrix_Type': '3x3 Homography Matrix',
            'Matrix_Values': str(H.tolist()),
            'Reprojection_Error': 'N/A',
            'Notes': 'Perspective transformation matrix'
        })

    # Save matrices table
    calibrator.save_matrices_table()

    print("\n" + "=" * 70)
    print("✅ MODULE 4 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n📁 All outputs saved in: {calibrator.output_dir}")
    print("\nGenerated files:")
    print("  - Original images")
    print("  - Checkerboard corners detection")
    print("  - Undistorted checkerboard")
    print("  - Homography transformed images (all)")
    print("  - Calibration visualizations")
    print("  - Homography visualizations")
    print("  - matrices.csv")

if __name__ == "__main__":
    main()
