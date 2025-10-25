# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Centralized utility functions for image loading and saving

# Utility functions for the CV assignment
# Common functions for loading images and saving outputs

import cv2
import numpy as np
from skimage import data
import matplotlib.pyplot as plt
import os

def load_test_images():
    # Load test images from scikit-image
    images = {
        'cameraman': data.camera(),
        'coins': data.coins(),
        'checkerboard': data.checkerboard(),
        'astronaut': data.astronaut(),
        'chelsea': data.chelsea()
    }

    print("Test images loaded:")
    for name, img in images.items():
        print(f"  - {name}: {img.shape}, dtype: {img.dtype}")

    return images

def save_image(image, filepath, as_grayscale=False):
    # Save image to file
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if as_grayscale and len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # OpenCV uses BGR so convert if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(filepath, image)
    print(f"Saved: {filepath}")

def create_comparison_plot(original, processed, title_original="Original",
                           title_processed="Processed", output_path=None):
    # Create side-by-side comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Show original
    if len(original.shape) == 2:
        axes[0].imshow(original, cmap='gray')
    else:
        axes[0].imshow(original)
    axes[0].set_title(title_original)
    axes[0].axis('off')

    # Show processed
    if len(processed.shape) == 2:
        axes[1].imshow(processed, cmap='gray')
    else:
        axes[1].imshow(processed)
    axes[1].set_title(title_processed)
    axes[1].axis('off')

    plt.tight_layout()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved comparison: {output_path}")

    plt.close()

def ensure_grayscale(image):
    # Convert to grayscale if color
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image

def normalize_image(image):
    # Normalize to 0-255 range
    if image.dtype == np.float64 or image.dtype == np.float32:
        image = (image * 255).astype(np.uint8)
    return image

if __name__ == "__main__":
    print("Testing utility functions...")
    images = load_test_images()
    print("\nAll utility functions ready!")
