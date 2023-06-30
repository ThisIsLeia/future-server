from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class SignupForm(FlaskForm):
    username = StringField(
        "使用者名稱",
        validators=[
            DataRequired(message = "必填填寫使用者名稱"),
            length(max=30, message = "請勿輸入超過30個字元")
        ],
    )

    email = StringField(
        "電子郵件",
        validators=[
            DataRequired(message = "必填填寫電子郵件"),
            Email(message = "請依照電子郵件格式輸入")
        ],
    )

    password = PasswordField(
        "密碼",
        validators=[
            DataRequired(message = "必填填寫密碼")
        ],
    )

    submit = SubmitField("提交表單")



class LoginForm(FlaskForm):
    email = StringField(
        "電子郵件",
        validators=[
            DataRequired(message = "必填填寫電子郵件"),
            Email(message = "請依照電子郵件格式輸入")
        ],
    )

    password = PasswordField(
        "密碼",
        validators=[
            DataRequired(message = "必填填寫密碼")
        ],
    )

    submit = SubmitField("登入") 