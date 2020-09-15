pip install flask-script  让flask可以多一些命令,有自带的，也可以自定义
pip install pymysql
pip install flask-sqlalchemy   ORM映射
pip install flask-migrate  #操作ORM
数据库配置settings

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@ip：port/数据库名字'

- url_for用法
url_for中可以是视图函数的名字，也可以是endpoint指定的名字，在蓝图中的url_for需要带上"蓝图的名字.函数名/endpoint名"


- 项目结构
    - 项目
        - manager.py    运行,关联数据库和app
        - config.py     配置
        - app           app总体内容
            - \_\_init\_\_.py       创建app,配置设置,为app绑定功能，如创建ORM,邮件系统等
            - 视图函数包             蓝图包,使用绑定的功能
            - static
            - templates
            - models.py             使用db,创建model

项目结构构造好之后的命令流程:
- 在manager.py中导入定义的模型class，不然不能关联。
- python manager.py db init       根据models.py中的class建立model模型文件，相当于django中的makemigrations,也会生成migrations文件，记录models的变化和版本，用来降级等操作。 操作一次即可/未必见得，每动一次模型应该也应该init一次
- python manager.py db migrate    将model模型变成数据库的表，model的任何修改都要做。
- python manager.py db upgrade    修改模型后，需要migrate生成迁移文件然后upgrade
- python manager.py db downgrade  版本回滚