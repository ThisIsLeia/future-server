import os
import shutil
import pytest
from future.app import create_app, db
from future.user.models import User
from future.detector.models import UserImage, UserImageTag


@pytest.fixture
def fixture_app():
    # 設置處理 
    # 引述指定testing 利用測試用的組態
    app = create_app('testing')

    # 宣告使用資料庫
    # 在應用程式外部操作資料庫會發生錯誤(No application found)
    app.app_context().push() # 將應用程式內文加入堆疊可以避免此問題

    # 建立測試用的資料庫表格
    with app.app_context():
        db.create_all()

    # 建立測試用的圖片上傳目錄
    os.mkdir(app.config['UPLOAD_FOLDER'])

    # 執行測試
    yield app

    # 清除處理
    # 刪除各表格的紀錄
    UserImageTag.query.delete()
    UserImage.query.delete()
    User.query.delete()
    
    # 刪除測試用的圖片上傳目錄
    shutil.rmtree(app.config['UPLOAD_FOLDER'])

    db.session.commit()


@pytest.fixture
def client(fixture_app):
    """ 建立回傳 Flask 測試客戶端的 fixture 函數 """
    return fixture_app.test_client()
