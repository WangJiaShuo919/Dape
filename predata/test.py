def parse_camera_file(file_path):
    cameras = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 5:  # 确保至少有5列数据
                raise ValueError(f"Line format incorrect: {line}")
            camera_id = int(parts[0])
            model = parts[1]
            width = int(parts[2])
            height = int(parts[3])
            params = list(map(float, parts[4:]))
            cameras.append((camera_id, model, width, height, params))
    return cameras

# 调用解析函数
cameras = parse_camera_file("cameras.txt")
print(f"Parsed {len(cameras)} cameras successfully.")
for cam in cameras[:5]:  # 打印前5个相机
    print(cam)
