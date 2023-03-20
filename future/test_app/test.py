from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, future-server'


@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):
    return render_template('test.html', name=name)
