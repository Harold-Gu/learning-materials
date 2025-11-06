import sqlite3
import os

# 定义数据库文件名
DB_NAME = 'inventory.db'


def setup_database():
    """连接数据库并创建表"""
    # 检查并删除旧的数据库文件，以便每次运行都是全新的示例
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"已删除旧的数据库文件: {DB_NAME}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 创建表：产品 (id, name, price, quantity)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    print("数据库连接成功并创建了 'products' 表。")
    return conn, cursor


def close_database(conn):
    """关闭数据库连接"""
    if conn:
        conn.close()
        print("\n数据库连接已关闭。")


# --- 1. 增 (Create) ---

def insert_single_product(cursor, name, price, quantity):
    """单个插入操作"""
    sql = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, price, quantity))
    print(f"✅ 单个插入成功：{name}")


def insert_many_products(conn, products_data):
    """批量插入操作 (executemany)"""
    cursor = conn.cursor()
    sql = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"
    cursor.executemany(sql, products_data)
    conn.commit()
    print(f"✅ 批量插入成功，共插入 {len(products_data)} 条记录。")


# --- 2. 查 (Read / Retrieve) ---

def select_all_products(cursor):
    """查询所有记录"""
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print("\n--- 所有产品列表 (SELECT *) ---")
    if not rows:
        print("无记录。")
        return
    for row in rows:
        print(f"ID: {row[0]}, 名称: {row[1]}, 价格: {row[2]}, 数量: {row[3]}")
    return rows


def select_by_keyword(cursor, keyword):
    """关键字查询 (模糊查询)"""
    search_term = f'%{keyword}%'
    sql = "SELECT * FROM products WHERE name LIKE ?"
    cursor.execute(sql, (search_term,))
    rows = cursor.fetchall()
    print(f"\n--- 关键字查询结果 (关键字: '{keyword}', 模糊匹配名称) ---")
    if not rows:
        print("未找到匹配记录。")
        return
    for row in rows:
        print(f"ID: {row[0]}, 名称: {row[1]}, 价格: {row[2]}, 数量: {row[3]}")
    return rows


def select_by_id_list(cursor, id_list):
    """
    ⭐ 批量查询：根据 ID 列表查询多条记录 (使用 WHERE IN)
    id_list 必须是元组或列表，如 (1, 3, 5)
    """
    if not id_list:
        print("\n--- 批量查询失败：ID 列表为空。---")
        return []

    # 构造 SQL 语句： (?, ?, ?...) 的部分
    # len(id_list) 个 '?'，用逗号连接起来
    placeholders = ', '.join('?' for _ in id_list)

    # 完整的 SQL：SELECT * FROM products WHERE id IN (?, ?, ...)
    sql = f"SELECT * FROM products WHERE id IN ({placeholders})"

    # 注意：这里 id_list 必须作为元组或列表传递给 execute
    cursor.execute(sql, tuple(id_list))
    rows = cursor.fetchall()

    print(f"\n--- 批量查询结果 (查询 ID 列表: {id_list}) ---")
    if not rows:
        print("未找到匹配记录。")
        return
    for row in rows:
        print(f"ID: {row[0]}, 名称: {row[1]}, 价格: {row[2]}, 数量: {row[3]}")
    return rows


# --- 3. 改 (Update) ---

def update_product_price(conn, product_id, new_price):
    """单个更新操作"""
    cursor = conn.cursor()
    sql = "UPDATE products SET price = ? WHERE id = ?"
    cursor.execute(sql, (new_price, product_id))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✅ 更新成功：产品ID {product_id} 的价格已更新为 {new_price}")
    else:
        print(f"❌ 更新失败：未找到产品ID {product_id}")


def update_many_quantities(conn, updates_data):
    """批量更新操作 (executemany)"""
    cursor = conn.cursor()
    sql = "UPDATE products SET quantity = ? WHERE id = ?"
    cursor.executemany(sql, updates_data)
    conn.commit()
    print(f"✅ 批量更新成功，共更新 {len(updates_data)} 条记录的数量。")


# --- 4. 删 (Delete) ---

def delete_by_id(conn, product_id):
    """单个删除操作"""
    cursor = conn.cursor()
    sql = "DELETE FROM products WHERE id = ?"
    cursor.execute(sql, (product_id,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✅ 删除成功：已删除产品ID {product_id}")
    else:
        print(f"❌ 删除失败：未找到产品ID {product_id}")


def delete_by_keyword(conn, keyword):
    """关键字删除操作"""
    cursor = conn.cursor()
    search_term = f'%{keyword}%'
    sql = "DELETE FROM products WHERE name LIKE ?"
    cursor.execute(sql, (search_term,))
    rows_deleted = cursor.rowcount
    if rows_deleted > 0:
        conn.commit()
        print(f"✅ 关键字删除成功：共删除 {rows_deleted} 条包含关键字 '{keyword}' 的记录。")
    else:
        print(f"❌ 关键字删除失败：未找到包含关键字 '{keyword}' 的记录。")


# ==================== 主程序执行 ====================
if __name__ == '__main__':
    conn, cursor = setup_database()

    # 1. 插入一些初始数据
    insert_single_product(cursor, 'Smart TV', 899.99, 50)  # ID 1
    conn.commit()
    products_to_insert = [
        ('Smartphone', 650.00, 100),  # ID 2
        ('Wireless Earbuds', 79.99, 300),  # ID 3
        ('Gaming Console', 499.50, 40),  # ID 4
        ('USB Drive', 15.99, 500)  # ID 5
    ]
    insert_many_products(conn, products_to_insert)

    # 2. 查询所有 (用于确认 ID)
    select_all_products(cursor)

    # ⭐ 3. 批量查询示例
    # 假设我们要查询 ID 1 (Smart TV) 和 ID 4 (Gaming Console)
    ids_to_query = [1, 4]
    select_by_id_list(cursor, ids_to_query)

    # 4. 单个更新 (改)
    update_product_price(conn, 2, 699.00)

    # 5. 批量更新 (批量改)
    updates_data = [
        (45, 1),
        (550, 5)
    ]
    update_many_quantities(conn, updates_data)

    # 6. 再次进行批量查询，查看 ID 1 的数量是否改变
    ids_to_query_2 = (1, 2)
    select_by_id_list(cursor, ids_to_query_2)

    # 7. 关闭连接
    close_database(conn)