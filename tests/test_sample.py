import pytest


def test_func1():
    assert 1 == 1


# 增加
@pytest.fixture
def app_data():
    """當次是會使用到資料庫時
    使用 fixture(夾具) 
    可以在函數執行之前設置資料庫、執行之後清除資料庫"""
    return 3


def test_func2(app_data):
    assert app_data == 3