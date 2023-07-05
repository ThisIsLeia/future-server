from flask import Flask, render_template
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from future.config import config
from flask_login import LoginManager

# 建立實體
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

# 在 login_manager 的 login_view 屬性，指定未登入時重新導向端點
login_manager.login_view = "auth.signup"
# 在 login_manager 的 login_message 屬性，指定登入後的顯示訊息
login_manager.login_message = ""

# 傳送組態key
def create_app(config_key):
    """建立 create_app"""
    app = Flask(__name__)

    # 加載config_key配對的環境組態類別
    app.config.from_object(config[config_key])

    # # 設定應用程式的組態
    # app.config.from_mapping(
    #     SECRET_KEY="jlhvgo76fliuhbluyf",
    #     # mysql+pymysql://username:password@localhost/db_name?charset=utf8mb4
    #     SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@0.0.0.0:3306/future?charset=utf8mb4',
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # 設定在控制台日誌輸出SQL
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="femwgjfnloirjg;qpeor"
    # )

    # 連結 SQLAlchemy 和應用程式
    db.init_app(app)
    # 連結 migrate 和應用程式
    Migrate(app, db)

    csrf.init_app(app)

    login_manager.init_app(app)

    from future.user import views as user_views
    from future.auth import views as auth_views
    from future.detector import views as detector_views

    app.register_error_handler(404, page_not_foind)
    app.register_error_handler(500, internal_server_error)

    app.register_blueprint(user_views.user, url_prefix='/user')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')
    app.register_blueprint(detector_views.dt) # 不指定 url_prefix 以便物件偵測應用程式當作應用程式路由

    return app


def page_not_foind(e):
    """ 404 Not Found """
    return render_template('404.html'), 404


def internal_server_error(e):
    """ 500 Internal Server Error """
    return render_template('500.html'), 500