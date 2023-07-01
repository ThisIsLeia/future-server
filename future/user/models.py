from datetime import datetime
from future.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



# 建立繼承 db.Model 和 UserMixin 的 User類別
class User(db.Model, UserMixin):

    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 對其他表進行雙向關聯，由 user 物件呼叫 UserImage 的物件（欄位），如 user.user_images
    # 一對多 輸出結果為 UserImages 物件陣列
    user_images = db.relationship('UserImage', backref='user')

    @property
    def password(self):
        """設置密碼的屬性"""
        raise AttributeError("無法加載")
    

    @password.setter
    def password(self, password):
        """藉由設置密碼屬性的setter函數 設定經過雜湊處理的密碼"""
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        """檢測密碼"""
        return check_password_hash(self.password_hash, password)
    

    def is_duplicate_email(self):
        """檢測電子郵件是否使用過"""
        return User.query.filter_by(email=self.email).first() is not None
    

@login_manager.user_loader
def load_user(user_id):
    """取得登入使用者的資訊"""
    return User.query.get(user_id)