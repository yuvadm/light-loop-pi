from flask import Flask
from flask import render_template, request
from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().child('data')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return 'hai'
    elif request.method == 'POST':
        print request.json
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
