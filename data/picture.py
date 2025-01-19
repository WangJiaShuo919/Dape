import os
import cv2

# 原始图片文件夹路径
input_dir = "/images"
# 处理后图片的保存路径
output_dir = "/Dape/data/my_dataset/images_resized"
# 设置目标分辨率（宽 x 高）
target_width = 512
target_height = 512

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

# 批量处理图片
for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # 读取图片
        img = cv2.imread(input_path)
        if img is None:
            print(f"Failed to load {input_path}")
            continue

        # 调整分辨率
        resized_img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)

        # 保存图片
        cv2.imwrite(output_path, resized_img)
        print(f"Resized {filename} and saved to {output_path}")
