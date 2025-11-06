import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3


# ==============================================================================
# Task 3a: 模型设置 (Model Setup)
# ==============================================================================

print("=" * 15 + " Task 3a: Data Setup " + "=" * 15)

# 1. 设置随机种子以确保每次运行结果一致 (0.5 mark)
torch.manual_seed(42)  # 使用一个固定值（如 42）

# 2. 生成合成特征 X (200个样本, 4个特征) (1 mark)
X = torch.randn(200, 4)

# 3. 生成二元目标标签 y (包含 0 或 1) (1 mark)
y = torch.randint(low=0, high=2, size=(200, 1)).float()

# 4. 打印 X 和 y 的形状 (0.5 mark)
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
print("-" * 50)


# ==============================================================================
# Task 3b: 模型定义和初始化 (Model Definition and Initialization)
# ==============================================================================

# 1. 定义一个继承自 torch.nn.Module 的神经网络类 (1.5 marks)
class RiskNN(nn.Module):
    def __init__(self, in_features=4, hidden_features=8, out_features=1):
        super(RiskNN, self).__init__()

        # 使用 nn.Sequential 定义网络结构
        self.net = nn.Sequential(
            # 输入层: 4个输入神经元
            nn.Linear(in_features, hidden_features),
            # 隐藏层: 8个神经元，使用 ReLU 激活
            nn.ReLU(),
            # 输出层: 1个输出神经元
            nn.Linear(hidden_features, out_features),
            # 使用 Sigmoid 激活函数
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


# 2. 实例化模型、损失函数和优化器 (1.5 marks)
model = RiskNN()
criterion = nn.BCELoss()  # 损失函数: 二元交叉熵损失
optimizer = optim.SGD(model.parameters(), lr=0.05)  # 优化器: SGD, 学习率 0.05

# 3. 打印模型架构 (1 mark)
print("=" * 15 + " Task 3b: Model Definition " + "=" * 15)
print(model.net)
print("-" * 50)

# ==============================================================================
# Task 3c: 训练模型 (Training the Model)
# ==============================================================================

num_epochs = 15
training_losses = []

print("=" * 15 + " Task 3c: Training Results " + "=" * 15)

# 1. 训练网络 15 个 Epoch (2 marks)
for epoch in range(1, num_epochs + 1):
    # a. 执行前向传播计算预测
    outputs = model(X)

    # b. 计算损失
    loss = criterion(outputs, y)

    # 记录损失值
    training_losses.append(loss.item())

    # c. 执行反向传播并更新模型权重
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 2. 打印训练损失 (1 mark)
    print(f"Epoch {epoch:02d}: loss={loss.item():.4f}")
print("-" * 50)

# ==============================================================================
# Task 3d: 损失可视化 (Loss Visualisation)
# ==============================================================================

print("=" * 15 + " Task 3d: Plotting Loss " + "=" * 15)

# 1. 准备数据
epochs = range(1, num_epochs + 1)

# 2. 创建图表
plt.figure(figsize=(7, 5))
plt.plot(epochs, training_losses, marker='o', linestyle='-', color='tab:blue', markersize=5)

# 3. 设置标签和标题
plt.title("RiskNN Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Training Loss")

# 4. 设置刻度以匹配示例图的布局
plt.xticks(np.arange(2, num_epochs + 1, 2))
# 根据 Task 3d 示例图 Y轴刻度范围(0.62到0.70)设置
y_min = np.floor(min(training_losses) / 0.02) * 0.02
y_max = np.ceil(max(training_losses) / 0.02) * 0.02
plt.yticks(np.arange(0.62, 0.701, 0.02))

# 5. 显示网格
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
print("训练损失曲线图已显示。")



# 设置 Matplotlib 样式（可选，让图表更清晰）
plt.style.use('ggplot')

# ==============================================================================
# Task 1a: 数据加载和清洗 (Data Loading and Cleaning)
# ==============================================================================

print("=" * 10 + " Task 1a: Data Loading and Cleaning " + "=" * 10)

# 1. Load the file cyber_incidents.csv into a pandas DataFrame (2 marks)
print("1. Load the file cyber_incidents.csv into a pandas DataFrame. Print the first 5 rows and the shape.")
try:
    # 尝试加载文件
    df = pd.read_csv('cyber_incidents.csv')

    # [1a-1] 打印前 5 行和形状
    print("\n[1a-1] First 5 rows:")
    print(df.head())
    print(f"\nDataFrame shape (rows, cols): ({df.shape[0]}, {df.shape[1]})")

except FileNotFoundError:
    print("错误：未找到 cyber_incidents.csv 文件。")
    # 如果文件找不到，退出后续操作
    exit()
print("-" * 50)

# 2. Data Cleaning: Convert the Date column to a datetime object (2 marks)
print("2. Data Cleaning: Convert the Date column to a datetime object and print the column type.")
# 原始数据中日期格式不统一 (MM/DD/YYYY 和 YYYY-MM-DD), errors='coerce' 会将无法解析的日期设为 NaT
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# [1a-2] 打印 Date 列的数据类型
print(f"\n[1a-2] 'Date' dtype after conversion: {df['Date'].dtype}")
print("-" * 50)

# 3. Check for and handle missing values (2 marks)
print("3. Check for and handle missing values. Fill them with appropriate values.")
initial_rows = len(df)
# 统计缺失值 (主要检查 Date 列转换失败的 NaT)
missing_before = df['Date'].isna().sum()

# 处理缺失值/无效值：删除带有 NaT 的行 (模仿 Task 1a-3 中的“Rows dropped”)
df.dropna(subset=['Date'], inplace=True)
final_rows = len(df)
rows_dropped = initial_rows - final_rows

# [1a-3] 打印处理结果
print(f"\n[1a-3] Rows dropped due to invalid/missing Date: {rows_dropped} (from {initial_rows} to {final_rows})")
print(f"[1a-3] Total missing values after handling: {df.isnull().sum().sum()}")  # 总缺失值应为 0
print("-" * 50)

# 4. Ensure Incident_Type is uppercase and stripped of spaces (2 marks)
print("4. Ensure Incident_Type is uppercase and stripped of spaces; print unique Incident_Type types.")
# 转换为大写并去除首尾空格
df['Incident_Type'] = df['Incident_Type'].str.upper().str.strip()

# [1a-4] 打印唯一的 Incident_Type
unique_types = df['Incident_Type'].unique()
print(f"\n[1a-4] Unique Incident_Type values:\n{unique_types.tolist()}")
print("-" * 50)

# ==============================================================================
# Task 1b: 数据可视化 (Data Visualisation)
# ==============================================================================

print("=" * 10 + " Task 1b: Data Visualisation " + "=" * 10)

# 1. Total Incidents per Type: Bar Chart (2 marks)
print("1. Total Incidents per Type: Create a bar chart showing total incidents per Incident_Type.")

# 聚合数据：按事件类型分组并求 Count 的总和
incident_totals = df.groupby('Incident_Type')['Count'].sum().sort_values(ascending=False)

# [1b-1] 打印聚合结果
print("\n[1b-1] Total incidents per Incident_Type:")
print(incident_totals)
print(f"Name: {incident_totals.name}, dtype: {incident_totals.dtype}")

# 绘制柱状图 (匹配示例图的样式)
plt.figure(figsize=(10, 6))
incident_totals.plot(kind='bar', color='#4C72B0')  # 使用 Matplotlib 默认蓝色系
plt.title('Total Incidents by Type')
plt.xlabel('Incident Type')
plt.ylabel('Total Incidents')
plt.xticks(rotation=45, ha='right')  # 旋转X轴标签
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
print("-" * 50)

# 2. Monthly Totals for 2025: Line Chart (3 marks)
print("2. Monthly Totals for 2025: Create a line chart of total incidents per month for 2025.")

# 筛选 2025 年的数据
df_2025 = df[df['Date'].dt.year == 2025].copy()

# 按月聚合
# to_period('M') 将日期转换为月份周期
monthly_totals_2025 = df_2025.groupby(df_2025['Date'].dt.to_period('M'))['Count'].sum()

# [1b-2] 打印聚合结果（匹配输出格式 YYYY-MM -> total）
monthly_totals_print = monthly_totals_2025.rename(index=lambda x: str(x))
print("\n[1b-2] Monthly totals for 2025 (YYYY-MM -> total):")
print(monthly_totals_print)
print(f"Name: {monthly_totals_print.name}, dtype: {monthly_totals_print.dtype}")

# 准备绘图数据：填充缺失月份为 0 (确保折线图是连续的)
# 创建完整的 2025 年 1 月到 10 月的 PeriodIndex
all_months = pd.PeriodIndex(start='2025-01', end='2025-10', freq='M')
monthly_totals_full = monthly_totals_2025.reindex(all_months, fill_value=0)

# 绘制折线图 (匹配示例图的样式)
plt.figure(figsize=(10, 6))
# 使用 to_timestamp() 将 PeriodIndex 转换回 DatetimeIndex 以便 Matplotlib 格式化日期
monthly_totals_full.to_timestamp().plot(kind='line', marker='o', color='green', linewidth=2)

plt.title('Monthly Incident Totals (2025)')
plt.xlabel('Month (2025)')
plt.ylabel('Total Incidents')

# 格式化 X 轴为月份名称 (Jan, Feb...)
import matplotlib.dates as mdates

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.xticks(rotation=0)

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
print("-" * 50)



# 假设 Task 1 的代码已在上方成功运行，且 cleaned DataFrame 名为 df
# df = pd.read_csv('cyber_incidents.csv') ... (Task 1 运行后的 df)

# ==============================================================================
# 任务 2a: 数据库创建和数据插入
# ==============================================================================
print("=" * 10 + " 任务 2a: 数据库创建和数据插入 " + "=" * 10)

# --- 准备插入数据 ---
# 数据库需要：Date (YYYY-MM-DD 字符串), System, Incident_Type, 和 Count。
# 将 'Date' 列转换回简单的字符串格式以便 SQL 插入。
df_insert = df.copy()
# 确保在 Task 1 中 Date 已经被转换为 datetime 对象，这里才能使用 dt.strftime
df_insert['Date'] = df_insert['Date'].dt.strftime('%Y-%m-%d')

# 准备数据为 list of tuples 格式，供 sqlite3.executemany 使用
# 列顺序: ['Date', 'System', 'Incident_Type', 'Count']
# 仅选择所需的列并转换为 Python 的列表 of 列表
incident_data = df_insert[['Date', 'System', 'Incident_Type', 'Count']].values.tolist()

# 转换为 list of tuples
incident_data = [tuple(row) for row in incident_data]

# 1. 创建名为 IncidentsDB 的 SQLite 数据库 (1 分)
# 连接到 SQLite 数据库。如果不存在，它将被创建。
DB_NAME = 'IncidentsDB.db'
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
print(f"1. 数据库 '{DB_NAME}' 连接/创建成功。")
print("-" * 50)

# 2. 创建名为 Incidents 的表 (2 分)
print("2. 创建名为 Incidents 的表，并设置唯一性约束。")
try:
    c.execute('''
    CREATE TABLE IF NOT EXISTS Incidents (
        Date TEXT NOT NULL,
        System TEXT NOT NULL,
        Incident_Type TEXT NOT NULL,
        Count INTEGER NOT NULL,
        PRIMARY KEY (Date, System, Incident_Type) -- 强制执行唯一性约束
    );
    ''')
    print("表 'Incidents' 创建成功。")
except sqlite3.Error as e:
    print(f"SQLite 表创建错误: {e}")
print("-" * 50)

# 3. 插入清理和处理后的数据 (3 分)
# 使用 INSERT OR IGNORE 来确保没有重复条目被添加 (由 PRIMARY KEY 约束处理)
print("3. 插入数据到 Incidents 表中。打印插入的行数。")
sql_insert = "INSERT OR IGNORE INTO Incidents (Date, System, Incident_Type, Count) VALUES (?, ?, ?, ?)"

try:
    # 批量插入数据
    c.executemany(sql_insert, incident_data)

    # 检查最后一次 executemany 操作影响的行数
    rows_inserted = c.rowcount

    # 提交更改
    conn.commit()

    # [2a-3] 打印插入的行数
    print(f"\n[2a-3] 插入的行数: {rows_inserted}")

except sqlite3.Error as e:
    print(f"SQLite 数据插入错误: {e}")
    conn.rollback()  # 出错时回滚更改

print("-" * 50)

# ==============================================================================
# 任务 2b: 查询数据库
# ==============================================================================
print("=" * 10 + " 任务 2b: 查询数据库 " + "=" * 10)

# 1. 查询 2025 年记录的总事件数 (2.5 分)
print("1. 查询 2025 年记录的总事件数。")
c.execute('''
SELECT SUM(Count)
FROM Incidents
WHERE Date LIKE '2025%' -- 匹配所有以 '2025' 开头的日期
''')
# fetchone()[0] 取出单个结果
total_incidents_2025 = c.fetchone()[0]

# [2b-1] 打印结果
print(f"\n[2b-1] 2025 年的总事件数: {total_incidents_2025}")
print("-" * 50)

# 2. 查询 2025 年总事件数最高的三个系统 (2.5 分)
print("2. 查询 2025 年总事件数最高的三个系统。")
c.execute('''
SELECT System, SUM(Count) AS Total
FROM Incidents
WHERE Date LIKE '2025%'
GROUP BY System -- 按系统分组
ORDER BY Total DESC -- 按总数降序排列
LIMIT 3 -- 限制为前 3 个
''')
top_systems = c.fetchall()

# [2b-2] 打印结果
print("\n[2b-2] 2025 年事件数前 3 的系统:")
for system, total in top_systems:
    print(f"- {system}: {total}")
print("-" * 50)

# ==============================================================================
# 任务 2c: 导出结果
# ==============================================================================
print("=" * 10 + " 任务 2c: 导出结果 " + "=" * 10)

# 编写查询以将任务 2b 的前 3 个系统保存到 CSV 文件 (3 分 + 1 分)
print("编写查询以将任务 2b 的前 3 个系统保存到名为 top3_systems.csv 的 CSV 文件。")

# 再次定义 SQL 查询
sql_top3 = '''
SELECT System, SUM(Count) AS Total
FROM Incidents
WHERE Date LIKE '2025%'
GROUP BY System
ORDER BY Total DESC
LIMIT 3
'''

# 直接使用 Pandas 从 SQL 查询结果中读取数据到 DataFrame
top3_df = pd.read_sql_query(sql_top3, conn)

# 打印保存前的 DataFrame (1 分)
print("\n[2c] 前 3 系统 DataFrame (将保存到 top3_systems.csv):")
print(top3_df)

# 将 DataFrame 保存到 CSV 文件 (3 分)
try:
    # index=False 避免将 DataFrame 的索引 (0, 1, 2...) 写入 CSV 文件
    top3_df.to_csv('top3_systems.csv', index=False)
    print("\n数据已成功导出到 'top3_systems.csv'")
except Exception as e:
    print(f"保存 CSV 文件出错: {e}")

# 关闭数据库连接
conn.close()
print(f"数据库连接 '{DB_NAME}' 已关闭。")
print("=" * 60)