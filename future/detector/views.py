from flask import Blueprint, render_template
from future.app import db
from future.user.models import User
from future.detector.models import UserImage

dt = Blueprint('detector', __name__, template_folder='templates')


@dt.route('/')
def index():
    """連結 User & UserImage 取得圖片列表"""
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    u = db.session.query(User, UserImage
                         ).join(UserImage
                                ).filter(User.id == UserImage.user_id
                                         ).all()
    
    print('user_images=( ===>', user_images, 'user_images type===>', type(user_images))
    print('u', u, 'u type===>', type(u))
    return render_template('detector/index.html', user_images=user_images)