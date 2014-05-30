from datetime import datetime
from flask import Flask
from flask import json, jsonify, render_template, request
from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        with open(DATA_DIR.child('data.json'), 'r') as f:
            return jsonify(json.load(f))
    elif request.method == 'POST':
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        for filename in ('data.json', 'data.{}.json'.format(ts)):
            with open(DATA_DIR.child(filename), 'w') as f:
                json.dump(request.json, f, indent=2)
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
