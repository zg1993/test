# flask-web


参考教程：Flask Web Development: Developing Web Applications with Python


本地测试：

1.git clone git@github.com:zg1993/test.git 下载代码

2.virtualenv flask_env 虚拟环境的创建（安装virtualenv：pip install virtualenv）

3.source flask_env/Scripts/activate 进入虚拟环境（退出虚拟环境deactivate）

4.pip install -r requirements/common.txt 安装相应模块

5.python manage.py shell:

	db.create_all() 创建表

	Role.insert_roles() 在数据库中创建角色

	User.generate_fake() 生成虚拟用户

	Post.generate_fake() 生成虚拟文章

	Comment.generate_fake() 生成虚拟评论

	User.add_self_follows() 用户设为自己的关注者



5.python manage.py runserver启动

6.pip install -r requirements/dev.txt 安装测试相应模块

7.python manage.py test 单元测试



Heroku平台上云部署：

1.heroku login

2.heroku create <appname> 创建程序 

3.heroku addons:add heroku-postgresql:dev 配置数据库 


4.heroku config:set FLASK_CONFIG=heroku

5.heroku config:set MAIL_USERNAME=<your-gmail-username> 
  heroku config:set MAIL_PASSWORD=<your-gmail-password>

6.将代码提交到github上

7.git push heroku master 将程序上传到 Heroku 服务器

8.heroku run python manage.py deploy 执行deploy命令

9.heroku restart 重启程序

访问：https://limitless-taiga-82662.herokuapp.com 