# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Multi-method feature detection with response heatmaps and statistical analysis

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils import load_test_images, save_image

class FeatureDetector:
    

    def __init__(self, output_dir="outputs"):
        
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.statistics = []

    def harris_corner_detection(self, image, image_name, block_size=2, ksize=3, k=0.04, threshold_percent=0.01):
        
        print(f"\n Applying Harris corner detection on {image_name}...")

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            color_img = image.copy()
        else:
            gray = image.copy()
            color_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        # Convert to float32
        gray = np.float32(gray)

        # Apply Harris corner detection
        harris_response = cv2.cornerHarris(gray, block_size, ksize, k)

        # Dilate to mark corners
        harris_response = cv2.dilate(harris_response, None)

        # Calculate threshold
        threshold = threshold_percent * harris_response.max()

        # Find corner coordinates
        corner_coords = np.argwhere(harris_response > threshold)

        # Create marked image
        marked_image = color_img.copy()
        marked_image[harris_response > threshold] = [255, 0, 0]  # Red markers

        # Calculate statistics
        num_corners = len(corner_coords)
        mean_response = np.mean(harris_response[harris_response > threshold]) if num_corners > 0 else 0
        max_response = np.max(harris_response)
        min_response = np.min(harris_response[harris_response > threshold]) if num_corners > 0 else 0

        stats = {
            'Image': image_name,
            'Method': 'Harris',
            'Block_Size': block_size,
            'Ksize': ksize,
            'K_Parameter': k,
            'Threshold_Percent': threshold_percent,
            'Threshold_Value': threshold,
            'Feature_Count': num_corners,
            'Mean_Response': mean_response,
            'Max_Response': max_response,
            'Min_Response': min_response
        }

        print(f"   Detected {num_corners} corners")
        print(f"   Mean response: {mean_response:.4f}")
        print(f"   Max response: {max_response:.4f}")

        return marked_image, corner_coords, harris_response, stats

    def create_heatmap(self, response_map, image_name):
        
        plt.figure(figsize=(10, 8))
        plt.imshow(response_map, cmap='hot', interpolation='nearest')
        plt.colorbar(label='Corner Response')
        plt.title(f'Harris Corner Response Heatmap - {image_name}', fontsize=14, fontweight='bold')
        plt.axis('off')

        output_path = self.output_dir / f"{image_name}_harris_heatmap.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Heatmap saved: {output_path.name}")
        return str(output_path)

    def create_visualization(self, original, marked, response_map, image_name, stats):
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Original image
        if len(original.shape) == 2:
            axes[0].imshow(original, cmap='gray')
        else:
            axes[0].imshow(original)
        axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        # Heatmap
        im = axes[1].imshow(response_map, cmap='hot', interpolation='nearest')
        axes[1].set_title('Harris Response Heatmap', fontsize=12, fontweight='bold')
        axes[1].axis('off')
        plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

        # Marked corners
        axes[2].imshow(marked)
        axes[2].set_title(f'Detected Corners: {stats["Feature_Count"]}', fontsize=12, fontweight='bold')
        axes[2].axis('off')

        plt.suptitle(f'Harris Corner Detection - {image_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()

        output_path = self.output_dir / f"{image_name}_harris_visualization.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Visualization saved: {output_path.name}")

    def detect_with_multiple_thresholds(self, image, image_name, thresholds=[0.01, 0.05, 0.1]):
        
        print(f"\n Testing multiple thresholds on {image_name}...")

        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            color_img = image.copy()
        else:
            gray = image.copy()
            color_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        gray = np.float32(gray)

        # Get Harris response once
        harris_response = cv2.cornerHarris(gray, 2, 3, 0.04)
        harris_response = cv2.dilate(harris_response, None)

        results = []
        fig, axes = plt.subplots(1, len(thresholds) + 1, figsize=(5 * (len(thresholds) + 1), 5))

        # Show original
        if len(image.shape) == 2:
            axes[0].imshow(image, cmap='gray')
        else:
            axes[0].imshow(image)
        axes[0].set_title('Original', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        for idx, thresh_pct in enumerate(thresholds, 1):
            threshold = thresh_pct * harris_response.max()
            corner_coords = np.argwhere(harris_response > threshold)
            num_corners = len(corner_coords)

            # Create marked image
            marked = color_img.copy()
            marked[harris_response > threshold] = [255, 0, 0]

            # Display
            axes[idx].imshow(marked)
            axes[idx].set_title(f'Threshold: {thresh_pct}\n{num_corners} corners', fontsize=11, fontweight='bold')
            axes[idx].axis('off')

            results.append({
                'threshold': thresh_pct,
                'count': num_corners,
                'marked': marked
            })

            print(f"   Threshold {thresh_pct}: {num_corners} corners detected")

        plt.suptitle(f'Threshold Comparison - {image_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()

        output_path = self.output_dir / f"{image_name}_threshold_comparison.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Threshold comparison saved: {output_path.name}")

        return results

    def save_statistics_table(self):
        
        df = pd.DataFrame(self.statistics)
        csv_path = Path(__file__).parent / "statistics.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n Statistics table saved: {csv_path}")
        print(f"\nStatistics summary:")
        print(df.to_string(index=False))

def main():
    
    print("=" * 70)
    print("MODULE 3: FEATURE/INTEREST POINTS DETECTION")
    print("=" * 70)

    # Initialize detector
    detector = FeatureDetector()

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

    # Process each image
    for name, img in test_images.items():
        print(f"\n{'='*70}")
        print(f"Processing: {name.upper()}")
        print(f"{'='*70}")

        # Apply Harris corner detection with default threshold
        marked, corners, response, stats = detector.harris_corner_detection(
            img, name,
            block_size=2,
            ksize=3,
            k=0.04,
            threshold_percent=0.01
        )

        # Save marked image
        output_path = detector.output_dir / f"{name}_harris_marked.png"
        save_image(marked, str(output_path))

        # Create heatmap
        detector.create_heatmap(response, name)

        # Create comprehensive visualization
        detector.create_visualization(img, marked, response, name, stats)

        # Test multiple thresholds for analysis
        threshold_results = detector.detect_with_multiple_thresholds(
            img, name, thresholds=[0.01, 0.05, 0.1]
        )

        # Store statistics
        detector.statistics.append(stats)

        # Add threshold comparison statistics
        for thresh_result in threshold_results:
            detector.statistics.append({
                'Image': name,
                'Method': 'Harris (threshold test)',
                'Block_Size': 2,
                'Ksize': 3,
                'K_Parameter': 0.04,
                'Threshold_Percent': thresh_result['threshold'],
                'Threshold_Value': '-',
                'Feature_Count': thresh_result['count'],
                'Mean_Response': '-',
                'Max_Response': '-',
                'Min_Response': '-'
            })

    # Save statistics table
    detector.save_statistics_table()

    print("\n" + "=" * 70)
    print(" MODULE 3 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n All outputs saved in: {detector.output_dir}")
    print("\nGenerated files:")
    print("  - Original images")
    print("  - Harris corner marked images")
    print("  - Response heatmaps")
    print("  - Comprehensive visualizations")
    print("  - Threshold comparison charts")
    print("  - statistics.csv")

if __name__ == "__main__":
    main()
