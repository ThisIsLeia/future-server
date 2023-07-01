from flask import Blueprint, render_template, redirect, url_for, flash, request
from future.app import db
from future.user.models import User
from future.auth.forms import SignupForm, LoginForm
from flask_login import login_user, logout_user


# 使用 Blueprint 建立 auth 應用程式
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@auth.route('/')
def index():
    return render_template('auth/index.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 未通過登入驗證 -> 導向註冊頁面
        if user.is_duplicate_email():
            flash("此電子郵件已重複註冊")
            return redirect(url_for('auth.signup'))

        db.session.add(user)
        db.session.commit()

        # 將使用者資訊存入 session，重新導向後直接為登入狀態
        login_user(user)

        # 未通過登入驗證 -> 導向註冊頁面 GET參數的next鍵有值（next鍵加入欲訪問頁面端點)
        # 通過登入驗證 -> 導向使用者列表頁面 GET參數的next鍵沒有值
        next_ = request.args.get('next')
        if next_ is None or not next_.startwith('/'):
            next_ = url_for('user.users')
        return redirect(next_)

    return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('user.users'))
        
        # 設定登入失敗的訊息
        flash('郵件位置或密碼不正確')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))