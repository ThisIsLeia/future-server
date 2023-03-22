from flask import Flask, render_template, url_for, request, url_for, redirect, flash
from voluptuous import Schema, Required, All, Length
from future.decorators import dataschema

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, future-server'


@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):
    return render_template('test.html', name=name)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/contact/complete', methods=['POST'])
@dataschema(Schema({
    Required('username'): All(str, Length(min=1, msg="請輸入使用者名稱")),
    Required('email'): All(str, Length(min=1, msg="請輸入電子郵件地址")),
    Required('content'): All(str, Length(min=1, msg="請輸入諮詢內容")),
}))
def contact_complete(**kwargs):
    print('username===>', kwargs['username'])
    print('email===>', kwargs['email'])
    print('content===>', kwargs['content'])

    # 傳送電子郵電

    return redirect(url_for('contact_settle'))


@app.route('/contact/settle')
def contact_settle(**kwargs):
    return render_template('contact_complete.html')

