import numpy as np
import json
import math
import os

def load_cameras(file_path):
    cameras = {}
    with open(file_path, 'r') as f:
        for line in f:
            if not line.startswith('#') and len(line.strip()) > 0:
                parts = line.split()
                try:
                    camera_id = int(parts[0])
                    model = parts[1]
                    width = int(parts[2])
                    height = int(parts[3])
                    fx = float(parts[4])
                    fy = fx  # Assuming fx == fy for pinhole cameras
                    cx = float(parts[5])
                    cy = float(parts[6])
                    cameras[camera_id] = {
                        'model': model,
                        'width': width,
                        'height': height,
                        'focal_length': [fx, fy],
                        'principal_point': [cx, cy]
                    }
                except (ValueError, IndexError) as e:
                    print(f"Error parsing cameras.txt line: {line.strip()} - {e}")
    return cameras

def load_images(file_path):
    images = []
    with open(file_path, 'r') as f:
        for line in f:
            if not line.startswith('#') and len(line.strip()) > 0:
                parts = line.split()
                try:
                    image_id = int(parts[0])
                    qw, qx, qy, qz = map(float, parts[1:5])  # Quaternions
                    tx, ty, tz = map(float, parts[5:8])  # Translation vector
                    file_name = parts[9]  # Image file name
                    images.append({
                        'image_id': file_name,
                        'rotation_quaternion': [qw, qx, qy, qz],
                        'translation_vector': [tx, ty, tz]
                    })
                except (ValueError, IndexError) as e:
                    print(f"Error parsing images.txt line: {line.strip()} - {e}")
    return images

def calculate_camera_angle_x(fx, width):
    return 2 * math.atan(width / (2 * fx))

def quaternion_to_rotation_matrix(qw, qx, qy, qz):
    R = np.array([
        [1 - 2 * (qy ** 2 + qz ** 2), 2 * (qx * qy - qw * qz), 2 * (qx * qz + qw * qy)],
        [2 * (qx * qy + qw * qz), 1 - 2 * (qx ** 2 + qz ** 2), 2 * (qy * qz - qw * qx)],
        [2 * (qx * qz - qw * qy), 2 * (qy * qz + qw * qx), 1 - 2 * (qx ** 2 + qy ** 2)]
    ])
    return R

def create_transforms_json(cameras, images, output_path, image_folder_path):
    if len(cameras) == 1:
        camera = list(cameras.values())[0]
    else:
        camera = cameras[1]  # Default to camera ID 1; modify as needed.

    fx = camera['focal_length'][0]
    width = camera['width']

    camera_angle_x = calculate_camera_angle_x(fx, width)

    frames = []
    for img in images:
        qw, qx, qy, qz = img['rotation_quaternion']
        tx, ty, tz = img['translation_vector']

        R = quaternion_to_rotation_matrix(qw, qx, qy, qz)

        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = R
        transform_matrix[:3, 3] = [tx, ty, tz]

        image_path = os.path.join(image_folder_path, img['image_id'])

        frames.append({
            "file_path": image_path.replace("\\", "/"),
            "rotation": 0.0,
            "transform_matrix": transform_matrix.tolist()
        })

    transforms_data = {
        "camera_angle_x": camera_angle_x,
        "frames": frames
    }

    with open(output_path, 'w') as json_file:
        json.dump(transforms_data, json_file, indent=4)

# Define paths
cameras_file = "D://Model_Project//predata//cameras.txt"
images_file = "D://Model_Project//predata//images.txt"
image_folder_path = "/Dape/data//images"
output_json_path = "transforms.json"

# Load COLMAP data
cameras = load_cameras(cameras_file)
images = load_images(images_file)

# Create and save transforms_trains.json
create_transforms_json(cameras, images, output_json_path, image_folder_path)
