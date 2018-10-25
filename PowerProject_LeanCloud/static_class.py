# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports

from datetime import datetime, timedelta
import time
# local imports


###################### Class Define #######################
class Class_Dictionary():
	# 处理 Dictionary Class的存取，没有属性，仅提供方法

	def Add_or_Update_Dict(self, objectId, dict):
		# 保存到 Dictionary_Class
		# 返回 objectId
		#print '@@@@@ ', self.Get_Read_d_x_str(read)
		DictionaryClass = leancloud.Object.extend( self.__DBClassName )
		if(objectId is None):
			dB = DictionaryClass()
		else:
			dB = DictionaryClass.create_without_data( objectId )
		# FieldName (d0,d1,d2...,d90,dx,code,date,break,page)		#break,page+20171231
		for fieldname in self.__Field:
			#if(dict.has_key(fieldname)):		#!!!!排除  Status
				#print fieldname,type(dict.get(fieldname)),dict.get(fieldname)
				dB.set( fieldname, dict.get(fieldname) )  # update
		dB.save( )
		if (objectId is None):
			objectId = dB.id
		return objectId

	def Load_Dict(self,theday,code):
		# 调用者需自行保存 objectId，用于 Add_or_Update_Read_to_Dictionary_Class()
		# 返回 Dictionary_Class中特定code的今日记录,type Dict
		DictionaryClass = leancloud.Object.extend( self.__DBClassName )
		query = DictionaryClass.query
		query.equal_to('code', code)
		theday = datetime(theday.year, theday.month, theday.day, 0, 0, 0)
		query.greater_than_or_equal_to( 'date', theday)                 # 今天：0点以后:greater_than
		query.less_than('date', theday+timedelta(days=1))   # 明天天：0点以前:less_than
		readfind = query.find()  # 查找

		# FieldName (d0,d1,d2...,d90,dx,code,date,break,page)		#break,page+20171231
		NAMELIST = GUBA_DATE_CLASS.Get_Name_List()
		objectId = None
		if(1<=len(readfind)):
			objectId = str(readfind[0].get('objectId'))		# uncode-->str
			read = {}
			for fieldname in NAMELIST:
				filed = {fieldname:readfind[0].get(fieldname)}
				read.update(filed)
			#转str
			read[ 'exchange' ] = str(read.get('exchange'))		# uncode-->str
			read[ 'code' ] = str(read.get('code'))			# uncode-->str
			#read['memo'] = 'V20180104 19:15'
		else:
			read = self.Set_Read_Default(code)
		return {'objectId':objectId,'read':read}		##read:{},type Dict


	############## private ################
	def __init__(self):
		self.__DBClassName = "Dictionary"
		self.__Field = ['ISBN','CSPP','Title','Content']



##########################Do not delete############################
DICTIONARY_CLASS = Class_Dictionary()
##########################Do not delete############################