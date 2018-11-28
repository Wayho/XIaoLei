# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports
import codecs
import random


###################### Class Define #######################
class Class_Writer():
	# 处理 Chat Class的存取，没有属性，仅提供方法

	def Add(self, sCountry, sName, sUrl):
		# 返回 objectId
		# 检查存过没有

		WriterClass = leancloud.Object.extend( self.__DBClassName )
		dB = WriterClass()
		dB.set('country', sCountry)
		dB.set('name', sName)
		dB.set('url', sUrl)
		dB.save()
		return dB.id

	def Update_active(self, objectId, active):
		# 保存到 ReadDaily_Class
		# 返回 objectId
		WriterClass = leancloud.Object.extend( self.__DBClassName )
		if(objectId is None):
			dB = WriterClass()
		else:
			dB = WriterClass.create_without_data( objectId )

		dB.set( 'active', active )  # update
		dB.save( )
		if (objectId is None):
			objectId = dB.id
		return objectId

	def Update_page(self, objectId, page):
		# 保存到 ReadDaily_Class
		# 返回 objectId
		WriterClass = leancloud.Object.extend( self.__DBClassName )
		if(objectId is None):
			dB = WriterClass()
		else:
			dB = WriterClass.create_without_data( objectId )

		dB.set( 'page', page )  # update
		dB.save( )
		if (objectId is None):
			objectId = dB.id
		return objectId

	def Get_Writer_One(self):
		# 返回 objectId
		# 检查存过没有
		WriterClass = leancloud.Object.extend( self.__DBClassName )
		query = WriterClass.query
		query.limit(1)
		query.add_ascending('createdAt')      #descending()
		#query.select('country', 'name', 'url', 'active')
		query.equal_to('active',False)
		#query.does_not_exist('page')
		aFind = query.find()
		print(len(aFind))
		if (len(aFind) == 0):
			return None
		else:
			return {'objectId':aFind[0].get('objectId'),'country':aFind[0].get('country'), 'name':aFind[0].get('name'), 'url':aFind[0].get('url'), 'active':aFind[0].get('active'),'page':aFind[0].get('page')}

	############## private #####
	def __init__(self):
		self.__DBClassName = "Writer"


##########################Do not delete############################
WRITER_CLASS = Class_Writer()