# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports
import codecs
import random

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
class Class_MingJu():
	# 处理 Chat Class的存取，没有属性，仅提供方法

	def Get(self):
		# return str
		MingJuClass = leancloud.Object.extend( self.__DBClassName )
		query = MingJuClass.query
		aFind = query.find()
		for find in aFind:
			print(find.get('Content').replace('\r','\n'))
			print('***********')



	def Add(self, sContent, sFrom, iLike, sAuther, sCountry):
		# 返回 objectId
		# 检查存过没有
		MingJuClass = leancloud.Object.extend( self.__DBClassName )

		dB = MingJuClass()
		dB.set('Content', sContent)
		dB.set('From', sFrom)
		dB.set('Like', iLike)
		dB.set('Auther', sAuther)
		dB.set('Country', sCountry)
		dB.save()
		return dB.id

	############## private #####
	def __init__(self):
		self.__DBClassName = "MingJu"


##########################Do not delete############################
MINGJU_CLASS = Class_MingJu()