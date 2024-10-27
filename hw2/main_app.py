import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for

# 獲取資料表中的所有資料
def get_data(table_name):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306  # 使用正確的端口
        )
        if connection.is_connected():
            print(f"成功連接到資料庫: {table_name}")
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"成功獲取資料: {rows}")  # 顯示獲取到的資料
        return rows
    except Error as e:
        print(f"資料庫連接錯誤: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連接已關閉")

# 插入資料到指定的表
def insert_data(table_name, id, value):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        if connection.is_connected():
            print(f"成功連接到資料庫: {table_name}")
        cursor = connection.cursor()
        if table_name == 'teacher':
            sql = "INSERT INTO teacher (id, teacher_name) VALUES (%s, %s)"
        elif table_name == 'subject':
            sql = "INSERT INTO subject (id, subject_name) VALUES (%s, %s)"
        else:
            sql = "INSERT INTO country (id, country_name) VALUES (%s, %s)"
        cursor.execute(sql, (id, value))
        connection.commit()
        print(f"成功插入資料: {id}, {value}")
    except Error as e:
        print(f"插入錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連接已關閉")

# 從指定的表中刪除資料
def delete_data(table_name, id):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        if connection.is_connected():
            print(f"成功連接到資料庫: {table_name}")
        cursor = connection.cursor()
        sql = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
        print(f"成功刪除資料: {id}")
    except Error as e:
        print(f"刪除錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連接已關閉")

# 連接三個表並查詢
def join_tables():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        if connection.is_connected():
            print("成功連接到資料庫: join")
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT teacher.id, teacher.teacher_name, subject.subject_name, country.country_name
        FROM teacher
        JOIN subject ON teacher.id = subject.id
        JOIN country ON teacher.id = country.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"成功獲取連接查詢資料: {rows}")  # 顯示獲取到的資料
        return rows
    except Error as e:
        print(f"連接查詢錯誤: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連接已關閉")

# 更新指定表中的資料
def update_data(table_name, id, value):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  # 修改為正確的主機
            user="root",
            password="",
            database="employeesystem",
            port=3306
        )
        if connection.is_connected():
            print(f"成功連接到資料庫: {table_name}")
        cursor = connection.cursor()
        if table_name == 'teacher':
            sql = "UPDATE teacher SET teacher_name = %s WHERE id = %s"
        elif table_name == 'subject':
            sql = "UPDATE subject SET subject_name = %s WHERE id = %s"
        else:
            sql = "UPDATE country SET country_name = %s WHERE id = %s"
        cursor.execute(sql, (value, id))
        connection.commit()
        print(f"成功更新資料: {id}, {value}")
    except Error as e:
        print(f"更新錯誤: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連接已關閉")

app = Flask(__name__)

# 路由設定
@app.route('/')
def index():
    teachers = get_data("teacher")
    subjects = get_data("subject")
    countries = get_data("country")
    return render_template('index.html', teachers=teachers, subjects=subjects, countries=countries)

@app.route('/add', methods=['POST'])
def add():
    table_name = request.form['table']
    id = request.form['id']
    value = request.form['value']
    insert_data(table_name, id, value)
    return redirect(url_for('index'))

@app.route('/delete/<table>/<int:id>', methods=['POST'])
def delete(table, id):
    delete_data(table, id)
    return redirect(url_for('index'))

@app.route('/join')
def show_join():
    joined_data = join_tables()  # 獲取 JOIN 查詢結果
    return render_template('join_results.html', data=joined_data)

@app.route('/update/<table>/<int:id>', methods=['POST'])
def update(table, id):
    value = request.form['value']
    update_data(table, id, value)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
