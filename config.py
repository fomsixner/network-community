#数据库文件路径
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:201609@localhost:3306/mydatabase"
#SQLALCHEMY_DATABASE_URI = r"sqlite:///E:\web\network-community\foo.db"
#每次请求结束都会自动提交数据库的变动
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

#启用CSRF保护的话，表单验证时会有一些问题
WTF_CSRF_ENABLED = False

SECRET_KEY = "123456"



#验证码
MAIL_SERVER = "smtp.126.com"
MAIL_PORT = "465"
MAIL_USE_TLS = False
MAIL_USE_SSL = True        #网易126邮箱使用SSL
MAIL_USERNAME = "net_community@126.com"
MAIL_PASSWORD = "python123"         #授权码
MAIL_DEFAULT_SENDER = "net_community@126.com"