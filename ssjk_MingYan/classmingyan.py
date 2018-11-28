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
class Class_MingYan():
	# 处理 Chat Class的存取，没有属性，仅提供方法

	def Random(self):
		# return str
		MingYanClass = leancloud.Object.extend( self.__DBClassName )
		query = MingYanClass.query
		index = random.randint(0,8309)
		query.select('Content','Auther')
		query.equal_to('Index', index)
		aFind = query.find()
		if (len(aFind) == 0):
			return None
		else:
			return aFind[0].get('Content') + '\r\n——' + aFind[0].get('Auther')

	def Import(self):
		# 返回 objectId
		# 检查存过没有
		sFileText = Load_From_File('名人名言大全.txt')

		aFileText = sFileText.split('\n')
		print(len(aFileText))
		for i in range(int(len(aFileText)/2)):
		#for i in range(10):
			Content = aFileText[2*i]
			Auther = aFileText[2 * i+1].replace('—','')
			self.Add(Content,Auther,i)
			print(Content[:30],Auther)
			#return


	def Add(self, sContent,sAuther,iIndex):
		# 返回 objectId
		# 检查存过没有
		MingYanClass = leancloud.Object.extend( self.__DBClassName )

		dB = MingYanClass()
		dB.set('Content', sContent) #展开sOpenid
		dB.set('Auther', sAuther)
		dB.set('Index', iIndex)
		dB.save()
		return dB.id

	############## private #####
	def __init__(self):
		self.__DBClassName = "MingYan"


##########################Do not delete############################
MINGYAN_CLASS = Class_MingYan()