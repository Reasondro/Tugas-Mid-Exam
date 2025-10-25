# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Automatic parameter comparison with multiple filter sizes and visualization

# Module 1: Image Filtering
# Gaussian and Median filters

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils import load_test_images, save_image, create_comparison_plot

class ImageFilter:
    # Image filtering with Gaussian and Median

    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.parameters = []

    def apply_gaussian_filter(self, image, image_name, sigma_values=[1, 3, 5]):
        # Apply Gaussian with different sigmas
        print(f"\nApplying Gaussian filter on {image_name}...")
        results = []

        # Ensure image is grayscale for consistent processing
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray_image = image.copy()

        for sigma in sigma_values:
            # Calculate kernel size from sigma (must be odd)
            ksize = int(6 * sigma + 1)
            if ksize % 2 == 0:
                ksize += 1

            # Apply Gaussian filter
            filtered = cv2.GaussianBlur(gray_image, (ksize, ksize), sigma)

            # Save output
            output_path = self.output_dir / f"{image_name}_gaussian_sigma{sigma}.png"
            save_image(filtered, str(output_path))

            # Store parameters
            self.parameters.append({
                'Image': image_name,
                'Filter_Type': 'Gaussian',
                'Parameter_Name': 'sigma',
                'Parameter_Value': sigma,
                'Kernel_Size': ksize,
                'Output_File': output_path.name
            })

            results.append(filtered)
            print(f"   Gaussian filter (σ={sigma}, kernel={ksize}x{ksize}) applied")

        return results

    def apply_median_filter(self, image, image_name, kernel_sizes=[3, 5, 7]):
        
        print(f"\n Applying Median filter on {image_name}...")
        results = []

        # Ensure image is grayscale
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray_image = image.copy()

        for ksize in kernel_sizes:
            # Apply Median filter
            filtered = cv2.medianBlur(gray_image, ksize)

            # Save output
            output_path = self.output_dir / f"{image_name}_median_k{ksize}.png"
            save_image(filtered, str(output_path))

            # Store parameters
            self.parameters.append({
                'Image': image_name,
                'Filter_Type': 'Median',
                'Parameter_Name': 'kernel_size',
                'Parameter_Value': ksize,
                'Kernel_Size': ksize,
                'Output_File': output_path.name
            })

            results.append(filtered)
            print(f"   Median filter (kernel={ksize}x{ksize}) applied")

        return results

    def create_visualization(self, original, filtered_images, titles, image_name, filter_type):
        
        n_images = len(filtered_images) + 1
        fig, axes = plt.subplots(1, n_images, figsize=(4 * n_images, 4))

        # Ensure image is grayscale for display
        if len(original.shape) == 3:
            display_original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        else:
            display_original = original

        # Display original
        axes[0].imshow(display_original, cmap='gray')
        axes[0].set_title('Original')
        axes[0].axis('off')

        # Display filtered images
        for i, (filtered, title) in enumerate(zip(filtered_images, titles), 1):
            axes[i].imshow(filtered, cmap='gray')
            axes[i].set_title(title)
            axes[i].axis('off')

        plt.suptitle(f'{filter_type} Filter Comparison - {image_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save visualization
        output_path = self.output_dir / f"{image_name}_{filter_type.lower()}_comparison.png"
        plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close()

        print(f"   Visualization saved: {output_path.name}")

    def save_parameters_table(self):
        
        df = pd.DataFrame(self.parameters)
        csv_path = Path(__file__).parent / "parameters.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n Parameters table saved: {csv_path}")
        print(f"\nParameters summary:")
        print(df.to_string(index=False))

def main():
    
    print("=" * 70)
    print("MODULE 1: IMAGE FILTERING")
    print("=" * 70)

    # Initialize filter
    filter_processor = ImageFilter()

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
        output_path = filter_processor.output_dir / f"{name}_original.png"
        save_image(img, str(output_path))

    # Process each image with both filters
    for name, img in test_images.items():
        print(f"\n{'='*70}")
        print(f"Processing: {name.upper()}")
        print(f"{'='*70}")

        # Apply Gaussian filter with different sigma values
        sigma_values = [1, 3, 5]
        gaussian_results = filter_processor.apply_gaussian_filter(img, name, sigma_values)

        # Create Gaussian visualization
        titles = [f'σ={s}' for s in sigma_values]
        filter_processor.create_visualization(
            img, gaussian_results, titles, name, 'Gaussian'
        )

        # Apply Median filter with different kernel sizes
        kernel_sizes = [3, 5, 7]
        median_results = filter_processor.apply_median_filter(img, name, kernel_sizes)

        # Create Median visualization
        titles = [f'k={k}' for k in kernel_sizes]
        filter_processor.create_visualization(
            img, median_results, titles, name, 'Median'
        )

    # Save parameters table
    filter_processor.save_parameters_table()

    print("\n" + "=" * 70)
    print(" MODULE 1 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n📁 All outputs saved in: {filter_processor.output_dir}")
    print("\nGenerated files:")
    print("  - Original images (cameraman, coins, checkerboard)")
    print("  - Gaussian filtered images (σ=1, 3, 5)")
    print("  - Median filtered images (kernel=3, 5, 7)")
    print("  - Comparison visualizations")
    print("  - parameters.csv")

if __name__ == "__main__":
    main()
