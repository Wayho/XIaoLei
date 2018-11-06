# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports

from datetime import datetime, timedelta
import time
import os
# local imports


DATE_LIST_NUM = 180
LIMIT_QUERY = 500

###################### Class Define #######################
class Class_Baike():
	# 处理 Baike Class的存取，没有属性，仅提供方法

	def Find_Not_Expand(self):
		# 返回 Title
		# 检查Expand没有
		BaikeClass = leancloud.Object.extend(self.__DBClassName)
		query = BaikeClass.query
		#query.add_ascending('updatedAt')    ## 按时间，升序排列
		query.add_ascending('createdAt')  ## 按时间，升序排列
		query.select('Expand','Title')
		query.equal_to('Expand', False)
		aFinds = query.find()
		if (len(aFinds) == 0):
			return None
		else:
			return aFinds[0].get('Title')

	def Add(self, sTitle):
		# 返回 objectId
		# 检查存过没有
		BaikeClass = leancloud.Object.extend( self.__DBClassName )

		objectId = self.Get_objectId_By_Title(sTitle)
		if (objectId is None):
			dB = BaikeClass()
			dB.set('Title', sTitle)
			dB.set('Expand', False) #展开链接否
			dB.save()
			print('Add:',sTitle)
			return dB.id
		else:
			return None

	def Update_Content(self, sTitle, sContent, bExpand):
		# 返回 objectId
		# 检查存过没有
		BaikeClass = leancloud.Object.extend( self.__DBClassName )

		objectId = self.Get_objectId_By_Title(sTitle)
		if (objectId is None):
			return None
		else:
			dB = BaikeClass.create_without_data(objectId)
			dB.set('Content', sContent)
			dB.set('Expand', bExpand)  # 展开链接否
			dB.save( )
			print('Update_Content:', sTitle)
			return dB.id

	def Get_objectId_By_Title(self,sTitle):
		BaikeClass = leancloud.Object.extend(self.__DBClassName)
		query = BaikeClass.query
		query.select('Title','objectId')
		query.equal_to('Title', sTitle)
		aFind = query.find()
		if(len(aFind)==0):
			return None
		else:
			return aFind[0].get('objectId')

	############## private #####
	def __init__(self):
		self.__DBClassName = "Baike"


##########################Do not delete############################
BAIKE_CLASS = Class_Baike()