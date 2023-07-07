 # future-server
 ## 虛擬環境
 ### pyenv
 ```
 # 可以用的 python 版本
pyenv versions

# 當前使用版本
python --version

# 下載特定版本 python
pyenv install <版本號>
 ```
 ### pyenv virtualenv
 ```
 # 創建虛擬環境及指定 Python 版本
 pyenv virtualenv 3.11.3 pyenv_future

# 專案指定虛擬環境
 cd <專案資料夾>
 pyenv local pyenv_future
 ```


## 啟動專案
```
flask run
```


## 資料庫
### 初始化資料庫
`flask db init`
### 資料庫腳本遷移
`flask db migrate -m"更新內容"`
### 升級資料庫
`flask db upgrade`

## 模型啟用方法
 若應用程式(detector)欲取得已學習模型<br>
 執行以下指令後，將 model.pt 檔案存至目標應用資料夾(detector)

```
terminal
 > python
 > import torch
 > import torchvision
 > model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
 > torch.save(model, 'model.pt')
 ```

 ## 測試
 ### 不指定測試（全部都跑）
 `pytest`
 ### 測試覆蓋率
 ```
 cd tests
 pytest detector --cov=../future/detector
 ```