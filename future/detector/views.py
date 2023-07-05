from flask import (
    Blueprint, render_template, current_app, 
    send_from_directory, redirect, url_for, flash, request
    )
from future.app import db
from future.user.models import User
from future.detector.models import UserImage, UserImageTag
import uuid
from pathlib import Path
from future.detector.forms import UploadImageForm, DetectorForm, DeleteForm
from flask_login import current_user, login_required
import random, cv2, torch, torchvision
import numpy as np
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError

dt = Blueprint('detector', __name__, template_folder='templates')


@dt.route('/')
def index():
    """連結 User & UserImage 取得圖片列表"""
    user_images = db.session.query(
        User, UserImage).join(UserImage).filter(User.id == UserImage.user_id).all()
    # [(<User 4>, <UserImage 1>)] # <class 'list'>

    # 取得標記列表
    user_image_tag_dict = {}
    for user_image in user_images:
        # 取得綁定圖片的標記列表
        user_image_tags = db.session.query(
            UserImageTag).filter(
            UserImageTag.user_image_id == user_image.UserImage.id).all()
        
        user_image_tag_dict[user_image.UserImage.id] = user_image_tags

    return render_template(
        'detector/index.html', 
        user_images=user_images,
        # 將標記列表傳給模板
        user_image_tag_dict = user_image_tag_dict,
        # 將物件偵測表單傳給模板
        detector_form=DetectorForm(),
        delete_form=DeleteForm()
    )


@dt.route('/images/<path:filename>')
def image_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@dt.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        # 取得檔案名稱和副檔名 將檔案名稱轉變為 uuid
        ext = Path(file.filename).suffix # ext == .jpg # Path(file.filename) == pizza.jpg
        image_uuid_file_name = str(uuid.uuid4()) + ext # e55d0ee9-98f5-4c83-9a1b-55ede8a3008a.jpg

        # 儲存圖片
        image_path = Path(
            current_app.config['UPLOAD_FOLDER'], image_uuid_file_name
        ) # /Users/leia/future-server/future/images/ccf9494b-153c-4dae-b405-a62fd185284f.jpg
        file.save(image_path)

        # 存至資料庫
        user_image = UserImage(
            user_id=current_user.id,
            image_path=image_uuid_file_name
        )

        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for('detector.index'))
    return render_template('detector/upload.html', form=form)


@dt.route('/detect/<string:image_id>', methods=['POST'])
@login_required
def detect(image_id):
    user_image =  db.session.query(
        UserImage).filter(UserImage.id == image_id).first()
    
    if user_image is None:
        flash('沒有執行物件偵測的圖片')
        return redirect(url_for('detector.index'))
    
    target_image_path = Path(
        current_app.config['UPLOAD_FOLDER'], user_image.image_path
    )

    tags, detected_image_file_name = exec_detect(target_image_path)

    try:
        save_detected_image_tags(user_image, tags, detected_image_file_name)
    except SQLAlchemyError as e:
        flash('物件偵測處理發生錯誤')
        # 進行撤回
        db.session.rollback()
        # 輸出錯誤日誌
        current_app.logger.error(e)
        return redirect(url_for('detector.index'))
    return redirect(url_for('detector.index'))
    

def make_color(labels):
    """隨機決定框線顏色"""
    colors = [[random.randint(0,255) for _ in range(3)] for _ in labels]
    color = random.choice(colors)
    return color


def make_line(result_image):
    """製作框線"""
    line = round(0.002 * max(result_image.shape[0:2])) + 1
    return line


def draw_lines(c1, c2, result_image, line, color):
    """在圖片添加四角形的框線"""
    cv2.rectangle(result_image, c1, c2, color, thickness=line)
    return cv2


def draw_texts(result_image, line, c1, cv2, color, labels, label):
    """在圖片中添加已經辨識的標籤"""
    display_txt = f'{labels[label]}'
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(
        display_txt, 0, fontScale=line / 3, thickness=font
    )[0]
    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
    cv2.rectangle(result_image, c1, c2, color, -1)
    cv2.putText(
        result_image,
        display_txt,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        lineType=cv2.LINE_AA
    )
    return cv2


def exec_detect(target_image_path):
    # 加載標籤
    labels = current_app.config['LABELS']
    # 加載圖片
    image = Image.open(target_image_path)
    # 將圖片資料轉成張量(tensor)型態的數值資料
    image_tensor = torchvision.transforms.functional.to_tensor(image)

    # 加載已學習模型
    model = torch.load(Path(current_app.root_path, 'detector', 'model.pt'))
    # 切換模型的推論模式
    model = model.eval()
    # 執行推論
    output = model([image_tensor])[0]

    tags = []
    result_image = np.array(image.copy())

    # 在圖片添加模型已識別的物體處理
    for box, label, score in zip(
        output['boxes'], output['labels'], output['scores']
    ):
        if score >0.5 and labels[label] not in tags:
                # 決定框線的顏色
            color = make_color(labels)
            # 製作匡線
            line = make_line(result_image)
            # 偵測圖片和文字標籤的框線位置資訊
            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))
            # 在圖片添加匡線
            cv2 = draw_lines(c1, c2, result_image, line, color)
            # 在圖片添加文字標籤
            cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)
            tags.append(labels[label])
    # 產生已識別的圖像檔案名稱
    detected_image_file_name = str(uuid.uuid4()) + '.jpg'
    # 取得圖片複製目的地的路徑
    detected_image_file_path = str(
        Path(current_app.config['UPLOAD_FOLDER'],
             detected_image_file_name)
    )
    # 將加工後的圖片檔案複製至儲存目的地
    cv2.imwrite(
        detected_image_file_path, cv2.cvtColor(
            result_image, cv2.COLOR_RGB2BGR
        )
    )

    return tags, detected_image_file_name


def save_detected_image_tags(user_image, tags, detected_image_file_name):
    """將已識別的圖片儲存位置路徑存置資料庫"""
    user_image.image_path = detected_image_file_name
    user_image.is_detected = True
    db.session.add(user_image)

    # 建立 user_images_tags 紀錄
    for tag in tags:
        user_image_tag = UserImageTag(
            user_image_id=user_image.id, tag_name=tag
        )
        db.session.add(user_image_tag)

    db.session.commit()


@dt.route('/images/delete/<string:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    """刪除已上傳、已識別圖片"""
    try:
        # 由 user_image_tags 表格刪除
        db.session.query(UserImageTag).filter(
            UserImageTag.user_image_id == image_id
        ).delete()

        # 由 user_images 表格刪除
        db.session.query(UserImage).filter(
            UserImage.id == image_id).delete()
        
        db.session.commit()

    except SQLAlchemyError as e:
        flash('圖片刪除處理發生錯誤')
        # 輸出錯誤日誌
        current_app.logger.error(e)
        db.session.rollback()

    return redirect(url_for('detector.index'))


@dt.route('/images/search', methods=['GET'])
def search():
    user_images = db.session.query(User, UserImage).join(
        UserImage, User.id  == UserImage.user_id
    )

    search_text = request.args.get('search')
    user_image_tag_dict = {}
    filtered_user_images = []

    for user_image in user_images:
        # 當搜尋空白時取得所有標記
        if not search_text:
            user_image_tags = db.session.query(UserImageTag).filter(
                UserImageTag.user_image_id == user_image.UserImage.id
            ).all()

        # 取得關鍵字標記
        else:
            user_image_tags = db.session.query(UserImageTag).filter(
                UserImageTag.user_image_id == user_image.UserImage.id
            ).filter(UserImageTag.tag_name.like(
                "%" + search_text +"%"
            )).all()

        # 若找不到標記則不回傳圖片
        if not user_image_tags:
            continue
        
        # 找到標記時，重新取得標記資訊
        user_image_tags = db.session.query(UserImageTag).filter(
            UserImageTag.user_image_id == user_image.UserImage.id).all()
        
        # 字典 key : value -> user_image_id : 標記
        user_image_tag_dict[user_image.UserImage.id] = user_image_tags

        # 使用陣列設置篩選結果的 user_image 資訊
        filtered_user_images.append(user_image)

    return render_template(
        'detector/index.html',
        user_images = filtered_user_images,
        user_image_tag_dict=user_image_tag_dict,
        delete_form = DeleteForm(),
        detector_form = DetectorForm()
    )


@dt.errorhandler(404)
def page_not_found(e):
    return render_template('detector/404.html'), 404