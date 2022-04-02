# -*- coding: utf-8 -*-

# import gevent
# from gevent.pywsgi import WSGIServer
# # from gevent import monkey
# # monkey.patch_all()
#
# from flask import Flask
# import time
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     time.sleep(10)
#     return 'Hello World!'
#
#
# @app.route('/index')
# def beijing():
#     return 'Beijing'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#     # http_server = WSGIServer(('127.0.0.1', 5000), app)
#     # http_server.serve_forever()
#

# 阻塞调用，即：调用 http://localhost:5000/index 再开一个浏览器调用 http://localhost:5000 时是阻塞的（会等待15秒)
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()  # 加上这行代码就是非阻塞方式调用（异步调用），否则就是阻塞方式调用
from flask import Flask, render_template

from flask_script import Manager

import time

app = Flask(__name__)
manager = Manager(app=app)


@app.route('/')
def connect():
	return "connected test"

@app.route('/index')
def index_test():
	time.sleep(15)
	return 'index'

@manager.command
def run_gevent():
	server = WSGIServer(("0.0.0.0", 50005), app)
	print("Server started with gevent")
	server.serve_forever()

# if __name__ == "__main__":
# 	server = WSGIServer(("0.0.0.0", 50005), app)
# 	print("Server started")
# 	server.serve_forever()
