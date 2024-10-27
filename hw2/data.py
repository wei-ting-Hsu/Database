import mysql.connector
from mysql.connector import Error

# 獲取資料表中的所有資料
def get_data(table_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306  # 使用正確的端口
        )
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"資料庫連接錯誤: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# 插入資料到指定的表
def insert_data(table_name, id, value):
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        cursor = connection.cursor()
        if table_name == 'teacher':
            sql = "INSERT INTO teacher (id, teacher_name) VALUES (%s, %s)"
        elif table_name == 'subject':
            sql = "INSERT INTO subject (id, subject_name) VALUES (%s, %s)"
        else:
            sql = "INSERT INTO country (id, country_name) VALUES (%s, %s)"
        cursor.execute(sql, (id, value))
        connection.commit()
    except Error as e:
        print(f"插入錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# 從指定的表中刪除資料
def delete_data(table_name, id):
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        cursor = connection.cursor()
        sql = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
    except Error as e:
        print(f"刪除錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# 連接三個表並查詢
def join_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT teacher.id, teacher.teacher_name, subject.subject_name, country.country_name
        FROM teacher
        JOIN subject ON teacher.id = subject.id
        JOIN country ON teacher.id = country.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"連接查詢錯誤: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# 更新指定表中的資料
def update_data(table_name, id, value):
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        cursor = connection.cursor()
        if table_name == 'teacher':
            sql = "UPDATE teacher SET teacher_name = %s WHERE id = %s"
        elif table_name == 'subject':
            sql = "UPDATE subject SET subject_name = %s WHERE id = %s"
        else:
            sql = "UPDATE country SET country_name = %s WHERE id = %s"
        cursor.execute(sql, (value, id))
        connection.commit()
    except Error as e:
        print(f"更新錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
