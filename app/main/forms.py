# from flask.ext.wtf import Form
from flask_wtf import Form
# Form从flask_wtf导入，基于WTForm中的SecureForm类，它能够防止跨站攻击，具有更好的安全性
from wtforms import StringField, SubmitField, TextField, TextAreaField, PasswordField, validators
# 标准字段从wtform导入
from wtforms.validators import DataRequired, Email, Length
# 验证函数从wtform导入


class NameForm(Form):
    name = StringField('姓名', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    name = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(Form):
    email = StringField('Email', validators=[Email(), Length(6, 64)])
    password = PasswordField('密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('密码确认')
    submit = SubmitField('Submit')


class OrderForm(Form):
    id_no = StringField('身份证号', validators=[Length(16, 18)])
    usr_name = StringField('姓名', validators=[Length(2, 10)])
    mobile_no = StringField('联系方式', validators=[Length(8, 11)])
    ps_text = TextAreaField('备注',validators=[Length(0, 50)])
    submit = SubmitField('提交')
