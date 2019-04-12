from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class RegistForm(FlaskForm):
    user_name = StringField(
        label="用户名",
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3,max=15, message="用户名长度必须在3到15之间")],
        render_kw={"id":"user_name",
                   "class":"form-control col-md-8",
                   "placeholder":"输入用户名"}
    )

    user_password = StringField(
        label="密码",
        validators=[DataRequired(message="用户密码不能为空！"),
                    Length(min=3, max=15, message="密码长度必须在3到15之间")],
        render_kw={"id": "user_password",
                   "class": "form-control col-md-8",
                   "placeholder": "输入密码"}
    )

    verify_password = StringField(
        label="确认密码",
        validators=[DataRequired(message="确认密码不能为空！"),
                    Length(min=3, max=15, message="密码长度必须在3到15之间")],
        render_kw={"id": "verify_password",
                   "class": "form-control col-md-8",
                   "placeholder": "确认密码"}
    )

    user_email = StringField(
        label="邮箱",
        validators=[DataRequired(message="邮箱不能为空！"),
                    Email(message="邮箱格式错误！")],
        render_kw={"id": "user_email",
                   "class": "form-control col-md-8",
                   "placeholder": "输入邮箱"}
    )

    verification_code = StringField(
        label="验证码",
        validators=[DataRequired(message="验证码不能为空！")],
        render_kw={"id": "verification_code",
                   "class": "form-control col-md-5",
                   "placeholder": "输入验证码"}
    )

    """
    get_verification_code = SubmitField(
        label="获取验证码",
        render_kw={"id":"get_verification_code",
                   "class":"btn btn-group",
                   "value":"获取验证码"}
    )
    """
    submit = SubmitField(
        label="提交",
        render_kw={"class": "btn btn-success offset-md-6",
                   "value": "提交"}
    )
