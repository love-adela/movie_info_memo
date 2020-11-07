from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

db = MongoClient('localhost', 27017).dbJungleTest

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def get_articles():
    result = list(db.articles.find())
    return jsonify({'result': 'success', 'articles': result})

@app.route('/api', methods=['POST'])
def post_articles():
    article = request.get_json()
    if not (article['title'] and article['content']):
        return jsonify({'result': 'failed'}), 400

    # TODO: 에러 핸들링
    db.articles.insert_one({
        'title': article['title'],
        'content': article['content']
    })
    return jsonify({'result': 'success', 'msg':'글이 작성되었습니다.'})

@app.route('/api/<id>', methods=['PUT'])
def update_articles(id):
    article = request.get_json()
    if not (article['title'] and article['content']):
        return jsonify({'result': 'failed'}), 400

    result = db.articles.update_one({'_id': ObjectId(id)},
        {
            '$set': {
                'title': article['title'],
                'content': article['content']
            }
        }
    )
    if result.modified_count == 0:
        return jsonify({'result': 'failed'}), 400

    return jsonify({'result': 'success', 'msg':'글이 수정되었습니다.'})

@app.route('/api/<id>', methods=['DELETE'])
def delete_articles(id):
    db.articles.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': 'success'})

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)