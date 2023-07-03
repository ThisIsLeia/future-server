from pathlib import Path

basedir = Path(__file__).parent.parent

# 建立 BaseConfig 類別
class BaseConfig:
    SECRET_KEY = 'jlhvgo76fliuhbluyf',
    WTF_CSRF_SECRET_KEY = "femwgjfnloirjg;qpeor"
    # 圖片上傳目的地指定
    UPLOAD_FOLDER = str(Path(basedir, 'future', 'images'))
    LABELS = [
        "unlabeled",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "street sign",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "hat",
        "backpack",
        "umbrella",
        "shoe",
        "eye glasses",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "plate",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "mirror",
        "dining table",
        "window",
        "desk",
        "toilet",
        "door",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "blender",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]


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