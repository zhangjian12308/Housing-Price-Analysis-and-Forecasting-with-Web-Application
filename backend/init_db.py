import sqlite3

# 连接 SQLite 数据库
conn = sqlite3.connect("housing_data.db")
cursor = conn.cursor()

# 创建 housing_prices 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS housing_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT,
        date TEXT,
        price REAL
    )
""")

# 插入示例数据
data = [
    ("New York", "2023-01-01", 500000),
    ("New York", "2023-02-01", 505000),
    ("New York", "2023-03-01", 510000),
    ("Los Angeles", "2023-01-01", 700000),
    ("Los Angeles", "2023-02-01", 710000),
    ("Los Angeles", "2023-03-01", 720000),
]

cursor.executemany("INSERT INTO housing_prices (region, date, price) VALUES (?, ?, ?)", data)
conn.commit()
conn.close()

print("SQLite 数据库 housing_data.db 生成完成！")
