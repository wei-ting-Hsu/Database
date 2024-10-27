from flask import Flask, render_template, request, redirect, url_for
from data import get_countries, get_subjects, get_teachers, insert_data, delete_data, update_data

app = Flask(__name__)

@app.route('/')
def index():
    countries = get_countries()
    subjects = get_subjects()
    teachers = get_teachers()
    return render_template('index.html', countries=countries, subjects=subjects, teachers=teachers)

@app.route('/add', methods=['POST'])
def add():
    table = request.form['table']
    id = request.form['id']
    name = request.form['name']
    insert_data(table, id, name)
    return redirect(url_for('index'))

@app.route('/delete/<table>/<int:id>', methods=['POST'])
def delete(table, id):
    delete_data(table, id)
    return redirect(url_for('index'))

@app.route('/update/<table>/<int:id>', methods=['POST'])
def update(table, id):
    name = request.form['name']
    update_data(table, id, name)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
