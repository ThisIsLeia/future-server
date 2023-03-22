from flask import Flask, render_template, url_for, request, url_for, redirect, flash, json
from voluptuous import Schema, Required, All, Length
from future.decorators import dataschema
import logging
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aosdiuhfpqo9ui'

# 設定日誌級別
app.logger.setLevel(logging.DEBUG)
# 避免中斷重新導向
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# 在 DebugToolbarExtension 設置應用程式
toolbar = DebugToolbarExtension(app)
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

# 增加 Mail 類別的組態
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS")
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")
mail = Mail(app)


@app.route('/')
def test_template():
    return render_template('contact_mail.html', username='Leia', content='測試')


@app.route('/contact')
def contact():
    return render_template('contact.html')

def send_email(to, subject, template, **kwargs):
    # 同時建立並傳送html和txt郵件，當html郵件遭拒便傳送純文字txt
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route('/contact/complete', methods=['POST'])
@dataschema(Schema({
    Required('username'): All(str, Length(min=1, msg="請輸入使用者名稱")),
    Required('email'): All(str, Length(min=1, msg="請輸入電子郵件地址")),
    Required('content'): All(str, Length(min=1, msg="請輸入諮詢內容"))}))
def contact_complete(**kwargs):
    send_email(
        kwargs['email'],
        "感謝您來信諮詢，我們將會盡快回覆",
        "contact_mail",
        username=kwargs['username'],
        content=kwargs['content'],
    )
    return redirect(url_for('contact_settle', content=kwargs['content']))


@app.route('/contact/settle')
def contact_settle():
    content = request.args.get('content', '')
    return render_template('contact_complete.html', content=content)
