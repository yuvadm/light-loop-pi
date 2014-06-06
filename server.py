from datetime import datetime
from flask import Flask
from flask import json, jsonify, render_template, request
from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

def save_json(data, filename):
    with open(DATA_DIR.child(filename), 'w') as f:
        json.dump(data, f, indent=2)

def save_raw(data, filename):
    with open(DATA_DIR.child(filename), 'w') as f:
        f.write('{}\n\n'.format(data['tempo']))
        for tree in data['trees']:
            for row in tree:
                f.write(''.join(map(str, row)) + '\n')
            f.write('\n')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        with open(DATA_DIR.child('data.json'), 'r') as f:
            return jsonify(json.load(f))
    elif request.method == 'POST':
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_json(request.json, 'data.json')
        save_json(request.json, 'data.{}.json'.format(ts))
        save_raw(request.json, 'data.txt')
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
