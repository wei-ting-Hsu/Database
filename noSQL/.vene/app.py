from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB 連接配置
client = MongoClient("mongodb://localhost:27017")
db = client['local']
collection = db['startup_log']

@app.route('/')
def index():
    # 加載主頁面
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    # 從前端表單中獲取資料
    country = request.form.get('country')
    occupation = request.form.get('occupation')
    age = request.form.get('age')

    # 插入新資料到 MongoDB
    collection.insert_one({
        "country": country,
        "occupation": occupation,
        "age": int(age)
    })
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['POST'])
def edit_record(id):
    # 從前端表單中獲取更新的資料
    country = request.form.get('country')
    occupation = request.form.get('occupation')
    age = request.form.get('age')

    # 更新 MongoDB 中的資料
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "country": country,
            "occupation": occupation,
            "age": int(age)
        }}
    )
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_record(id):
    # 刪除 MongoDB 中的資料
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/api/records', methods=['GET'])
def get_records():
    # 返回所有資料給前端（JSON 格式）
    records = list(collection.find())
    formatted_records = []
    for record in records:
        formatted_records.append({
            "_id": str(record["_id"]),
            "country": record.get("country", ""),
            "occupation": record.get("occupation", ""),
            "age": record.get("age", "")
        })
    return jsonify({"records": formatted_records})

if __name__ == '__main__':
    app.run(debug=True)
