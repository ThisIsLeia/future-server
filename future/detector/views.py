from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for
from future.app import db
from future.user.models import User
from future.detector.models import UserImage
import uuid
from pathlib import Path
from future.detector.forms import UploadImageForm
from flask_login import current_user, login_required

dt = Blueprint('detector', __name__, template_folder='templates')


@dt.route('/')
def index():
    """連結 User & UserImage 取得圖片列表"""
    # user_images = (
    #     db.session.query(User, UserImage)
    #     .join(UserImage)
    #     .filter(User.id == UserImage.user_id)
    #     .all()
    # ) 
    # [(<User 4>, <UserImage 1>)] # <class 'list'>

    user_images = db.session.query(
        User, UserImage).join(UserImage).filter(User.id == UserImage.user_id).all()
    # [(<User 4>, <UserImage 1>)] # <class 'list'>
    
    return render_template('detector/index.html', user_images=user_images)


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
        )

        print('image_path====>', image_path)

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