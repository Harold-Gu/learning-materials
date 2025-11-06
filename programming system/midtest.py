import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

# ==============================================================================
# 0. 配置/初始化部分
# ==============================================================================

# 配置 Matplotlib 样式（可选）
plt.style.use('seaborn-v0_8-whitegrid')
pd.set_option('display.max_columns', 10)  # 设置最大显示列数
pd.set_option('display.width', 1000)  # 设置控制台显示宽度

FILE_NAME = 'your_data.csv'  # 待加载的数据文件名
DB_NAME = 'your_database.db'  # 数据库文件名
TABLE_NAME = 'your_table'  # 数据库表名

print("--- 模板初始化完成 ---")


# ==============================================================================
# 1. Pandas 数据加载与基础操作
# ==============================================================================

def load_and_inspect_data(file_path):
    """加载数据，进行初步检查，并返回 DataFrame"""
    print("\n" + "=" * 10 + " 1. Pandas 数据加载与基础操作 " + "=" * 10)
    try:
        # 常见加载函数
        df = pd.read_csv(file_path)
        # df = pd.read_excel(file_path, sheet_name='Sheet1')

        print(f"数据加载成功。文件: {file_path}")
        print("-" * 50)

        # 基础检查
        print("1.1. DataFrame 形状 (行, 列):", df.shape)
        print("1.2. 前 5 行数据:\n", df.head())
        print("1.3. 列信息 (数据类型/非空值计数):\n", df.info(verbose=False))
        print("1.4. 数值列描述性统计:\n", df.describe())

        return df
    except FileNotFoundError:
        print(f"错误：未找到文件 '{file_path}'。")
        return pd.DataFrame()  # 返回空 DataFrame
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        return pd.DataFrame()


# ==============================================================================
# 2. Pandas 数据清洗与转换 (结合 NumPy)
# ==============================================================================

def clean_and_transform(df):
    """数据清洗、类型转换和特征工程"""
    if df.empty:
        return df

    print("\n" + "=" * 10 + " 2. Pandas 数据清洗与转换 " + "=" * 10)

    # 2.1. 类型转换与日期处理
    # 示例：将列转换为日期类型
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # 尝试转换，错误值转为 NaT

    # 示例：将列转换为数值类型
    # df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # 2.2. 缺失值处理
    missing_initial = df.isnull().sum()
    print("2.2. 初始缺失值统计:\n", missing_initial[missing_initial > 0])

    # 示例：删除包含 NaN 的行
    df.dropna(subset=['Date'], inplace=True)

    # 示例：用平均值/中位数填充缺失值
    # df['Some_Column'].fillna(df['Some_Column'].mean(), inplace=True)

    # 2.3. 字符串处理 (常用于分类列)
    # 示例：去除首尾空格，转换为大写
    if 'Category' in df.columns:
        df['Category'] = df['Category'].str.strip().str.upper()

    # 2.4. NumPy 数组操作 / 条件计算
    # 示例：使用 np.where 创建新特征 (二值化)
    # df['Is_High_Value'] = np.where(df['Value'] > 1000, 1, 0)

    # 示例：计算对数
    # df['Log_Value'] = np.log(df['Value'])

    # 2.5. 数据聚合
    # 示例：按组计算总和
    # summary = df.groupby('Category')['Count'].sum().reset_index()
    # print("2.5. 聚合结果示例:\n", summary)

    print("数据清洗和转换完成。")
    return df


# ==============================================================================
# 3. Matplotlib 数据可视化
# ==============================================================================

def visualize_data(df):
    """使用 Matplotlib 绘制常用图表"""
    if df.empty:
        return

    print("\n" + "=" * 10 + " 3. Matplotlib 数据可视化 " + "=" * 10)

    # 3.1. 柱状图 (Bar Chart) 示例
    # 假设有一个 Series 记录了不同类别的计数
    if 'Incident_Type' in df.columns and 'Count' in df.columns:
        counts = df.groupby('Incident_Type')['Count'].sum().sort_values(ascending=False).head(5)

        plt.figure(figsize=(8, 5))
        counts.plot(kind='bar', color='skyblue')
        plt.title('Top 5 Incident Types')
        plt.ylabel('Total Count')
        plt.xlabel('Incident Type')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    # 3.2. 折线图 (Line Plot) 示例
    # 假设按月聚合后的数据
    if 'Date' in df.columns and 'Count' in df.columns:
        # 筛选 2025 年数据并按月聚合
        df_2025 = df[df['Date'].dt.year == 2025].copy()
        if not df_2025.empty:
            monthly_totals = df_2025.groupby(df_2025['Date'].dt.to_period('M'))['Count'].sum()

            plt.figure(figsize=(10, 6))
            monthly_totals.to_timestamp().plot(kind='line', marker='o', color='green')
            plt.title('Monthly Trend (2025)')
            plt.xlabel('Month')
            plt.ylabel('Total Count')
            plt.grid(True)
            plt.show()

    # 3.3. 散点图 (Scatter Plot) 示例 (用于关系分析)
    # if 'X_Feature' in df.columns and 'Y_Feature' in df.columns:
    #     plt.figure(figsize=(6, 6))
    #     plt.scatter(df['X_Feature'], df['Y_Feature'], alpha=0.6)
    #     plt.title('Scatter Plot of X vs Y')
    #     plt.xlabel('X_Feature')
    #     plt.ylabel('Y_Feature')
    #     plt.show()

    print("可视化完成。")


# ==============================================================================
# 4. Pandas/SQLite3 数据库集成应用
# ==============================================================================

def database_integration(df, db_name, table_name):
    """使用 Pandas 和 SQLite3 进行数据存取和查询"""
    if df.empty:
        print("\n跳过数据库操作：DataFrame 为空。")
        return

    print("\n" + "=" * 10 + " 4. Pandas/SQLite3 数据库集成应用 " + "=" * 10)

    # 4.1. 建立连接
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print(f"4.1. 成功连接到数据库: {db_name}")

    # 4.2. Pandas to SQLite (快速写入)
    try:
        # 将 DataFrame 写入 SQLite 数据库中的一个表
        # if_exists='replace': 每次运行都替换整个表
        # if_exists='append': 追加数据
        # if_exists='fail': 如果表已存在则抛出错误
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"4.2. 成功将 {len(df)} 条数据写入表 '{table_name}'。")
    except Exception as e:
        print(f"Pandas 写入 SQLite 失败: {e}")

    # 4.3. SQLite 查询 (Query)
    # 示例：查询总数最高的 Top 5
    sql_query = f"""
    SELECT System, SUM(Count) AS Total_Count
    FROM {table_name}
    GROUP BY System
    ORDER BY Total_Count DESC
    LIMIT 5;
    """

    print("\n4.3. 执行 SQL 查询 (Top 5 Systems):")

    # 使用 pd.read_sql_query 直接将查询结果读取到新的 DataFrame
    try:
        query_df = pd.read_sql_query(sql_query, conn)
        print(query_df)
    except pd.io.sql.DatabaseError as e:
        print(f"执行 SQL 查询失败: 请确保表中存在 'System' 和 'Count' 列. 错误: {e}")
        conn.close()
        return

    # 4.4. 结果导出 (从数据库结果到 CSV)
    output_file = 'query_results.csv'
    query_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n4.4. 查询结果已导出到文件: {output_file}")

    # 4.5. 关闭连接
    conn.close()
    print("数据库连接已关闭。")


# ==============================================================================
# 5. 主执行逻辑 (Main)
# ==============================================================================

if __name__ == "__main__":

    # 创建一个模拟数据文件，便于模板运行和测试
    if not os.path.exists(FILE_NAME):
        data = {
            'Date': pd.to_datetime(
                ['2024-01-01', '2025-02-05', '2025-02-15', '2025-03-01', '2025-03-10', '2025-04-01', 'Invalid Date']),
            'System': ['AuthServer', 'FinanceDB', 'AuthServer', 'WebCore', 'FinanceDB', 'AuthServer', 'AuthServer'],
            'Incident_Type': ['error', 'warning ', ' ERROR', 'critical', 'error', 'error', 'error'],
            'Count': [10, 5, 20, 15, 30, 25, 5],
            'Value': [100.5, 50.2, 200.1, 150.0, 300.0, 250.0, 50.0],
            'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'A']
        }
        mock_df = pd.DataFrame(data)
        mock_df['Date'] = mock_df['Date'].dt.strftime('%Y-%m-%d')  # 为了能写入 CSV
        mock_df.to_csv(FILE_NAME, index=False)
        print(f"已创建模拟数据文件: {FILE_NAME}")

    # --- 运行流程 ---

    # 1. 加载数据
    data_df = load_and_inspect_data(FILE_NAME)

    # 2. 清洗与转换
    cleaned_df = clean_and_transform(data_df)

    # 3. 可视化
    visualize_data(cleaned_df)

    # 4. 数据库集成
    database_integration(cleaned_df, DB_NAME, TABLE_NAME)