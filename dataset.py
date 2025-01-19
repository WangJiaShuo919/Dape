import torch
from torch.utils.data import Dataset
from PIL import Image
import os
import json
import numpy as np


class NeRFDataset(Dataset):
    def __init__(self, data_dir):
        # 加载 transforms_trains.json
        with open(os.path.join(data_dir, 'transforms_trains.json'), 'r') as f:
            self.data = json.load(f)

        # 加载所有图像路径和相机姿势
        self.image_paths = []
        self.poses = []
        for frame in self.data['frames']:
            self.image_paths.append(frame['file_path'])
            self.poses.append(frame['transform_matrix'])

        # 设置相机水平视角
        self.camera_angle_x = self.data['camera_angle_x']

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # 获取图像和位姿矩阵
        img_path = self.image_paths[idx]
        pose = np.array(self.poses[idx])

        # 加载图像
        img = Image.open(img_path).convert('RGB')
        img = np.array(img)  # 转换为 numpy 数组

        # 转换图像为 float32 类型，归一化到 [0, 1]
        img = img.astype(np.float32) / 255.0

        # 转换为 PyTorch 张量
        img = torch.from_numpy(img).permute(2, 0, 1)  # 变为 (C, H, W)

        # 转换相机位姿矩阵为 PyTorch 张量
        pose = torch.from_numpy(pose).float()

        return img, pose, img_path
