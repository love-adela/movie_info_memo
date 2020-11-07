from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient('localhost', 27017).dbJungleTest

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
def get_articles():
    result = list(db.articles.find({}, {'_id':0}))
    return jsonify({'result': 'success', 'articles': result})

@app.route('/memo', methods=['POST'])
def post_articles():
    article = request.get_json()
    if not (article['title'] and article['content']):
        return jsonify({'result': 'failed'}), 400

    db.articles.insert_one(article)
    return jsonify({'result': 'success', 'msg':'글이 작성되었습니다.'})

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)