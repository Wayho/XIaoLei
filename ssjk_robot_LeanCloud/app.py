# coding: utf-8
#使用chatterbot的回复机器人,数据来源于XiaoLei_Corpus
#在微信号向公众号端发送消息后,直接转发到LeanCloud端(通过公众号后台配置),
#即:使用LeanCloud云引擎作为微信公众号的回调服务器,Lean马上回复空串,避免耗时
#在Lean获得回复字串后,直接通过WeChatClient.message.send_text()发送迟到的消息
from datetime import datetime
import time

from flask import Flask
from flask import render_template
from flask_sockets import Sockets

from views.todos import todos_view

import os
import _thread

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

import xmltodict
from wechatpy.utils import to_text

from wechatpy import WeChatClient
# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', '123456')
AES_KEY = os.getenv('WECHAT_AES_KEY', '')
APPID = os.getenv('WECHAT_APPID', '')
WECHAT_APPSECRET = os.getenv('WECHAT_APPSECRET', '')

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot
print(chatterbot.__version__)

oChatBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
#oChatBot.set_trainer(ChatterBotCorpusTrainer)
#oChatBot.train("chatterbot.corpus.chinese.GBT50297")

oWeChatClient = WeChatClient(APPID, WECHAT_APPSECRET)

###############################################

app = Flask(__name__)
sockets = Sockets(app)

sReturnMessage = '您好,欢迎光临!'

#使用机器人回复,有个比较耗时的检索任务在这里运行
def message_robot(sFromUserName, sContent):
	#time.sleep(5)
	sMessage = str(oChatBot.get_response(sContent))
	print("<<", sMessage)
	oWeChatClient.message.send_text(sFromUserName, sMessage)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
	signature = request.args.get('signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	encrypt_type = request.args.get('encrypt_type', 'raw')
	msg_signature = request.args.get('msg_signature', '')
	try:
		check_signature(TOKEN, signature, timestamp, nonce)
	except InvalidSignatureException:
		abort(403)
	if request.method == 'GET':
		echo_str = request.args.get('echostr', '')
		return echo_str


	# POST request
	if encrypt_type == 'raw':
		# plaintext mode
		msg = parse_message(request.data)
		print(">>", str(msg))
		if msg.type == 'text':
			reply = create_reply('', msg)
			message = xmltodict.parse(to_text(request.data))['xml']
			#MESSAGEROBOT.Reset(message['FromUserName'], msg.content)
			_thread.start_new_thread(message_robot, (message['FromUserName'], msg.content,))
		else:
			reply = create_reply('抱歉,仅支持文本', msg)
		#print(type(reply.render()))
		return reply.render()
	else:
		# encryption mode
		from wechatpy.crypto import WeChatCrypto

		crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
		try:
			msg = crypto.decrypt_message(
				request.data,
				msg_signature,
				timestamp,
				nonce
			)
		except (InvalidSignatureException, InvalidAppIdException):
			abort(403)
		else:
			msg = parse_message(msg)
			if msg.type == 'text':
				reply = create_reply(msg.content, msg)
			else:
				reply = create_reply('抱歉,仅支持文本', msg)
			return crypto.encrypt_message(reply.render(), nonce, timestamp)




@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
