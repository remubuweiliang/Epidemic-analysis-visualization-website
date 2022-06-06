import json

from flask import Flask, render_template, \
    request, redirect, session, url_for, \
    jsonify, flash, get_flashed_messages
from flask_cors import CORS  # 导入包
# 自定义API导入
from API.AIchat import get_answer
from API.mapData import get_map_data, get_time_data
from API.realTimeInfo import get_real_time_info, get_detail
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket

user_socket_dict = {}  # 创建一个空字典用来存储用户
data = []  # 用于存储聊天数据
user_data = [{'user': '123', 'password': '123123', 'mail': '1231231@qq.com', 'city': ['湖北', '武汉'], 'gender': 'male',
              'hobby': ['Sleep'], 'date': '2021-06-18T16:00:00.000Z', 'desc': '123123123123123333333333333333333333',
              'data': []}]  # 用于存储用户的账号信息

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.debug = True  # 开启调试模式
app.secret_key = "20202005185ZhanRunYuan"  # 设置密钥
# app.register_blueprint(user.us)#蓝图的使用
CORS(app, supports_credentials=True)  # 设置参数


# 无session重定向
# @app.before_request
# def before(*arg, **kwarg):
#     if request.path == '/login' or request.path == '/register':
#         return None
#     else:
#         name = session.get('user_info')
#         if not name:
#             # print('非法访问！！！')
#             return redirect('/login')  # 未登录弹回
#         else:
#             return None


# 登录页面
@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        res = request.get_json(silent=True)
        user = res['data']['user']
        pwd = res['data']['password']
        right = False
        # 账号密码判定
        for item in user_data:
            if user == item['user'] and pwd == item['password']:
                right = True
        if right:
            session['user_info'] = user
            print(user + "登录成功！")
            return 'window.location.href="/index"'
        else:
            return 'alert("Error!");window.location.href="/login"'


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        res = request.get_json(silent=True)
        user_data.append(res['data'])  # 存进用户数组
        user = res['data']['user']
        print(user_data)
        print(user + "注册成功！")
        return 'window.location.href="/login"'


# 获取该用户详细数据信息
@app.route('/get_userdata', methods=['GET', 'POST'])
def get_userdata():
    name = session.get('user_info')
    x = {}
    for item in user_data:
        if name == item['user']:
            x['user'] = item['user']
            x['gender'] = item['gender']
            x['mail'] = item['mail']
            x['city'] = item['city']
            x['date'] = item['date'].split('T')[0]
            x['hobby'] = item['hobby']
            x['desc'] = item['desc']
            break
    x = jsonify(x)
    return x


# 主页
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'], endpoint='index')
def index():
    user = session.get('user_info')
    res = get_flashed_messages()
    if not user:
        return redirect(url_for('login'))
    return render_template('index.html')


# 主页
@app.route('/home')
def home():
    return render_template('home.html')


# 资讯搜索页面
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


# 实事资讯数据地址
@app.route('/real_time_info', methods=['GET', 'POST'])
def real_time_info():
    res = request.get_json(silent=True)
    return jsonify(get_real_time_info(res['txt']))


# 实事资讯具体页面
@app.route('/detail')
def detail():
    return render_template('detail.html')


# 实事资讯具体数据地址
@app.route('/real_time_info/<string:url>', methods=['GET', 'POST'])
def real_time_info_get_detail(url):
    return jsonify(get_detail(url))


# 地图图表
@app.route('/map')
def map():
    return render_template('map.html')


# 表单图表
@app.route('/form')
def form():
    return render_template('form.html')


# 地图数据页面
@app.route('/map_data', methods=['GET', 'POST'])
def map_data():
    return get_map_data()


# 全国疫情信息获取
@app.route('/time_data', methods=['GET', 'POST'])
def time_data():
    return get_time_data()


# AI聊天页面
@app.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    return render_template('ai_chat.html')


# AI聊天返回数据地址
@app.route('/chat_info', methods=['GET', 'POST'])
def chat_info(*arg, **kwarg):
    res = request.get_json(silent=True)
    return get_answer(res['txt'])


# 获取用户名校验地址
@app.route('/get_name', methods=['GET', 'POST'])
def get_name():
    name = session.get('user_info')
    return str(name)


# 聊天室主进程地址
@app.route('/websocket/<user_nick>')  # 设置Flask路由,前端通过访问这个地址拆解信息,<user_nick>即前端登录聊天室输入的内容
def ws_app(user_nick):
    print('进入聊天室路径！')
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket is None:
        print('您使用的是Http协议')
        return '您使用的是Http协议'
    try:
        print('聊天室登录成功！')
        # 取出environ中的wsgi.websocket对应的值
        user_socket_dict[user_nick] = user_socket  # 以<user_nick>为key在字典中插入用户信息
        for item in data:
            user_socket.send(item)
        print(user_socket_dict)
        while True:
            msg = user_socket.receive()  # 取出发送内容
            data.append(msg)
            for user in list(user_socket_dict.values()):
                user.send(msg)
        user_socket.close()
    except:
        del user_socket_dict[user_nick]
        print(user_socket_dict)
        print("One connection closed")


# 聊天室页面
@app.route('/chatroom')
def chatroom():
    return render_template('chatroom.html')


# 设置页面
@app.route('/setting')
def setting():
    return render_template('setting.html')


# 帮助页面
@app.route('/help')
def help():
    return render_template('help.html')


# 评价页面
@app.route('/comment')
def comment():
    return render_template('comment.html')


# 测试页面
@app.route('/temp')
def temp():
    return render_template('temp.html')


# 错误状态码返回
@app.errorhandler(404)
def error_404(arg):
    return render_template('404.html', arg=arg)


# 错误状态码返回
@app.errorhandler(500)
def error_400(arg):
    return render_template('500.html', arg=arg)


if __name__ == '__main__':
    http_serve = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()

# pipreqs ./ --encoding=utf-8   #导出引用包
# pip3 freeze > requirements.txt
