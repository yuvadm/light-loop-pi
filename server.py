import subprocess

from datetime import datetime
from flask import Flask
from flask import json, jsonify, render_template, request
from unipath import FSPath as Path
from uuid import uuid4

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        with open(DATA_DIR.child('data.txt'), 'r') as f:
            return jsonify({
                'data': f.read()
            })
    elif request.method == 'POST':
        with open(DATA_DIR.child('data.txt'), 'w') as f:
            f.write(request.json['data'])
        with open(DATA_DIR.child('data.{}.txt'.format(uuid4().hex[:10])), 'w') as f:
            f.write(request.json['data'])
        subprocess.call(['supervisorctl', 'restart', 'client'])
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
