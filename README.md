 future-server

 detector 取得已學習模型
 執行以下指令後，將 model.pt 檔案存至 detector 資料夾
 
 (terminal) python
 >>> import torch
 >>> import torchvision
 >>> modle = torchvision.models.detectioin.maskrcnn_resnet50_fpn(pretrained=True)
 >>> torch.save(model, 'model.pt')