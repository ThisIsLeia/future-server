from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# 建立 SQLAlchemy實體
db = SQLAlchemy()

csrf = CSRFProtect()

def create_app():
    """建立 create_app"""
    app = Flask(__name__)

    # 設定應用程式的組態
    app.config.from_mapping(
        SECRET_KEY="jlhvgo76fliuhbluyf",
        # mysql+pymysql://username:password@localhost/db_name?charset=utf8mb4
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@0.0.0.0:3306/future?charset=utf8mb4',
        SQLALCHEY_TRACK_MODIFICATIONS=False,
        # 設定在控制台日誌輸出SQL
        SQLALCHEY_ECHO=True,
        WTF_CSRF_SECRET_KEY="femwgjfnloirjg;qpeor"
    )

    # 連結 SQLAlchemy和應用程式
    db.init_app(app)
    # 連結 migrate和應用程式
    Migrate(app, db)

    csrf.init_app(app)

    from future.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix='/crud')
    return app