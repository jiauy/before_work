from flask import Flask, request, render_template,url_for,redirect
from flask import Response
import settings
import uuid
# from flask_script import Manager


app = Flask(__name__)
app.config.from_object(settings.Production)
print(app.config)



@app.route('/',endpoint='helloworld')
def hello_world1():
    return 'Hello world'  # 返回的是html的 body
# 等价于
# app.add_url_rule('/',view_func=hello_world)


@app.route('/<key>/<int:num>/<uuid:uuid>/<path:p>')  # 默认str:不用写 /
def params1(key, num, uuid, p):
    return '{}-{}-{}-{}'.format(key, num, uuid, p)


@app.route('/test1')
def test11():
    return "test1"


@app.route('/test1/')  # 推荐，浏览器/没有加会自动重定向到有/的
def test1_1():
    return 'test1/'


@app.route('/request')
def rq1():
    print(request.headers)
    return request.headers['Cookie']


@app.route('/response/')
def rs1():
    return Response('<h1>response<h1/>', status=404)


@app.route('/template/')  # 创建一个templates文件夹
def template1():
    tp = render_template('js2.html',name="小明")  #传入模板参数，可以是自定义类，有实例属性，可被调用
    return tp


@app.route('/getargs/')  # get传参用args.get获取
def get_args1():
    username = request.args.get('username')
    return username


@app.route('/getpostargs/',methods=['GET','POST'],endpoint='getpostargs')  # post传参用form.get获取
def get_postargs1():
    username = request.form.get('username')
    return username


@app.route('/redirect/')  # post传参用form.get获取
def redirect1():
    return redirect(url_for('helloworld'))    #注意不能定义出来一个redirect自定义函数啊

if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=8888)
    uid = uuid.uuid4()
    print(uuid)
    app.run(port=8808)
