import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# --- Step 1: Data Generation (Learnable Binary Target) ---
print("\n--- 任务 2: PyTorch 分类 (BCELoss + SGD) ---")
print("--- Step 1: 数据生成 ---")

# 1. 生成输入特征 X (200 样本, 4 特征)
X = torch.randn(200, 4)

# 2. 创建 learnable binary target y
w = torch.tensor([[0.8],[0.6],[0.7],[0.5]])
b = torch.tensor([-1.0])
noise = 0.3 * torch.randn(200, 1)

# 计算概率 (0, 1)
proba = torch.sigmoid(X @ w + b + noise)
# 转换为二元标签 (0/1)
y = (proba > 0.5).float()

print(f"X.shape: {X.shape}")
print(f"y.shape: {y.shape}")

# --- Step 2: Model Definition (RiskNN) ---
class RiskNN(nn.Module):
    def __init__(self):
        super(RiskNN, self).__init__()
        # Input: 4 -> Hidden: 8
        self.fc1 = nn.Linear(4, 8)
        # Hidden: 8 -> Output: 1
        self.fc2 = nn.Linear(8, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        # 输出层使用 Sigmoid 激活函数，将输出压缩到 [0, 1] 范围作为概率
        return torch.sigmoid(self.fc2(x))

# --- Step 3: Model Setup (BCELoss + SGD) ---
print("\n--- Step 3: 模型设置 (BCELoss + SGD) ---")
model = RiskNN()
criterion = nn.BCELoss() # Binary Cross Entropy Loss
optimizer = optim.SGD(model.parameters(), lr=0.05) # Stochastic Gradient Descent

print("模型架构:")
print(model)

# --- Step 4: Training Loop ---
epochs = 15
loss_history = []

print("\n--- Step 4: 训练循环 ---")
for epoch in range(epochs):
    # 1. 计算预测
    preds = model(X)

    # 2. 计算损失
    loss = criterion(preds, y)

    # 3. 优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 记录并打印损失
    loss_history.append(loss.item())
    print(f"Epoch {epoch + 1:02d}: loss={loss.item():.4f}")

# --- Step 5: Loss Visualisation ---
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs + 1), loss_history, marker='s', linestyle='--', color='red')
plt.title('Training Loss Over Epochs (BCELoss + SGD)')
plt.xlabel('Epoch')
plt.ylabel('Loss (BCE)')
plt.grid(True)
plt.show()

# --- 打印最终性能 ---
final_preds = (model(X) > 0.5).float()
accuracy = (final_preds == y).float().mean().item()
print(f"\n最终分类准确率: {accuracy:.4f}")