import cv2
import argparse
import os
from utils import (
    calculate_rotation_angle,
    rotate_image,
    scale_image_to_metres,
    draw_grid,
    crop_image,
    interactive_point_selection
)
# read input image file path from args
parser = argparse.ArgumentParser(description="Convert a satellite image to a grid-aligned pixel map.")
parser.add_argument("image_path", type=str, help="Path to the satellite input image relative to main.py (eg. ./images/test_image.png)")
args = parser.parse_args()
# read in image
img = cv2.imread(args.image_path)
if img is None:
    raise FileNotFoundError(f"Could not load image: {args.image_path}")
# rotate image
points = interactive_point_selection(img, "Select alignment points")
angle = calculate_rotation_angle(points[0], points[1])
rotated = rotate_image(img, angle)
# crop image
(x1, y1), (x2, y2) = interactive_point_selection(rotated, "Select crop points", show_box=True)
cropped = crop_image(rotated, x1, y1, x2, y2)
# resize image
real_width_m = float(input("Enter the real-world width (m): "))
real_height_m = float(input("Enter the real-world height (m): "))
resized = scale_image_to_metres(cropped, real_width_m, real_height_m, pixels_per_m=16)
# draw grid
grid_img = draw_grid(resized, tile_size_px=16, colour=(0, 0, 255), major_colour=(0, 255, 255))
# display final image
cv2.imshow("Final Image with Grid", grid_img)
# build output file name and path
input_dir = os.path.dirname(args.image_path)
input_base, input_ext = os.path.splitext(os.path.basename(args.image_path))
output_filename = f"{input_base}_grid{input_ext}"
output_path = os.path.join(input_dir, output_filename)
# save the new image
cv2.imwrite(output_path, grid_img)
cv2.waitKey(0)
cv2.destroyAllWindows()