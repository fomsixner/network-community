from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#让flask-login知道哪个用户视图允许登录
login_manager = LoginManager()
login_manager.init_app(app)

#验证码
mail = Mail()
mail.init_app(app)

#CSRFProtect(app)    #启用csrf保护

from apps import view