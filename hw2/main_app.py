from flask import Flask, render_template_string, request, redirect, url_for
import MySQLdb

app = Flask(__name__)  


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jason930520'
app.config['MYSQL_DB'] = 'employeesystem'


def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db_connection()
    cursor = db.cursor()
    
    # 顯示三個表的資料
    cursor.execute("SELECT * FROM country")
    country_rows = cursor.fetchall()
    cursor.execute("SELECT * FROM subject")
    subject_rows = cursor.fetchall()
    cursor.execute("SELECT id, teacher_name FROM teacher")
    teacher_rows = cursor.fetchall()

    # 如果是 POST 請求，則處理添加資料的表單
    if request.method == 'POST':
        table = request.form['table']
        new_id = request.form['new_id']
        new_content = request.form['new_content']

        if table == 'country':
            cursor.execute("INSERT INTO country (id, country_name) VALUES (%s, %s)", (new_id, new_content))
        elif table == 'subject':
            cursor.execute("INSERT INTO subject (id, subject_name) VALUES (%s, %s)", (new_id, new_content))
        elif table == 'teacher':
            cursor.execute("INSERT INTO teacher (id, teacher_name) VALUES (%s, %s)", (new_id, new_content))

        db.commit()
        return redirect(url_for('index'))

    # HTML 模板 (使用 Bootstrap 美化)
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Employee System - Data Management</h1>
        
        <!-- 表單添加資料 -->
        <form method="POST" action="/" class="row g-3 mb-5">
            <div class="col-md-4">
                <label for="table" class="form-label">Select Table:</label>
                <select name="table" id="table" class="form-select">
                    <option value="country">Country</option>
                    <option value="subject">Subject</option>
                    <option value="teacher">Teacher</option>
                </select>
            </div>
            <div class="col-md-3">
                <label for="new_id" class="form-label">ID:</label>
                <input type="text" name="new_id" id="new_id" class="form-control" required>
            </div>
            <div class="col-md-3">
                <label for="new_content" class="form-label">Content:</label>
                <input type="text" name="new_content" id="new_content" class="form-control" required>
            </div>
            <div class="col-md-2 d-grid">
                <button type="submit" class="btn btn-primary mt-4">Add Data</button>
            </div>
        </form>

        <!-- 顯示 Country 表 -->
        <h2 class="mt-4">Country Table</h2>
        <table class="table table-striped table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Country Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {% for row in country_rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>
                        <form method="POST" action="/update/country/{{ row[0] }}" class="d-flex">
                            <input type="text" name="new_value" class="form-control" value="{{ row[1] }}">
                            <button type="submit" class="btn btn-warning btn-sm ms-2">Update</button>
                        </form>
                    </td>
                    <td>
                        <a href="/delete/country/{{ row[0] }}" class="btn btn-danger btn-sm">Delete</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <!-- 顯示 Subject 表 -->
        <h2 class="mt-4">Subject Table</h2>
        <table class="table table-striped table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Subject Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {% for row in subject_rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>
                        <form method="POST" action="/update/subject/{{ row[0] }}" class="d-flex">
                            <input type="text" name="new_value" class="form-control" value="{{ row[1] }}">
                            <button type="submit" class="btn btn-warning btn-sm ms-2">Update</button>
                        </form>
                    </td>
                    <td>
                        <a href="/delete/subject/{{ row[0] }}" class="btn btn-danger btn-sm">Delete</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <!-- 顯示 Teacher 表 -->
        <h2 class="mt-4">Teacher Table</h2>
        <table class="table table-striped table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Teacher Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {% for row in teacher_rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>
                        <form method="POST" action="/update/teacher/{{ row[0] }}" class="d-flex">
                            <input type="text" name="new_value" class="form-control" value="{{ row[1] }}">
                            <button type="submit" class="btn btn-warning btn-sm ms-2">Update</button>
                        </form>
                    </td>
                    <td>
                        <a href="/delete/teacher/{{ row[0] }}" class="btn btn-danger btn-sm">Delete</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <!-- JOIN 按鈕 -->
        <form method="POST" action="/join" class="mt-4">
            <button type="submit" class="btn btn-success">Join Tables</button>
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    return render_template_string(html_template, country_rows=country_rows, subject_rows=subject_rows, teacher_rows=teacher_rows)

@app.route('/join', methods=['POST'])
def join_tables():
    db = get_db_connection()
    cursor = db.cursor()

    # Join 三個表
    cursor.execute("""
        SELECT teacher.id, teacher.teacher_name, country.country_name, subject.subject_name
        FROM teacher
        JOIN country ON teacher.id = country.id
        JOIN subject ON teacher.id = subject.id
    """)
    joined_rows = cursor.fetchall()

    # 顯示 JOIN 結果
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Joined Data</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Joined Data</h1>
        <table class="table table-striped table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Teacher Name</th>
                    <th>Country Name</th>
                    <th>Subject Name</th>
                </tr>
            </thead>
            <tbody>
            {% for row in joined_rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        <br>
        <a href="/" class="btn btn-primary">Back</a>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    return render_template_string(html_template, joined_rows=joined_rows)

# 更新資料
@app.route('/update/<table>/<int:id>', methods=['POST'])
def update(table, id):
    db = get_db_connection()
    cursor = db.cursor()

    new_value = request.form['new_value']
    if table == 'country':
        cursor.execute("UPDATE country SET country_name = %s WHERE id = %s", (new_value, id))
    elif table == 'subject':
        cursor.execute("UPDATE subject SET subject_name = %s WHERE id = %s", (new_value, id))
    elif table == 'teacher':
        cursor.execute("UPDATE teacher SET teacher_name = %s WHERE id = %s", (new_value, id))
    db.commit()
    return redirect(url_for('index'))

# 刪除資料
@app.route('/delete/<table>/<int:id>', methods=['GET'])
def delete(table, id):
    db = get_db_connection()
    cursor = db.cursor()

    if table == 'country':
        cursor.execute("DELETE FROM country WHERE id = %s", (id,))
    elif table == 'subject':
        cursor.execute("DELETE FROM subject WHERE id = %s", (id,))
    elif table == 'teacher':
        cursor.execute("DELETE FROM teacher WHERE id = %s", (id,))
    
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
