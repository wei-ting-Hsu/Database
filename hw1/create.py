from flask import Flask, render_template_string, request, redirect
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jason930520'
app.config['MYSQL_DB'] = 'testdb'

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

    if request.method == 'POST':
        post_content = request.form['post']
        
        cursor.execute("INSERT INTO example_table (post, created_at) VALUES (%s, NOW())", (post_content,))
        db.commit()
        return redirect('/')
    
    cursor.execute("SELECT * FROM example_table")
    rows = cursor.fetchall()

    html_template = """
    <h1>Example Table</h1>
    
    <form method="POST" action="/">
        <label for="post">Post:</label>
        <input type="text" id="post" name="post" required>
        <input type="submit" value="Submit">
    </form>
    
    <h2>Data in Example Table</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Post</th>
            <th>Created At</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    
    return render_template_string(html_template, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
