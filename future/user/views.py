from flask import Blueprint, render_template, redirect, url_for
from future.app import db
from future.user.models import User
from future.user.forms import UserForm
from flask_login import login_required


# 使用 Blueprint 建立 user 應用程式
user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# 建立 index 端點並回傳 index.html
@user.route("/")
@login_required
def index():
    return render_template('user/index.html')


@user.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return '請控制台日誌'


@user.route("/user/new", methods=['get', 'post'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        # 重新導向使用者列表頁面
        return redirect(url_for('user.users'))
    return render_template('user/create.html', form=form)


@user.route("/users")
@login_required
def users():
    """取得使用者列表"""
    users = User.query.all()
    return render_template('user/index.html', users=users)


@user.route("/users/<user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """編輯使用者"""
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    # 發送表單後修改內容並重新導向使用者列表
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        # 重新導向使用者列表頁面
        return redirect(url_for('user.users'))
    # 請求方法為get時回傳
    return render_template('user/edit.html', user=user, form=form)


@user.route("/users/<user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    """刪除使用者"""
    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()
    # 重新導向使用者列表頁面
    return redirect(url_for('user.users'))