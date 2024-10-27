import mysql.connector

def connect_db():
    # 與 MySQL 資料庫建立連接
    return mysql.connector.connect(
        host="localhost",      # 請替換為您的 MySQL 伺服器主機
        user="root",  # 替換為您的 MySQL 用戶名
        password="jason930520",  # 替換為您的 MySQL 密碼
        database="employeesystem"  # 資料庫名稱
    )

def get_countries():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, country_name FROM country")  # 確認表名稱為 'country'
    countries = cursor.fetchall()
    conn.close()
    return countries

def insert_country(id, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO country (id, country_name) VALUES (%s, %s)", (id, name))
    conn.commit()
    conn.close()

def delete_country(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM country WHERE id = %s", (id,))
    conn.commit()
    conn.close()

def update_country(id, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE country SET country_name = %s WHERE id = %s", (name, id))
    conn.commit()
    conn.close()
