from flask import Flask, render_template_string
import MySQLdb

app = Flask(__name__)

# 配置 MySQL 数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jason930520'
app.config['MYSQL_DB'] = 'world'

# 初始化 MySQL 连接
def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    
    # 查询 world 数据库的全部表内容（假设要查询某个具体表格，比如 city 表）
    cursor.execute("SELECT * FROM city")
    rows = cursor.fetchall()

    # 动态生成 HTML 页面来显示查询结果
    html_template = """
    <h1>World Schema - City Table</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>CountryCode</th>
            <th>District</th>
            <th>Population</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    
    return render_template_string(html_template, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
