from apps import db


class GeneralUser(db.Model):
    __tablename__ =  'generalUser'

    userID = db.Column(db.String(36), primary_key=True)              #主键
    userName = db.Column(db.String(10), index=True)
    registerTime = db.Column(db.DateTime)     #注册时间
    email = db.Column(db.String(120))         #电子邮件
    password = db.Column(db.String(20))       #密码
    realName = db.Column(db.String(10))       #真实姓名
    gender = db.Column(db.Enum("男", "女"))   #性别
    birthday = db.Column(db.Date)             #生日
    describe = db.Column(db.String(100))      #个人签名

    #对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边。
    #在这种关系下，我们得到一个 user.posts 成员，它给出一个用户所有的 blog。
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    @property
    def is_authenticated(self):   #属性,判断是否已经授权
        return True

    @property
    def is_active(self):         #属性,判断用户是否已被激活
        return True

    @property
    def is_anonymous(self):     #属性,判断是否是匿名用户
        return False

    def get_id(self):        #方法,返回用户唯一标识
        return str(self.userID)

    #__repr__方法告诉Python如何打印这个类的对象，用来调试
    def __repr__(self):
        return '<GeneralUser %r>' % (self.userName)

class Administrator(db.Model):
    __tablename__ = "administrator"
    userID = db.Column(db.String(36), primary_key=True)  # 主键
    userName = db.Column(db.String(10), index=True)
    registerTime = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Administrator %r>' % (self.userName)

class Article(db.Model):
    __tablename__ = "article"
    author = db.Column(db.String(36), index=True)
    articleID = db.Column(db.String(36), primary_key=True, index=True)
    title = db.Column(db.String(40), index=True)
    context = db.Column(db.TEXT)
    tag = db.Column(db.Enum("event", "entertainment", "science", "life", "trip"))
    status = db.Column(db.Enum("published", "draft"))
    time = db.Column(db.DateTime)
    read = db.Column(db.Integer)

    def __repr__(self):
        return '<Title %r Content %r>' % (self.title, self.context)

class Comment(db.Model):
    __tablename__ = "comment"
    commentID = db.Column(db.String(36), primary_key=True, index=True)
    userID = db.Column(db.String(36), index=True)
    userName = db.Column(db.String(10), index=True)
    articleID = db.Column(db.String(36), index=True)
    title = db.Column(db.String(40), index=True)
    time = db.Column(db.DateTime)
    context = db.Column(db.TEXT)

    def __repr__(self):
        return '<commentID %r>' % (self.commentID)

class Favorite(db.Model):
    __tablename__ = "favorite"
    articleID = db.Column(db.String(36), index=True)
    userID = db.Column(db.String(36), index=True)
    favoriteID = db.Column(db.String(36), primary_key=True, index=True)
    articleURL = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    title = db.Column(db.String(40), index=True)

    def __repr__(self):
        return '<favoriteID %r>' % (self.favoriteID)


class ThumpUp(db.Model):
    __tablename__ = "thumpup"
    thumpupID = db.Column(db.String(36), primary_key=True, index=True)
    time = db.Column(db.DateTime)
    userID = db.Column(db.String(36), index=True)
    articleID = db.Column(db.String(36), index=True)
    title = db.Column(db.String(40), index=True)

    def __repr__(self):
        return '<thunpupID %r>' % (self.thumpupID)


if __name__ == '__main__':
    db.create_all()
    #admin = GeneralUser(userID=1234, userName="admin", email="ass@as.com")
    #db.session.add(admin)
    #db.session.commit()
    all = GeneralUser.query.all()
    print(all)

