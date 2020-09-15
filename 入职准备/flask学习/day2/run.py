from apps import create_app
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app=create_app()

migrate = Migrate(app=app,db=db)

manager = Manager(app)

@manager.command
def init():
    print('初始化测试')
#定义形式等价于
manager.add_command('自定义名称',MigrateCommand)
    
    
# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    manager.run()