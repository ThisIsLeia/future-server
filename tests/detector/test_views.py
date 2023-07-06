from pathlib import Path
from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage
from future.detector.models import UserImage


# 測試圖片列表頁面
# 未登入
# 將 fixture 的 client 傳給 test_index 函數
def test_index(client):
    rv = client.get('/') # 使用 client 訪問應用程式路由'/'
    # 執行結果 rv.data 會存至訪問後的 HTML，確認有以下字串
    # 最後結果回傳字節型態 bytes 故以 decode 解碼
    assert '登入' in rv.data.decode()
    assert '新增圖片' in rv.data.decode()


# 登入時
def signup(client, username, email, password):
    """ 進行註冊 """
    data = dict(username=username, email=email, password=password)
    return client.post('/auth/signup', data=data, follow_redirects=True)


def test_index_signup(client):
    """ 執行註冊 """
    rv = signup(client, 'admin', 'test@example.com', 'password')
    assert 'admin' in rv.data.decode()

    rv = client.get('/')
    assert '登出' in rv.data.decode()
    assert '新增圖片' in rv.data.decode()


# 測試圖片上傳頁面
# 未登入 -> 直接跳轉登入頁面
def test_upload_no_auth(client):
    rv = client.get('/upload', follow_redirects=True)
    # 無法訪問圖片上傳頁面
    assert '上傳' not in rv.data.decode()
    # 跳轉登入頁面
    assert '電子郵件' in rv.data.decode()
    assert '密碼' in rv.data.decode()


# 登入
def test_upload_signup_get(client):
    signup(client, 'admin', 'test@example.com', 'password')
    rv = client.get('/upload')
    assert '上傳' in rv.data.decode()


# 測試驗證錯誤時的圖片上傳頁面
def upload_image(client, image_path):
    """ 上傳圖片 """
    image = Path(get_root_path('tests'), image_path)

    test_file = (
        FileStorage(
            stream=open(image, 'rb'),
            filename=Path(image_path).name,
            content_type='multipart/form-data'
        )
    )

    data = dict(image=test_file)

    return client.post('/upload', data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    signup(client, 'admin', 'test@example.com', 'password')
    rv = upload_image(client, 'detector/testdata/test_invalid_file.txt')
    assert '不支援該圖片格式' in rv.data.decode()


def test_upload_signup_post(client):
    signup(client, 'admin', 'test@example.com', 'password')
    rv = upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


# 測試物件偵測與標記搜尋功能
def test_detect_no_user_image(client):
    """ 測試 點擊檢測後驗證錯誤時的情況 """
    signup(client, 'admin', 'test@example.com', 'password')
    upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    # 指定不存在的id
    rv = client.post('/detect/notexistid', follow_redirects=True)
    assert '沒有執行物件偵測的圖片' in rv.data.decode()


def test_detect(client):
    """ 測試 物件偵測成功時 """
    signup(client, 'admin', 'test@example.com', 'password')
    upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    user_image = UserImage.query.first()
    # 執行物件偵測
    rv = client.post(f'/detect/{user_image.id}', follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert 'dog' in rv.data.decode()


def test_detect(client):
    """ 測試 物件偵測成功時 """
    signup(client, 'admin', 'test@example.com', 'password')
    upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    user_image = UserImage.query.first()
    # 執行物件偵測
    rv = client.post(f'/detect/{user_image.id}', follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert 'dog' in rv.data.decode()


def test_detect_search(client):
    """ 測試 物件偵測後標記搜尋 """
    signup(client, 'admin', 'test@example.com', 'password')
    upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    user_image = UserImage.query.first()
    # 執行物件偵測
    client.post(f'/detect/{user_image.id}', follow_redirects=True)

    rv = client.get('/images/search?search=dog')
    # 確認不存在帶有dog標記的圖片
    assert user_image.image_path in rv.data.decode()
    assert 'dog' in rv.data.decode()

    rv = client.get('/images/search?search=test')
    # 確認不存在帶有test標記的圖片
    assert user_image.image_path not in rv.data.decode()
    assert 'dog' not in rv.data.decode()


# 測試圖片刪除功能
def test_delete(client):
    signup(client, 'admin', 'test@example.com', 'password')
    upload_image(client, 'detector/testdata/test_valid_image.jpeg')
    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f'/images/delete/{user_image.id}', follow_redirects=True)
    assert image_path not in rv.data.decode()


def test_custom_error(client):
    rv = client.get('notfonud')
    assert '404 Not Found' in rv.data.decode()