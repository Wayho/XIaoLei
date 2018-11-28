# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports
import codecs
import random

from wechatclient import Get_User

########## Base Functions ##################
def Save_To_File(filename,text):
	ffile = codecs.open( filename, 'w', 'utf-8')
	ffile.write(text)
	ffile.close()

def Load_From_File(filename):
	ffile = codecs.open( filename, 'r', 'utf-8')
	text = ffile.read()
	ffile.close()
	return text

###################### Class Define #######################
class Class_UserInfo():
	# 处理 Chat Class的存取，没有属性，仅提供方法

	def Add(self, sOpenid):
		# 返回 objectId
		# 检查存过没有
		#oUser = Get_User('oZtJK1HT5ueWXBeX4wMu1ze2Sm98')
		oUser = Get_User(sOpenid)
		MingYanClass = leancloud.Object.extend( self.__DBClassName )

		dB = MingYanClass()
		dB.set('openid', oUser.get('openid')) #展开sOpenid
		dB.set('nickname', oUser.get('nickname'))
		dB.set('sex', oUser.get('sex'))
		dB.set('language', oUser.get('language'))
		dB.set('city', oUser.get('city'))
		dB.set('province', oUser.get('province'))
		dB.set('country', oUser.get('country'))
		dB.set('headimgurl', oUser.get('headimgurl'))
		dB.set('subscribe_time', oUser.get('subscribe_time'))
		dB.set('remark', oUser.get('remark'))
		dB.set('groupid', oUser.get('groupid'))
		dB.set('tagid_list', oUser.get('tagid_list'))
		dB.set('subscribe_scene', oUser.get('subscribe_scene'))
		dB.set('qr_scene', oUser.get('qr_scene'))
		dB.set('qr_scene_str', oUser.get('qr_scene_str'))

		dB.save()
		return dB.id

	############## private #####
	def __init__(self):
		self.__DBClassName = "UserInfo"


##########################Do not delete############################
USERINFO_CLASS = Class_UserInfo()