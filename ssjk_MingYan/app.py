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

import os

from flask import Flask, request, abort, render_template

from classmingyan import MINGYAN_CLASS
from classuserinfo import USERINFO_CLASS

from wechatclient import send_random_message,send_message

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)


import xmltodict
from wechatpy.utils import to_text

# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', '123456')
AES_KEY = os.getenv('WECHAT_AES_KEY', '')
APPID = os.getenv('WECHAT_APPID', '')
WECHAT_APPSECRET = os.getenv('WECHAT_APPSECRET', '')


###############################################

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
	return '您好,欢迎光临!\r\n每天早中晚分别送您三句名人名言。'

@app.route('/heart')
def heart():
	return 'Heart'


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
		#msg = parse_message(request.data)
		message = xmltodict.parse(to_text(request.data))['xml']
		sOpenid = message['FromUserName']
		sMsgType = message['MsgType']
		print(">>", message)
		if('text' == sMsgType):
			if('0'== message['Content']):
				send_message(sOpenid, '您好,谢谢回复!\r\n您将在每天早中晚分别收到三句名人名言,如需即时收取名人名言,只需向我回复任意消息即可。')
			send_random_message(sOpenid)
		if ('image' == sMsgType or 'voice' == sMsgType):
			#send_message(sOpenid, '您好,谢谢回复!\r\n您将在每天早中晚分别收到三句名人名言,如需即时收取名人名言,只需向我回复任意消息即可。')
			send_random_message(sOpenid)
		elif('event' == sMsgType ):
			if( 'subscribe'== message['Event']):
				send_message(sOpenid, '您好,欢迎关注!\r\n每天早中晚分别自动送您三句名人名言,请回复0以便发送给您(不回复不发送)。')
				send_random_message(sOpenid)
				send_random_message(sOpenid)
				USERINFO_CLASS.Add(sOpenid)
			elif ('unsubscribe' == message['Event']):
				print(sOpenid,' ***** unsubscribe')
		return ''
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
			reply = create_reply('您好,欢迎光临!', msg)
			return crypto.encrypt_message(reply.render(), nonce, timestamp)


@app.route('/time')
def time():
	return str(datetime.now())

@app.route('/msg')
def msg():
	from wechatpy import WeChatClient
	oWeChatClient = WeChatClient(APPID, WECHAT_APPSECRET)
	oWeChatClient.message.send_text('oZtJK1HT5ueWXBeX4wMu1ze2Sm98', str(datetime.now()))
	return str(datetime.now())

@sockets.route('/echo')
def echo_socket(ws):
	while True:
		message = ws.receive()
		ws.send(message)
