# network-community
flask+bootstrap开发的网络社区

## 项目名称

> 网络社区系统

## 成员

> 161610118  朱文滔
>
> 161610120  孙文韬

## 运行环境

> 自带虚拟环境（python 3.6.5）

## 数据库

> 版本：sqlite
>
> 数据库名称：foo
>
> #### 详解
>
> 一共有6个表，分别为用户(Generaluser)、管理员(administrator)、文章(article)、评论(comment)、点赞(thumpup)、收藏(favorite)。采用orm工具flask-sqlachemy进行管理。
>
> ##### 1.generaluser
>
> 共9个字段：
>
> ```python
> userID = db.Column(db.String(36), primary_key=True)   #主键
> userName = db.Column(db.String(10), index=True)       #用户名
> registerTime = db.Column(db.DateTime)                 #注册时间
> email = db.Column(db.String(120))                     #电子邮件
> password = db.Column(db.String(20))                   #密码
> realName = db.Column(db.String(10))                   #真实姓名
> gender = db.Column(db.Enum("男", "女"))                #性别
> birthday = db.Column(db.Date)                         #生日
> describe = db.Column(db.String(100))                  #个人签名
> ```
>
> ##### 2.administrator
>
> 共3个字段：
>
> ```python
> userID = db.Column(db.String(36), primary_key=True)  # 主键
> userName = db.Column(db.String(10), index=True)      #用户名
> registerTime = db.Column(db.DateTime, index=True)    #注册时间
> ```
>
> ##### 3.article
>
> 共8个字段：
>
> ```python
> author = db.Column(db.String(36), index=True) #作者
> articleID = db.Column(db.String(36), primary_key=True, index=True)  #主键
> title = db.Column(db.String(40), index=True)  #标题
> context = db.Column(db.TEXT)                  #内容
> tag = db.Column(db.Enum("event", "entertainment", "science", "life", "trip"))                                      #标签
> status = db.Column(db.Enum("published", "draft")) #状态
> time = db.Column(db.DateTime)                 #上一次修改时间
> read = db.Column(db.Integer)                  #阅读数量
> ```
>
> ##### 4.comment
>
> 共7个字段：
>
> ```python
> commentID = db.Column(db.String(36), primary_key=True, index=True)#主键
> userID = db.Column(db.String(36), index=True)      #用户id
> userName = db.Column(db.String(10), index=True)    #用户名
> articleID = db.Column(db.String(36), index=True)   #文章id
> title = db.Column(db.String(40), index=True)       #文章标题
> time = db.Column(db.DateTime)                      #评论时间
> context = db.Column(db.TEXT)                       #评论内容
> ```
>
> ##### 5.favorite
>
> 共6个字段：
>
> ```python
> articleID = db.Column(db.String(36), index=True)   #文章id
> userID = db.Column(db.String(36), index=True)      #用户id
> favoriteID = db.Column(db.String(36), primary_key=True, index=True)#主键
> articleURL = db.Column(db.String(100))             #文章链接
> time = db.Column(db.DateTime)                      #收藏时间
> title = db.Column(db.String(40), index=True)       #文章标题
> ```
>
> ##### 6.thumpup
>
> 共5个字段：
>
> ```python
> thumpupID = db.Column(db.String(36), primary_key=True, index=True)#主键
> time = db.Column(db.DateTime)                          #点赞时间
> userID = db.Column(db.String(36), index=True)          #用户id
> articleID = db.Column(db.String(36), index=True)       #文章id
> title = db.Column(db.String(40), index=True)           #文章标题
> ```

## 主要技术指标

> 前端使用BootStrap，后端使用Flask

## 主要实现功能

> #### 1.登录
>
> ![1554991894075](./Typora/typora-user-images/1554991894075.png)
>
> #### 2.注册
>
> ![1554991913585](\typora-user-images\1554991913585.png)
>
> 注册时提供了邮箱验证服务
>
> #### 3.个人中心
>
> ##### 创建文章
>
> ![1554992258754](\typora-user-images\1554992258754.png)
>
> 文章编辑采用富文本编辑器summernote
>
> ##### 文章管理
>
> ![1554992295468](\typora-user-images\1554992295468.png)
>
> ##### 收藏管理
>
> ![1554992372743](\typora-user-images\1554992372743.png)
>
> ##### 评论管理
>
> ![1554992494482](\typora-user-images\1554992494482.png)
>
> ##### 点赞管理
>
> ![1554992519379](\typora-user-images\1554992519379.png)
>
> ##### 个人资料
>
> ![1554992542548](\typora-user-images\1554992542548.png)
>
> ##### 密码修改
>
> ![1554992562928](\typora-user-images\1554992562928.png)
>
> #### 4.浏览文章
>
> ##### 首页
>
> ![1554992617538](\typora-user-images\1554992617538.png)
>
> ##### 浏览、评论、收藏、点赞
>
> ![1554992649587](\typora-user-images\1554992649587.png)
>
> #### 5.密码找回
>
> ![1554992736246](\typora-user-images\1554992736246.png)
>
> ![1554992800420](\typora-user-images\1554992800420.png)







