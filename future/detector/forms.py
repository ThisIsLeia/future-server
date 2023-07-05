from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    # 在檔案欄位設定所需驗證
    image = FileField(
        validators=[
            FileRequired('請指定圖片檔案'),
            FileAllowed(['png', 'jpg', 'jpeg'], '不支援該圖片格式')
        ]
    )

    submit = SubmitField('上傳')



class DetectorForm(FlaskForm):
    submit = SubmitField('檢測')



class DeleteForm(FlaskForm):
    submit = SubmitField('刪除')