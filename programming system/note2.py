import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# --- Step 1: Data Generation ---
print("--- Step 1: 数据生成 ---")
# 1. 生成特征数据 X (120 样本, 8 特征)
X = torch.randn(120, 8)

# 2. 创建 learnable target y
torch.manual_seed(42) # 设置随机种子以保证结果可复现

# 定义常数 w (8x1) 和 b
w = torch.randn(8, 1)
b = torch.randn(1)
# 噪声项 ~ N(0, 0.5)
noise = 0.5 * torch.randn(120, 1)

# 创建目标 y = X @ w + b + noise
y = X @ w + b + noise

print(f"X.shape: {X.shape}")
print(f"y.shape: {y.shape}")

# --- Step 2: Model Definition ---
class RevenueNet(nn.Module):
    def __init__(self):
        super(RevenueNet, self).__init__()
        # Input: 8 -> Hidden: 16
        self.fc1 = nn.Linear(8, 16)
        # Hidden: 16 -> Hidden: 8
        self.fc2 = nn.Linear(16, 8)
        # Hidden: 8 -> Output: 1
        self.fc3 = nn.Linear(8, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x) # 回归任务，输出层无激活函数

# --- Step 3: Model Setup ---
print("\n--- Step 3: 模型设置 ---")
model = RevenueNet()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.010)

print("模型架构:")
print(model)

# --- Step 4: Training Loop ---
epochs = 30
loss_history = []

print("\n--- Step 4: 训练循环 ---")
for epoch in range(epochs):
    # 1. 计算预测
    predictions = model(X)

    # 2. 计算损失
    loss = criterion(predictions, y)

    # 3. 反向传播和优化
    optimizer.zero_grad() # 梯度归零
    loss.backward()       # 反向传播
    optimizer.step()      # 更新权重

    # 记录损失
    loss_history.append(loss.item())

    # 打印损失
    print(f"Epoch {epoch + 1:02d} | Loss: {loss.item():.6f}")

# --- Step 5: Loss Visualisation ---
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs + 1), loss_history, marker='o', linestyle='-', color='blue')
plt.title('Training Loss Over Epochs (MSELoss + Adam)')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.grid(True)
plt.show()

# --- 打印最终性能 ---
final_pred = model(X)
final_loss = criterion(final_pred, y).item()
print(f"\n最终 MSE Loss: {final_loss:.6f}")