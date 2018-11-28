# coding: utf-8
import os
import time
from wechatpy import WeChatClient

from classmingyan import MINGYAN_CLASS

# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', '123456')
AES_KEY = os.getenv('WECHAT_AES_KEY', '')
APPID = os.getenv('WECHAT_APPID', '')
WECHAT_APPSECRET = os.getenv('WECHAT_APPSECRET', '')

oWeChatClient = WeChatClient(APPID, WECHAT_APPSECRET)




def send_message(sOpenid,sMessage):
	#sOpenid = 'oZtJK1HT5ueWXBeX4wMu1ze2Sm98'
	oWeChatClient.message.send_text(sOpenid, sMessage)
	return sMessage

def send_random_message(sOpenid):
	#sOpenid = 'oZtJK1HT5ueWXBeX4wMu1ze2Sm98'
	sMingyan = MINGYAN_CLASS.Random()
	if (sMingyan):
		oWeChatClient.message.send_text(sOpenid, sMingyan)
	return sMingyan

def send_random_message_to_all():
	sMingyan = MINGYAN_CLASS.Random()
	print ('>>', sMingyan)
	if (sMingyan):
		sOpenid_List = Openid_List()
		print(sOpenid_List)
		for openid in sOpenid_List:
			try:
				oWeChatClient.message.send_text(openid, sMingyan)
				print ('>>',openid)
			except Exception:
				print ('??',openid)
				#time.sleep(10)
	return sMingyan


def follower():
	openids = oWeChatClient.user.get_followers().get('data').get('openid')
	followers = oWeChatClient.user.get_batch(openids)
	for tmp in followers:
		print(tmp)
	return str(followers)

def Openid_List():
	#openid List,str
	return oWeChatClient.user.get_followers().get('data').get('openid')

def Get_User(sOpenid):
	#sOpenid = 'oZtJK1HT5ueWXBeX4wMu1ze2Sm98'
	return oWeChatClient.user.get(sOpenid)

