from pathlib import Path

basedir = Path(__file__).parent.parent

# 建立 BaseConfig 類別
class BaseConfig:
    SECRET_KEY = 'jlhvgo76fliuhbluyf',
    WTF_CSRF_SECRET_KEY = "femwgjfnloirjg;qpeor"


# 繼承 BaseConfig 類別，建立 LocalConfig 類別
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@0.0.0.0:3306/future?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 設定在控制台日誌輸出SQL
    SQLALCHEMY_ECHO = True


# 繼承 BaseConfig 類別，建立 TestingConfig 類別
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@0.0.0.0:3306/future?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLE = False

# 建立組態字典
config = {
    'testing': TestingConfig,
    'local': LocalConfig
}