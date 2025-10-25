# Nama: Alessandro Jusack Hasian
# NIM: 18222025
# Fitur unik: Generate proper calibration checkerboard pattern

import cv2
import numpy as np
from pathlib import Path

def create_checkerboard(pattern_size=(9, 6), square_size=50, output_path="calibration_checkerboard.png"):
    
    # Calculate image size (add 2 for border squares)
    width = (pattern_size[0] + 1) * square_size
    height = (pattern_size[1] + 1) * square_size

    # Create checkerboard
    checkerboard = np.zeros((height, width), dtype=np.uint8)

    for i in range(pattern_size[1] + 1):
        for j in range(pattern_size[0] + 1):
            if (i + j) % 2 == 0:
                y1 = i * square_size
                y2 = (i + 1) * square_size
                x1 = j * square_size
                x2 = (j + 1) * square_size
                checkerboard[y1:y2, x1:x2] = 255

    # Save checkerboard
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    full_path = output_dir / output_path

    cv2.imwrite(str(full_path), checkerboard)
    print(f" Checkerboard created: {full_path}")
    print(f"  - Pattern size: {pattern_size}")
    print(f"  - Square size: {square_size}px")
    print(f"  - Image size: {width}x{height}")

    return checkerboard

if __name__ == "__main__":
    print("Creating calibration checkerboard...")
    checkerboard = create_checkerboard(pattern_size=(9, 6), square_size=50)
    print("\n Done!")
