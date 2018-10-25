# coding: utf-8
import re
import codecs

# local imports
#from static_class import DICTIONARY_CLASS

########## Base Functions ##################
# GBT50297
def Save_To_File(sFileName,sText):
	ffile = codecs.open( sFileName, 'w', 'utf-8')
	ffile.write(sText)
	ffile.close()

def Load_From_File(sFileName):
	ffile = codecs.open( sFileName, 'r', 'utf-8')
	sText = ffile.read()
	ffile.close()
	return sText


def Prase_File_To_yml():
	sFileText = "categories:\n- 电力工程\nconversations:\n"
	aItem = Prase_File()
	for item in aItem:
		print(item.get("CSPP"), item.get("Title"))
		print(item.get("Content"))
		sFileText += '- - ' + item.get("Title") + '\n' + '  - ' + item.get("Content") + '\n'

	print("CSPP array length:", len(aItem))
	Save_To_File('GBT50297.yml', sFileText)

def Prase_File():
	sFileText = Load_From_File('GBT50297.txt')
	aCSPP = []
	iStart = 1
	sText = sFileText
	#扫描出现点的位置,作为初步识别章节小节的依据
	while(-1 != iStart):
		(iStart, iEnd) = Find_Dot_Locate(sText)
		if (-1 != iStart):
			sText = sFileText[:iStart]  # 最后的条目已截取，留前面的
			aCSPP.append({"CSPP": sFileText[iStart:iEnd],"Start":iStart})
			print(iStart,iEnd,sFileText[iStart:iEnd])

	List(aCSPP)
	idx=-2
	#删除Content中出现.的idx记录,避免出现截断错误
	while(idx!=-1):
		idx = Find_Error_CSPP(aCSPP)
		print('delete', aCSPP[idx])
		aCSPP.remove(aCSPP[idx])

	#根据每个标号出现位置,组织内容
	aItem = []
	iLastStart = len(sFileText)
	for ocspp in aCSPP:
		(sTitle, sContent) = PraseItem(sFileText[ocspp.get("Start"):iLastStart], ocspp.get("CSPP"))
		iLastStart = ocspp.get("Start")
		aItem.append({"CSPP": ocspp.get("CSPP"), "Title": sTitle, "Content": sContent})
		print(ocspp.get("CSPP"), sTitle)

	# 如果遇到节(无内容),组织小节标题作为内容
	aItem.reverse()
	aRet = []
	for idx in range(len(aItem)):
		sContent = Content_Section(aItem,idx)
		aRet.append({"CSPP": aItem[idx].get("CSPP"), "Title": aItem[idx].get("Title"), "Content": sContent})

	return aRet

		#Dict = {'ISBN':'GBT50297','CSPP':item.get("CSPP"),'Title':item.get("Title"),'Content':item.get("Content")}
		#DICTIONARY_CLASS.Add_or_Update_Dict(None,Dict)
	#List(aItem)

def Content_Section(aItem,idx):
	#根据节(无内容),组织小节标题作为内容
	thisItem = aItem[idx]
	cspp = thisItem.get("CSPP").split('.')
	if(len(cspp)==2):
		#节
		sContent = ""
		First = True
		for item in aItem:
			cs = item.get("CSPP")[:len(thisItem.get("CSPP"))]
			if(thisItem.get("CSPP")==cs):
				#该节下的小节,标题送入节内容
				if(First):
					First = False
					sContent += item.get("Title")
				else:
					sContent += '、' + item.get("Title")
		#print(thisItem.get("CSPP"),sContent)
		return sContent
	else:
		#非节
		return thisItem.get("Content")  #非节返回自己的内容


def List(aItem):
	#查找不合规的条目位置
	for item in aItem:
		print(item)
	print("CSPP array length:", len(aItem))

def Find_Error_CSPP(aItem):
	#查找不合规的条目位置
	for idx in range(1,len(aItem)-3):
		if(  not Check_Right(aItem[idx].get("CSPP"),aItem[idx+1].get("CSPP"),aItem[idx+2].get("CSPP")) ):
			if (not Check_Right(aItem[idx-1].get("CSPP"), aItem[idx + 1].get("CSPP"), aItem[idx + 3].get("CSPP"))):
				print("WWW", aItem[idx + 1].get("CSPP"))
				return  idx+1
	return -1

def CSPP_Compare(a,b):
	#比较包含.的数字串的大小
	#例如版本号,CSPP
	la = a.split('.')
	lb = b.split('.')
	f = 0
	if len(la) > len(lb):
		f = len(la)
	else:
		f = len(lb)
	for i in range(f):
		try:
			if int(la[i]) > int(lb[i]):
				return 1
			elif int(la[i]) == int(lb[i]):
				continue
			else:
				return -1
		except IndexError as e:
			if len(la) > len(lb):
				return 1
			else:
				return -1
	return 0

####查找最后一个条目
#条目符合的依据是带.，前后都是数字
# sCSPP==1.2.3.4
def Check_Right(sCSPP0,sCSPP1,sCSPP2):
	#检查是否合理
	if ((CSPP_Compare(sCSPP1,sCSPP0) == 1) and (CSPP_Compare(sCSPP1,sCSPP2) == 1)):
		return False
	if ((CSPP_Compare(sCSPP1, sCSPP0) == -1) and (CSPP_Compare(sCSPP1, sCSPP2) == -1)):
		return False

	return True
print (Check_Right('1.2.1','1.2.3','1.2.8'))

####查找最后一个条目
#条目符合的依据是带.，前后都是数字
# sCSPP==1.2.3.4
def Find_Dot_Locate(sText):
	#返回包含.的数字串起始地址
	ifind = find_last(sText, '.')
	index_start = 0    # 偏移
	index_end = 1       # 偏移
	if (-1 != ifind):
		try:
			while(IsNumber(sText[ifind+index_end])):
				index_end += 1
			while (IsNumberOrDot(sText[ifind + index_start])):
				index_start -= 1
		except:
			return (-1, -1)
		index_start += 1
		return (ifind+index_start,ifind+index_end)
	return (-1, -1)

### 查找最后出现的字符串
def find_last(string,str):
	#在字符串中寻找目标最后一次出现的位置
	last_position=-1
	while True:
		position=string.find(str,last_position+1)
		if position==-1:
			return last_position
		last_position=position

#是否为数字
def IsNumber(Char):
	sChar = "0123456789"
	for iChar in sChar:
		if(iChar==Char):
			return True
	return False

#是否为数字和.
def IsNumberOrDot(Char):
	sChar = ".0123456789"
	for iChar in sChar:
		if(iChar==Char):
			return True
	return False

#返回条目标题和内容，已除掉空格和标题内英文
# sItem start at 1.2.3
def PraseItem(sItem,sCSPP):
	sItem = sItem[len(sCSPP):]
	ifind = sItem.find('\n')
	if (-1 != ifind):
		sTitle = DeleteBlank(sItem[:ifind],True)
		sContent = DeleteBlank(sItem[ifind+1:],False)
	ifind = sItem.find('\r')
	if (-1 != ifind):
		sTitle = DeleteBlank(sItem[:ifind], True)
		sContent = DeleteBlank(sItem[ifind + 1:], False)
	return(sTitle,sContent)

#删除空格
def DeleteBlank(sText,bEnglish):
	sChar = " ';://&,-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n　"
	if(bEnglish):
		for iChar in sChar:
			sText = sText.replace(iChar, '')
	else:
		#仅删除最前的空格
		while(' ' == sText[:1]):
			sText = sText[1:]
		#sText = sText.replace(' ', '')
		sText = sText.replace('\n', '')
	return sText

'''
####查找最后一个条目
#条目符合的依据是带.，前后都是数字
# sCSPP==1.2.3.4
def Find_LastItem_CSPP(sText):
	ifind = find_last(sText, '.')
	sCSPP = ""
	sTitle = ""
	sContent = ""
	index_start = -1  # 最后的CSPP
	index_end = 1   #最后的CSPP
	ifind_ret= -1
	if (-1 != ifind):
		try:
			while(IsNumber(sText[ifind+index_end])):
				index_end += 1
			while (IsNumberOrDot(sText[ifind + index_start])):
				index_start -= 1
		except:
			return (-1, sCSPP, sTitle, sContent)
		index_start += 1
		ifind_ret = ifind+index_start

		sText_cps = sText[ifind_ret:]  # start at 1.2.3.4
		sCSPP = sText[ifind_ret:ifind+index_end]
		(sTitle, sContent) = PraseItem(sText_cps, sCSPP)
	return (ifind_ret,sCSPP, sTitle, sContent)
'''

Prase_File_To_yml()


