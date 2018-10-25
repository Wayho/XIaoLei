# coding: utf-8
from leancloud import cloudfunc				#requirements leancloud-sdk>=1.0.9,<=2.0.0
from datetime import datetime

from flask import Flask,request
from flask import render_template
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)




@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get")
def get_bot_response():
    sUserText = request.args.get('msg')
    #sRet = english_bot.get_response(userText)
    sRet = cloudfunc.run( 'chat',sString=sUserText ) #必须待程序上传到云端才能使用
    #print(userText,sRet)
    return str(sRet)


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
