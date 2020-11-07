from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient('localhost', 27017).dbTest

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
def get_articles():
    result = list(db.posts.find({}))
    return jsonify({'result': 'success's})

@app.route('/memo', methods=['POST'])
def post_articles():
    post_title = request.form['client_title']
    post_content = request.form['client_content']
    article = {'client_title':post_title, 'client_content': post_content}
    db.posts.insert_one(article)
    return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)