from flask import Flask
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

    from future.crud import views as crud_views
    from future.auth import views as auth_views

    app.register_blueprint(crud_views.crud, url_prefix='/crud')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')
    return app