"""
    Created by zltningx on 18-4-29.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    admin = StringField("Username", validators=[DataRequired(),
                                                Length(3, 20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    ip = TextAreaField("Ip", validators=[DataRequired(), Length(1, 512)],
                               render_kw={"placeholder":
                                          "请输入ip地址"
                                          ",多个地址请使用逗号隔开,"
                                          "或使用ip段如192.168.1.1/24"
                                          ",或给定start ip 和 end ip使用空格隔开"
                                          "如192.168.1.1 192.168.2.1"},
                               description="输入ip开始扫描")
    port = StringField("Port", validators=[Length(0, 128)],
                       render_kw={"placeholder":
                                  "多个端口使用逗号隔开，不填则使用默认端口集"})
    submit = SubmitField("Start")


class PortScanForm(FlaskForm):
    ip = TextAreaField("Ip", validators=[DataRequired(), Length(1, 512)],
                               render_kw={"placeholder":
                                          "请输入ip地址"
                                          ",多个地址请使用逗号隔开,"
                                          "或使用ip段如192.168.1.1/24"
                                          ",或给定start ip 和 end ip使用空格隔开"
                                          "如192.168.1.1 192.168.2.1"},
                               description="输入ip开始扫描")
    submit = SubmitField("Start")