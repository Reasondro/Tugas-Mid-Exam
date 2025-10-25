# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Multi-threshold edge detection comparison with automatic threshold selection

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_test_images, save_image

class EdgeDetector:
    

    def __init__(self, output_dir="outputs"):
        
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.thresholds = []

    def apply_sobel(self, image, image_name, ksize_values=[3, 5]):
        
        print(f"\n Applying Sobel edge detection on {image_name}...")
        results = []

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()

        for ksize in ksize_values:
            # Compute Sobel gradients in X and Y directions
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

            # Compute magnitude
            sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

            # Normalize to 0-255
            sobel_magnitude = np.uint8(255 * sobel_magnitude / np.max(sobel_magnitude))

            # Save output
            output_path = self.output_dir / f"{image_name}_sobel_k{ksize}.png"
            save_image(sobel_magnitude, str(output_path))

            # Store threshold info
            self.thresholds.append({
                'Image': image_name,
                'Method': 'Sobel',
                'Kernel_Size': ksize,
                'Threshold_Low': 'N/A',
                'Threshold_High': 'N/A',
                'Notes': f'Magnitude-based, kernel={ksize}x{ksize}',
                'Output_File': output_path.name
            })

            results.append(sobel_magnitude)
            print(f"   Sobel (kernel={ksize}x{ksize}) applied")

        return results

    def apply_canny(self, image, image_name, threshold_sets=None):
        
        if threshold_sets is None:
            # Default threshold sets: (low, high)
            threshold_sets = [
                (50, 150),   # Low sensitivity
                (100, 200),  # Medium sensitivity
                (150, 250)   # High sensitivity
            ]

        print(f"\n Applying Canny edge detection on {image_name}...")
        results = []

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()

        # Apply Gaussian blur for noise reduction
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)

        for low_thresh, high_thresh in threshold_sets:
            # Apply Canny edge detection
            edges = cv2.Canny(blurred, low_thresh, high_thresh)

            # Save output
            output_path = self.output_dir / f"{image_name}_canny_t{low_thresh}_{high_thresh}.png"
            save_image(edges, str(output_path))

            # Count edge pixels for analysis
            edge_pixel_count = np.sum(edges > 0)
            edge_percentage = (edge_pixel_count / edges.size) * 100

            # Store threshold info
            self.thresholds.append({
                'Image': image_name,
                'Method': 'Canny',
                'Kernel_Size': '5x5 (Gaussian pre-blur)',
                'Threshold_Low': low_thresh,
                'Threshold_High': high_thresh,
                'Notes': f'Edge pixels: {edge_pixel_count} ({edge_percentage:.2f}%)',
                'Output_File': output_path.name
            })

            results.append(edges)
            print(f"   Canny (low={low_thresh}, high={high_thresh}) - {edge_percentage:.2f}% edges")

        return results

    def create_sobel_visualization(self, original, sobel_results, ksize_values, image_name):
        
        n_images = len(sobel_results) + 1
        fig, axes = plt.subplots(1, n_images, figsize=(5 * n_images, 5))

        # Ensure original is grayscale for display
        if len(original.shape) == 3:
            display_original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        else:
            display_original = original

        # Display original
        axes[0].imshow(display_original, cmap='gray')
        axes[0].set_title('Original', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        # Display Sobel results
        for i, (sobel, ksize) in enumerate(zip(sobel_results, ksize_values), 1):
            axes[i].imshow(sobel, cmap='gray')
            axes[i].set_title(f'Sobel (k={ksize})', fontsize=12, fontweight='bold')
            axes[i].axis('off')

        plt.suptitle(f'Sobel Edge Detection - {image_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save visualization
        output_path = self.output_dir / f"{image_name}_sobel_comparison.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Sobel visualization saved: {output_path.name}")

    def create_canny_visualization(self, original, canny_results, threshold_sets, image_name):
        
        n_images = len(canny_results) + 1
        fig, axes = plt.subplots(1, n_images, figsize=(5 * n_images, 5))

        # Ensure original is grayscale for display
        if len(original.shape) == 3:
            display_original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        else:
            display_original = original

        # Display original
        axes[0].imshow(display_original, cmap='gray')
        axes[0].set_title('Original', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        # Display Canny results
        for i, (edges, (low, high)) in enumerate(zip(canny_results, threshold_sets), 1):
            axes[i].imshow(edges, cmap='gray')
            axes[i].set_title(f'Canny\n({low}, {high})', fontsize=12, fontweight='bold')
            axes[i].axis('off')

        plt.suptitle(f'Canny Edge Detection - {image_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save visualization
        output_path = self.output_dir / f"{image_name}_canny_comparison.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Canny visualization saved: {output_path.name}")

    def create_combined_visualization(self, original, sobel_result, canny_result, image_name):
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Ensure original is grayscale for display
        if len(original.shape) == 3:
            display_original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        else:
            display_original = original

        # Original
        axes[0].imshow(display_original, cmap='gray')
        axes[0].set_title('Original', fontsize=14, fontweight='bold')
        axes[0].axis('off')

        # Sobel
        axes[1].imshow(sobel_result, cmap='gray')
        axes[1].set_title('Sobel Edge Detection', fontsize=14, fontweight='bold')
        axes[1].axis('off')

        # Canny
        axes[2].imshow(canny_result, cmap='gray')
        axes[2].set_title('Canny Edge Detection', fontsize=14, fontweight='bold')
        axes[2].axis('off')

        plt.suptitle(f'Edge Detection Comparison - {image_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()

        # Save
        output_path = self.output_dir / f"{image_name}_combined_comparison.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Combined visualization saved: {output_path.name}")

    def save_thresholds_table(self):
        
        df = pd.DataFrame(self.thresholds)
        csv_path = Path(__file__).parent / "thresholds.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n Thresholds table saved: {csv_path}")
        print(f"\nThresholds summary:")
        print(df.to_string(index=False))

def main():
    
    print("=" * 70)
    print("MODULE 2: EDGE DETECTION & SAMPLING")
    print("=" * 70)

    # Initialize edge detector
    detector = EdgeDetector()

    # Load test images
    print("\n Loading test images...")
    images = load_test_images()

    # Select mandatory test images
    test_images = {
        'cameraman': images['cameraman'],
        'coins': images['coins'],
        'checkerboard': images['checkerboard']
    }

    # Save original images for reference
    print("\n Saving original images...")
    for name, img in test_images.items():
        output_path = detector.output_dir / f"{name}_original.png"
        save_image(img, str(output_path))

    # Define parameters
    sobel_ksize = [3, 5]
    canny_thresholds = [
        (50, 150),   # Low sensitivity
        (100, 200),  # Medium sensitivity
        (150, 250)   # High sensitivity
    ]

    # Process each image
    for name, img in test_images.items():
        print(f"\n{'='*70}")
        print(f"Processing: {name.upper()}")
        print(f"{'='*70}")

        # Apply Sobel
        sobel_results = detector.apply_sobel(img, name, sobel_ksize)
        detector.create_sobel_visualization(img, sobel_results, sobel_ksize, name)

        # Apply Canny
        canny_results = detector.apply_canny(img, name, canny_thresholds)
        detector.create_canny_visualization(img, canny_results, canny_thresholds, name)

        # Create combined comparison (use middle results)
        detector.create_combined_visualization(
            img,
            sobel_results[0],  # First Sobel result
            canny_results[1],  # Middle Canny result
            name
        )

    # Save thresholds table
    detector.save_thresholds_table()

    print("\n" + "=" * 70)
    print(" MODULE 2 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n All outputs saved in: {detector.output_dir}")
    print("\nGenerated files:")
    print("  - Original images")
    print("  - Sobel edge maps (kernel sizes: 3, 5)")
    print("  - Canny edge maps (3 threshold sets)")
    print("  - Individual method comparisons")
    print("  - Combined comparisons (Sobel vs Canny)")
    print("  - thresholds.csv")

if __name__ == "__main__":
    main()
