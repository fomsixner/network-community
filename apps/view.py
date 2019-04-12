from apps import app, db, mail, login_manager
from flask import render_template, flash, redirect, session, url_for, g, request, get_flashed_messages
from .form import RegistForm
import datetime
from .model import GeneralUser, Article, Comment, Favorite, ThumpUp
import uuid
from functools import wraps
import json
import re
from flask_mail import Message
import random
from flask_login import login_user, logout_user, current_user, login_required

#登录装饰器检查用户是否登录
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=["POST", "GET"])
@app.route('/<int:page>', methods=["POST", "GET"])
@user_login_req
def index(page=1):
    articles = Article.query.filter_by(status="published").order_by(Article.time.desc()).paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@login_manager.user_loader
def load_user(userID):
    #获取user对象,存储到session中
    return GeneralUser.query.get(userID)


@app.route('/event', methods=["POST", "GET"])
@app.route('/event/<int:page>', methods=["POST", "GET"])
@user_login_req
def event(page=1):     #时事
    articles = Article.query.filter_by(status="published", tag="event").paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@app.route('/entertainment', methods=["POST", "GET"])
@app.route('/entertainment/<int:page>', methods=["POST", "GET"])
@user_login_req
def entertainment(page=1):        #娱乐
    articles = Article.query.filter_by(status="published", tag="entertainment").paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@app.route('/science', methods=["POST", "GET"])
@app.route('/science/<int:page>', methods=["POST", "GET"])
@user_login_req
def science(page=1):        #科学
    articles = Article.query.filter_by(status="published", tag="science").paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@app.route('/life', methods=["POST", "GET"])
@app.route('/life/<int:page>', methods=["POST", "GET"])
@user_login_req
def life(page=1):        #生活
    articles = Article.query.filter_by(status="published", tag="life").paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@app.route('/trip', methods=["POST", "GET"])
@app.route('/trip/<int:page>', methods=["POST", "GET"])
@user_login_req
def trip(page=1):        #旅游
    articles = Article.query.filter_by(status="published", tag="trip").paginate(page, per_page=10)
    return render_template('index.html', articles=articles.items, pagination=articles)


@app.route('/login', methods=['POST', 'GET'])
def login(page=1):
    articles = Article.query.filter_by(status="published").paginate(page, per_page=10)
    if request.method == "POST":
        username = request.form.get("inputAccount")
        password = request.form.get("inputPassword")
        user_x = GeneralUser.query.filter_by(userName=username).first()
        if user_x is None:
            flash("该用户不存在", category="error")
            return render_template("login.html")
        else:
            if password != user_x.password:
                flash("密码错误", category="error")
                return render_template("login.html")
            else:
                flash("登录成功", category="ok")
                session["username"] = username
                session["userid"] = user_x.userID
                login_user(user_x)
                print(current_user.userName)
                return render_template("index.html", articles=articles.items, pagination=articles)
    return render_template('login.html')


@app.route("/forget_pwd", methods=["POST", "GET"])
def forget_pwd():
    if request.method == "POST":
        verify_code = request.form.get("verify_code")
        username = request.form.get("user_name")
        if username == "":
            flash("请输入用户名", category="user_error")
            return render_template("forget_pwd.html")
        if verify_code == "":
            flash("请输入验证码", category="verify_error")
            return render_template("forget_pwd.html")
        if "verify_code" in session:
            if session["verify_code"] == verify_code:
                session.pop("verify_code")
                session["username"] = username
                return redirect(url_for("forget_pwd2"))
            else:
                flash("验证码错误", category="verify_error")
                return render_template("forget_pwd.html")
        else:
            flash("请获取验证码", category="verify_error")
            return render_template("forget_pwd.html")
    return render_template("forget_pwd.html")


@app.route("/forget_pwd2", methods=["POST", "GET"])
def forget_pwd2():
    if request.method == "POST":
        new_pwd = request.form.get("new_password")
        rep_pwd = request.form.get("rep_password")
        if new_pwd != rep_pwd:
            flash(message="重复密码错误", category="rep_error")
            return render_template("forget_pwd2.html")
        if "username" in session:
            user = GeneralUser.query.filter_by(userName=session.get("username")).first()
            user.password = new_pwd
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("forget_pwd2.html")


@app.route("/get_verification_code2", methods=["POST"])
def get_verification_code2():
    data = json.loads(request.form.get("data"))
    user = GeneralUser.query.filter_by(userName=data["username"]).first()
    email_addr = user.email
    print(email_addr)
    if email_addr:
        chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verify_code = ''.join(x)
        session["verify_code"] = verify_code
        print(session["verify_code"])
        #发送验证码
        msg = Message("验证码", sender="net_community@126.com", recipients=[email_addr])
        msg.body = "验证码为: " + verify_code
        mail.send(msg)
        return "200"       #验证码发送成功
    else:
        return "100"             #用户名不存在


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        user = GeneralUser()
        user.userName = request.form.get("user_name")
        user.userID = ''.join([each for each in str(uuid.uuid1()).split('-')])
        user.registerTime = datetime.datetime.now()
        user.email = request.form.get("user_email")
        user.password = request.form.get("user_password")
        if user.password != request.form.get("verify_password"):
            flash("前后密码不一致", category="error")
            return render_template('regist.html', form=form)
        user_x = GeneralUser.query.filter_by(userName=user.userName).first()
        if user_x is not None:
            flash("该用户已经存在", category="error")
            return render_template('regist.html', form=form)
        if session["verify_code"] != request.form.get("verification_code"):
            flash("验证码错误", category="error")
            return render_template('regist.html', form=form)
        session.pop("verify_code", None)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    return render_template('regist.html', form=form)


@app.route("/get_verification_code", methods=["POST"])
def get_verification_code():
    data = json.loads(request.form.get("data"))
    c = re.compile(r"^\w+@(\w+\.)+(com|cn|net)$")
    email_addr = c.search(data["email_addr"]).string
    if email_addr:
        chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verify_code = ''.join(x)
        session["verify_code"] = verify_code
        #发送验证码
        msg = Message("验证码", sender="net_community@126.com", recipients=[email_addr])
        msg.body = "验证码为: " + verify_code
        mail.send(msg)
        return "200"       #验证码发送成功
    else:
        return "100"             #邮箱未填写或格式错误


@app.route('/logout')
@user_login_req
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    logout_user()
    return redirect(url_for("index"))


@app.route('/user_center')
@user_login_req
def user_center():
    return render_template("user_center.html")

#@app.route('/user_center/article_manage')
#@user_login_req
#def article_manage():
#    return render_template('article_manage.html')

@app.route('/user_center/my_favorite')
@app.route('/user_center/my_favorite/<int:page>')
@user_login_req
def my_favorite(page=1):
    favorites = Favorite.query.filter_by(userID=session.get("userid")).order_by(Favorite.time.desc()).paginate(page, per_page=10)
    return render_template('my_favorite.html', favorites=favorites.items, pagination=favorites)


@app.route('/user_center/my_comment')
@app.route('/user_center/my_comment/<int:page>')
@user_login_req
def my_comment(page=1):
    comments = Comment.query.filter_by(userID=session.get("userid")).order_by(Comment.time.desc()).paginate(page, per_page=10)
    return render_template('my_comment.html', comments=comments.items, pagination=comments)


@app.route('/user_center/my_thumpup')
@app.route('/user_center/my_thumpup/<int:page>')
@user_login_req
def my_thumpup(page=1):
    thumpups = ThumpUp.query.filter_by(userID=session.get("userid")).order_by(ThumpUp.time.desc()).paginate(page, per_page=10)
    return render_template('my_thumpup.html', thumpups=thumpups.items, pagination=thumpups)


@app.route('/user_center/visitors_cal')
@user_login_req
def visitors_cal():
    return render_template('visitors_cal.html')


@app.route('/user_center/userinfo', methods=['POST', 'GET'])
@user_login_req
def user_info():
    """
    此处要添加表单验证
    :return:
    """
    user = GeneralUser.query.filter_by(userName=session.get("username")).first()
    if request.method == "POST":
        user.realName = request.form.get("real_name", None)
        if request.form.get("gender", None) == "male":
            user.gender = "男"
        elif request.form.get("gender", None) == "female":
            user.gender = "女"
        else:
            pass
        user.birthday = request.form.get("birthday", None)
        user.describe = request.form.get("describe", None)
        db.session.commit()
        #flash(message="修改成功", category="ok")
        return render_template("user_center.html")
    return render_template("user_info.html", user=user)


@app.route('/user_center/resetpassword', methods=['POST', 'GET'])
@user_login_req
def resetpassword():
    if request.method == "POST":
        old_pwd = request.form.get("old_password")
        user = GeneralUser.query.filter_by(userName=session.get("username")).first()
        if old_pwd != user.password:
            flash(message="旧密码错误", category="error")
            return render_template("resetpassword.html")
        new_pwd = request.form.get("new_password")
        rep_pwd = request.form.get("rep_password")
        if new_pwd != rep_pwd:
            flash(message="重复密码错误", category="rep_error")
            return render_template("resetpassword.html")
        user.password = new_pwd
        db.session.commit()
        session.pop("username", None)
        flash(message="修改密码成功，请重新登录", category="ok")
        return redirect(url_for("login", account=user.userName))
    return render_template("resetpassword.html")


@app.route('/user_center/article_manage')
@app.route("/user_center/article_manage/published", methods=["POST", "GET"])
@app.route("/user_center/article_manage/published/<int:page>", methods=["POST", "GET"])
@user_login_req
def published(page=1):
    articles = Article.query.filter_by(author=session.get("username"), status="published").order_by(Article.time.desc()).paginate(page, per_page=5)
    return render_template("article_manage.html", articles=articles.items, pagination=articles)


@app.route("/user_center/article_manage/draft", methods=["POST", "GET"])
@app.route("/user_center/article_manage/draft/<int:page>", methods=["POST", "GET"])
@user_login_req
def draft(page=1):
    articles = Article.query.filter_by(author=session.get("username"), status="draft").order_by(Article.time.desc()).paginate(page, per_page=5)
    return render_template("draft.html", articles=articles.items, pagination=articles)


@app.route("/user_center/article_manage/newarticle", methods=["POST", "GET"])
@user_login_req
def newarticle():
    return render_template("new_article.html")


@app.route("/article_save", methods=["POST"])
@user_login_req
def article_save():
    article = Article()
    data = json.loads(request.form.get("data"))
    if data["title"] == "":
        return "100"    #未输入标题
    article.title = data["title"]
    article.status = "draft"         #未发表
    if "tag" not in data:
        return "200"    #未选择标签
    article.tag = data["tag"]
    if data["content"] == "":
        return "300"    #未输入内容
    article.context = data["content"]
    article.articleID = ''.join([each for each in str(uuid.uuid1()).split('-')])
    article.author = session.get("username")
    db.session.add(article)
    db.session.commit()
    return "400"         #成功


@app.route("/article_submit", methods=["POST"])
@user_login_req
def article_submit():
    data = json.loads(request.form.get("data"))
    if data["title"] == "":
        return "100"  # 未输入标题
    if "tag" not in data:
        return "200"  # 未选择标签
    if data["content"] == "":
        return "300"  # 未输入内容
    article = Article()
    article.title = data["title"]
    article.status = "published"  #发表
    article.tag = data["tag"]
    article.context = data["content"]
    article.articleID = ''.join([each for each in str(uuid.uuid1()).split('-')])
    article.author = session.get("username")
    article.time = datetime.datetime.now()
    article.read = 0
    db.session.add(article)
    db.session.commit()
    return "400"  # 成功


@app.route("/article/<string:id>", methods=["POST", "GET"])
def article_broswer(id):
    article = Article.query.filter_by(articleID=id).first()
    if article.read is None:
        article.read = 0
    article.read = article.read + 1              #阅读数+1
    db.session.commit()
    comments = Comment.query.filter_by(articleID=id).order_by(Comment.time.desc())     #降序排列
    is_thump_up = "0"    #未点赞
    is_favorite = "0"    #未收藏
    if "username" in session:
        is_thump_up = "1"
        is_favorite = "1"
        temp1 = ThumpUp.query.filter_by(articleID=id, userID=session.get("userid")).first()
        temp2 = Favorite.query.filter_by(articleID=id, userID=session.get("userid")).first()
        if temp1 is None:
            is_thump_up = "0"
        if temp2 is None:
            is_favorite = "0"
    return render_template("article_broswer.html", article=article, comments=comments, is_thump_up=is_thump_up, is_favorite=is_favorite)


@app.route("/comment_submit", methods=["POST"])
@user_login_req
def comment_submit():
    comment = Comment()
    data = json.loads(request.form.get("data"))
    if data["context"] == "":
        return "100"    #未输入评论
    user = GeneralUser.query.filter_by(userName=session.get("username")).first()
    comment.userID = user.userID
    comment.userName = user.userName
    comment.context = data["context"]
    comment.time = datetime.datetime.now()
    comment.commentID = ''.join([each for each in str(uuid.uuid1()).split('-')])
    comment.articleID = data["articleid"]
    comment.title = data["title"]
    db.session.add(comment)
    db.session.commit()
    return "200"   #评论提交成功


@app.route("/new_favorite", methods=["POST"])
@user_login_req
def new_favorite():
    data = json.loads(request.form.get("data"))
    if data["status"] == 0:        #收藏
        favorite = Favorite()
        favorite.articleID = data["articleid"]
        favorite.time = datetime.datetime.now()
        favorite.userID = GeneralUser.query.filter_by(userName=session.get("username")).first().userID
        favorite.articleURL = r"http://127.0.0.1:5000/article/" + data["articleid"]
        favorite.favoriteID = ''.join([each for each in str(uuid.uuid1()).split('-')])
        favorite.title = data["title"]
        db.session.add(favorite)
        db.session.commit()
        return "100"
    else:               #取消收藏
        favorite = Favorite.query.filter_by(articleID=data["articleid"], userID=session.get("userid")).first()
        db.session.delete(favorite)
        db.session.commit()
        return "200"


@app.route("/new_thump_up", methods=["POST"])
@user_login_req
def new_thump_up():
    data = json.loads(request.form.get("data"))
    if data["status"] == 0:         #还未点赞
        thump_up = ThumpUp()
        thump_up.userID = GeneralUser.query.filter_by(userName=session.get("username")).first().userID
        thump_up.thumpupID = ''.join([each for each in str(uuid.uuid1()).split('-')])
        thump_up.articleID = data["articleid"]
        thump_up.title = data["title"]
        thump_up.time = datetime.datetime.now()
        db.session.add(thump_up)
        db.session.commit()
        return "100"             #点赞
    else:
        thump_up = ThumpUp.query.filter_by(articleID=data["articleid"], userID=session.get("userid")).first()
        db.session.delete(thump_up)
        db.session.commit()
        return "200"            #取消点赞


@app.route("/user_center/article_manage/draft_edit", methods=["POST", "GET"])
@app.route("/user_center/article_manage/draft_edit/<string:id>", methods=["POST", "GET"])
def draft_edit(id):
    draft = Article.query.filter_by(articleID=id, status="draft").first()
    return render_template("draft_edit.html", draft=draft)


@app.route("/draft_submit", methods=["POST"])
@user_login_req                     #草稿提交
def draft_submit():
    data = json.loads(request.form.get("data"))
    if data["title"] == "":
        return "100"  # 未输入标题
    if "tag" not in data:
        return "200"  # 未选择标签
    if data["content"] == "":
        return "300"  # 未输入内容
    article = Article.query.filter_by(articleID=data["id"]).first()
    article.title = data["title"]
    article.status = "published"  #发表
    article.tag = data["tag"]
    article.context = data["content"]
    article.time = datetime.datetime.now()
    db.session.commit()
    return "400"          #提交成功


@app.route("/draft_save", methods=["POST"])
@user_login_req                #草稿保存
def draft_save():
    data = json.loads(request.form.get("data"))
    article = Article.query.filter_by(articleID=data["id"]).first()
    article.title = data["title"]
    article.status = "draft"  # 发表
    article.tag = data["tag"]
    article.context = data["content"]
    article.time = datetime.datetime.now()
    db.session.commit()
    return "400"              #保存成功