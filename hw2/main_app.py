from flask import Flask, render_template, request, redirect, url_for
from data import get_countries, insert_country, delete_country, update_country

app = Flask(__name__)

@app.route('/')
def index():
    # 獲取 country 資料
    countries = get_countries()
    return render_template('index.html', countries=countries)

@app.route('/add', methods=['POST'])
def add():
    # 新增 country 資料
    id = int(request.form['id'])
    name = request.form['name']
    insert_country(id, name)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # 刪除 country 資料
    delete_country(id)
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    # 更新 country 資料
    name = request.form['name']
    update_country(id, name)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
