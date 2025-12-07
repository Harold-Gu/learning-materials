import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

file_name = 'heights.csv'

# ==========================================
# Task 1: Create/Check CSV (严格遵守：存在即追加，不存在则创建)
# ==========================================
print("\n=== Task 1: Initialization ===")

# 检查文件是否存在
if os.path.isfile(file_name):
    # 场景 A: 文件存在 -> 不覆盖，准备追加
    # 题目要求：Print a message confirming the .csv is open for appending
    print(f"File '{file_name}' is open for appending.")
else:
    # 场景 B: 文件不存在 -> 创建并写入表头
    # 题目要求：Print a message confirming whether the .csv file was created
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Height'])  # 只在第一次创建时写表头
    print(f"File '{file_name}' was created successfully.")

# ==========================================
# Task 2: Data Entry (直接追加数据)
# ==========================================
print("\n=== Task 2: Data Entry ===")

# 使用 'a' (append) 模式，确保不覆盖旧数据
with open(file_name, mode='a', newline='') as file:
    writer = csv.writer(file)

    while True:
        name = input("Enter name (or 'q' to quit): ").strip()
        if name.lower() == 'q':
            break

        # 获取身高 (简单验证是否为数字)
        while True:
            height_str = input("Enter height (cm): ").strip()
            if height_str.isdigit():
                writer.writerow([name, height_str])
                break
            else:
                print("Invalid input. Please enter a whole number.")

print(f"Data saved to {file_name}")

# ==========================================
# Task 3: Summary Statistics (智能读取，兼容旧文件)
# ==========================================
print("\n=== Task 3: Summary Statistics ===")

try:
    # 读取数据
    df = pd.read_csv(file_name)

    # --- 兼容性处理 (防止因为旧文件表头格式不同而报错) ---
    # 1. 去除列名空格 (例如 " Height" -> "Height")
    df.columns = df.columns.str.strip()

    # 2. 统一列名大小写 (例如 "height" -> "Height")
    # 这样即使你之前的 csv 写的是小写 height，这里也能识别
    df.rename(columns=lambda x: x.capitalize(), inplace=True)

    # 3. 检查是否有 'Height' 列
    if 'Height' in df.columns:
        # 强制转换为数字，无法转换的变为 NaN (处理脏数据)
        df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
        # 删除身高为空的行
        df = df.dropna(subset=['Height'])

        if not df.empty:
            total_records = len(df)
            avg_height = df['Height'].mean()
            min_height = df['Height'].min()
            max_height = df['Height'].max()

            print(f"Total number of records: {total_records}")
            print(f"Average height: {avg_height:.2f} cm")
            print(f"Minimum height: {min_height} cm")
            print(f"Maximum height: {max_height} cm")

            # 保存结果
            with open('height_summary.txt', 'w') as f:
                f.write(f"Total: {total_records}\nAverage: {avg_height:.2f}\nMin: {min_height}\nMax: {max_height}")
            print("Summary saved to 'height_summary.txt'.")

            # ==========================================
            # Task 4: Visualisation
            # ==========================================
            print("\n=== Task 4: Visualisation ===")
            plt.figure(figsize=(8, 5))
            plt.hist(df['Height'], bins=5, color='skyblue', edgecolor='black')
            plt.title('Height Distribution')
            plt.xlabel('Height (cm)')
            plt.ylabel('Frequency')
            plt.grid(axis='y', alpha=0.5)
            print("Displaying plot...")
            plt.show()
        else:
            print("File exists but contains no valid height data.")
    else:
        # 如果真的找不到 Height 列 (说明文件格式完全不对)
        print("Error: Could not find 'Height' column in the file. Please check the CSV format.")

except Exception as e:
    print(f"An error occurred: {e}")