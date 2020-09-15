#Flask(__name__)负责配置文件的设置,如模板文件夹，静态文件夹，且能关联蓝图的视图，以及网站的启动
from flask import Flask
import settings
from apps.user.view import user_bp
def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    app.config.from_object(settings.Config)
    app.register_blueprint(user_bp)
    return app