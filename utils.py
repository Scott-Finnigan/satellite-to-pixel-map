import math
import cv2
import numpy as np

def calculate_rotation_angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def rotate_image(image, angle_deg):
    (h, w) = image.shape[:2]
    centre = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(centre, angle_deg, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotated_image

def crop_image(image, x1, y1, x2, y2):
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    return image[y_min:y_max, x_min:x_max]

def scale_image_to_metres(image, real_width_m, real_height_m, pixels_per_m=16):
    target_width_px = int(real_width_m * pixels_per_m)
    target_height_px = int(real_height_m * pixels_per_m)
    resized = cv2.resize(image, (target_width_px, target_height_px), interpolation=cv2.INTER_LANCZOS4)
    return resized

def draw_grid(image, tile_size_px=16, major_line_every=10, colour=(0, 0, 255), major_colour=(0, 255, 255)):
    h, w = image.shape[:2]
    grid_img = image.copy()
    for x in range(0, w, tile_size_px):
        is_major = (x // tile_size_px) % major_line_every == 0
        line_color = major_colour if is_major else colour
        cv2.line(grid_img, (x, 0), (x, h), line_color, 1)
    for y in range(0, h, tile_size_px):
        is_major = (y // tile_size_px) % major_line_every == 0
        line_color = major_colour if is_major else colour
        cv2.line(grid_img, (0, y), (w, y), line_color, 1)
    return grid_img

def interactive_point_selection(image, prompt_text="Click two points", show_box=False):
    temp = image.copy()
    points = []
    selected_img = temp.copy()
    
    def draw_crosshair_and_points(event, x, y, flags, param):
        nonlocal selected_img
        selected_img = temp.copy()
        for pt in points:
            cv2.circle(selected_img, pt, 4, (0, 255, 0), -1)
        if len(points) == 1 and show_box:
            cv2.rectangle(selected_img, points[0], (x, y), (255, 255, 0), 1)
        cv2.line(selected_img, (x, 0), (x, selected_img.shape[0]), (200, 200, 200), 1)
        cv2.line(selected_img, (0, y), (selected_img.shape[1], y), (200, 200, 200), 1)
        cv2.imshow(prompt_text, selected_img)
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            points.append((x, y))
            print(f"Selected point {len(points)}: ({x}, {y})")
    
    cv2.namedWindow(prompt_text)
    cv2.setMouseCallback(prompt_text, draw_crosshair_and_points)
    while len(points) < 2:
        cv2.imshow(prompt_text, selected_img)
        cv2.waitKey(1)
    cv2.destroyWindow(prompt_text)
    return points