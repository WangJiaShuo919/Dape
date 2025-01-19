import torch

# 路径到你的 .pth 文件
model_checkpoint = "D:/Model_Project/predata/nerf_model_step_10000.pth"

# 加载检查内容
saved_data = torch.load(model_checkpoint, map_location='cpu')

# 打印文件内容的键
print("Keys in .pth file:", saved_data.keys())
