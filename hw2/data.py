import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jason930520",  # 使用您的 MySQL 密碼
        database="employeesystem",
        port=3306  # 修改為您的 MySQL 連接埠，若為 3307，請改為 3307
    )

# 獲取所有國家資料
def get_countries():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM country")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Database connection error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 獲取所有學科資料
def get_subjects():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subject")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Database connection error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 獲取所有老師資料
def get_teachers():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teacher")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Database connection error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 插入數據
def insert_data(table, id, name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if table == 'country':
            sql = "INSERT INTO country (id, country_name) VALUES (%s, %s)"
        elif table == 'subject':
            sql = "INSERT INTO subject (id, subject_name) VALUES (%s, %s)"
        elif table == 'teacher':
            sql = "INSERT INTO teacher (id, teacher_name) VALUES (%s, %s)"
        cursor.execute(sql, (id, name))
        connection.commit()
    except Error as e:
        print(f"Insert error in {table}: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 刪除數據
def delete_data(table, id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = f"DELETE FROM {table} WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
    except Error as e:
        print(f"Delete error in {table}: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 更新數據
def update_data(table, id, name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if table == 'country':
            sql = "UPDATE country SET country_name = %s WHERE id = %s"
        elif table == 'subject':
            sql = "UPDATE subject SET subject_name = %s WHERE id = %s"
        elif table == 'teacher':
            sql = "UPDATE teacher SET teacher_name = %s WHERE id = %s"
        cursor.execute(sql, (name, id))
        connection.commit()
    except Error as e:
        print(f"Update error in {table}: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
