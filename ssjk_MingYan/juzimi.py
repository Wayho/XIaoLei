# coding: utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
# Standard library imports

import random
import time
from lxml import etree
from datetime import datetime, timedelta

import  os


# local imports

DELAY_BASE = 8

from functions import Get_Html_String_Use_Private_Proxy,Unset_Private_Proxy,Get_First_Char_Of_Sting,Get_Html_String_Use_phantomjs,Get_Html_String_Use_Local_Proxy

from classwriter import WRITER_CLASS
from classmingju import MINGJU_CLASS
#from agentpool import Class_Proxy
'''
ShortUrl = [
{'type':'/dynasty/','page':3, 'country':'先秦'},
{'type':'/dynasty/','page':4, 'country':'汉朝'},
{'type':'/dynasty/','page':4, 'country':'魏晋'},
{'type':'/dynasty/','page':3, 'country':'南北朝'},
{'type':'/dynasty/','page':5, 'country':'隋唐五代'},
{'type':'/dynasty/','page':5, 'country':'宋朝'},
{'type':'/dynasty/','page':4, 'country':'元朝'},
{'type':'/dynasty/','page':5, 'country':'明朝'},
{'type':'/dynasty/','page':5, 'country':'清朝'},
{'type':'/dynasty/','page':5, 'country':'近现代'},
{'type':'/country/','page':5, 'country':'美国'},
{'type':'/country/','page':5, 'country':'英国'},
{'type':'/country/','page':5, 'country':'法国'},
{'type':'/country/','page':5, 'country':'德国'},
{'type':'/country/','page':5, 'country':'日本'},
{'type':'/country/','page':5, 'country':'俄国'},
{'type':'/country/','page':3, 'country':'希腊'},
{'type':'/country/','page':2, 'country':'罗马'},
{'type':'/country/','page':4, 'country':'意大利'},
{'type':'/country/','page':2, 'country':'奥地利'},
{'type':'/country/','page':2, 'country':'印度'}
]
'''
ShortUrl = [
]


class Class_Http_Get_MingYan():
	# A class get html and prase it like this url:
	# http://guba.eastmoney.com/news,600683,693158720.html
	# 为解决主页面中夹杂混乱日期的方案
	# 直接返回页面中最后的日期，1、先找zwlitime，返回最后一个，若无，返回zwfbtime
	# <div class="zwfbtime">发表于 2017-08-16 10:45:55 股吧网页版</div>	=楼主，一定有
	# <div class="zwlitime">发表于 2017-12-12  15:53:44</div>			=评论，不一定有

	############## private ################
	def __init__(self):

		self.__BaseUrl = "https://www.juzimi.com"
		self.__dalay = DELAY_BASE					#每个专属代理有一个专属延时，可以根据返回码决定是否增加延时
		#self.__Prase_Page()

	def Test(self):

		#return
		oWriter = WRITER_CLASS.Get_Writer_One()
		# print(oWriter.get('country'),oWriter.get('name'),oWriter.get('url'))
		print(oWriter)
		RefererUrl = 'https://www.juzimi.com'
		Url = oWriter.get('url')
		iStartPage = oWriter.get('page')
		#Url = 'https://www.juzimi.com/writer/%E8%AF%97%E7%BB%8F'
		if(0==iStartPage):
			iPage = self.Http_Prase_Page(Url, RefererUrl,oWriter.get('name'),oWriter.get('country'))
			WRITER_CLASS.Update_page(oWriter.get('objectId'), 1)
		else:
			iPage = self.Http_Prase_Page(Url + '?page=' + str(iStartPage), RefererUrl, oWriter.get('name'),
			                             oWriter.get('country'))
			WRITER_CLASS.Update_page(oWriter.get('objectId'), iStartPage+1)
		print('pages=',iPage)
		for page in range(iStartPage+1,iPage):
			self.Http_Prase_Page(Url+'?page='+str(page), Url ,oWriter.get('name'), oWriter.get('country'))
			WRITER_CLASS.Update_page(oWriter.get('objectId'), page+1)
			time.sleep(random.randint(12, 16))
		WRITER_CLASS.Update_active(oWriter.get('objectId'), True)
		#WRITER_CLASS.Update_page(oWriter.get('objectId'), iPage)
		print('***************** End of Prase *******************')

	def Test_0(self):
			RefererUrl = 'https://www.juzimi.com'
			Url = 'https://www.juzimi.com/writer/%E8%AF%97%E7%BB%8F'
			print(Url)
			Html_Str = Get_Html_String_Use_Private_Proxy(Url, RefererUrl, '0')
			print(id, Get_First_Char_Of_Sting(Html_Str, 60))
			oWriter = self.__Prase_Page(Html_Str)
			#oWriter = self.__Print_Page_Num(Html_Str)
			print(oWriter)
			time.sleep(random.randint(8, 16))

			print('***************** End of Prase *******************')

	def Http_Get_MinJu_All(self):
		while(True):
			oWriter = WRITER_CLASS.Get_Writer_One()
			# print(oWriter.get('country'),oWriter.get('name'),oWriter.get('url'))
			print(oWriter)
			RefererUrl = 'https://www.juzimi.com'
			Url = oWriter.get('url')
			iStartPage = oWriter.get('page')
			# Url = 'https://www.juzimi.com/writer/%E8%AF%97%E7%BB%8F'
			if (0 == iStartPage):
				iPage = self.Http_Prase_Page(Url, RefererUrl, oWriter.get('name'), oWriter.get('country'))
				WRITER_CLASS.Update_page(oWriter.get('objectId'), 1)
			else:
				iPage = self.Http_Prase_Page(Url + '?page=' + str(iStartPage), RefererUrl, oWriter.get('name'),
				                             oWriter.get('country'))
				WRITER_CLASS.Update_page(oWriter.get('objectId'), iStartPage + 1)
			print('pages=', iPage)
			time.sleep(random.randint(38, 43))
			for page in range(iStartPage + 1, iPage):
				self.Http_Prase_Page(Url + '?page=' + str(page), Url, oWriter.get('name'), oWriter.get('country'))
				WRITER_CLASS.Update_page(oWriter.get('objectId'), page + 1)
				time.sleep(random.randint(62, 68))
			WRITER_CLASS.Update_active(oWriter.get('objectId'), True)
			# WRITER_CLASS.Update_page(oWriter.get('objectId'), iPage)
			print('***************** End of Prase *******************')
		return



	def Http_Prase_Page(self, Url, RefererUrl, sAuther, sCountry):
		aMingYan = []
		iPage = 1
		while(0==len(aMingYan)):
			id = str(random.randint(0,200))
			print('request:',Url)
			#Html_Str = Get_Html_String_Use_Private_Proxy(Url, RefererUrl, id)
			Html_Str = Get_Html_String_Use_phantomjs(Url)
			#Html_Str = Get_Html_String_Use_Local_Proxy(Url)
			#proxy = Class_Proxy()
			#Html_Str = proxy.Get_Html_String(Url, RefererUrl, False)
			print(id, Get_First_Char_Of_Sting(Html_Str,60))
			aMingYan = self.__Prase_Page(Html_Str)
			iPage = self.__Get_Page_Num(Html_Str)
			time.sleep(random.randint(self.__dalay, self.__dalay + 3))
		for m in aMingYan:
			print(m)
			MINGJU_CLASS.Add(m.get('content'),m.get('from'),m.get('like'), sAuther, sCountry)
		return iPage

	def __Prase_Page(self,html_str):
		# 解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		aMingYan = []
		selector = etree.HTML(html_str)
		try:
			articleh = selector.xpath('//div[@class="views-field-phpcode"]')
			print("Total:", len(articleh))
			for ainfo in articleh:
				try:
					aContent = ainfo.xpath('.//div[@class="views-field-phpcode-1"]/a[@class="xlistju"]/text()')
					sContent = ''
					for content in aContent:
						sContent += content
					sContent= sContent.replace(' ','')

					try:
						sFrom = str(ainfo.xpath(
							'.//span[@class="views-field-field-oriarticle-value"]/a[@class="active"]/text()')[0])
					except:
						sFrom = ''
					sLike = str(ainfo.xpath('.//div[@class="views-field-ops"]/a[@class="flag-action"]/text()')[0])
					sLike = str(self.__Delete_No_Digit(sLike))
					try:
						iLike = int(sLike)
					except:
						iLike = 0
					aMingYan.append({'content': sContent, 'from': sFrom, 'like': iLike})
				except:
					pass
		except:
			pass
		return aMingYan


	def __Prase_Page_Content_NG(self,html_str):
		# 解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		aMingYan = []
		selector = etree.HTML(html_str)
		try:
			articleh = selector.xpath('//div[@class="views-field-phpcode-1"]')
			#### print '阅读\t评论\t标题\t作者\t发表日期\t最后更新'
			print("Total:", len(articleh))
			for ainfo in articleh:
				try:
					sMingYan = ''
					aTmp = ainfo.xpath('.//a[@class="xlistju"]/text()')
					for duanluo in aTmp:
						sMingYan += str(duanluo)
						#print (type(sMingYan), sMingYan)
					aMingYan.append(sMingYan)
				except:
					pass
		except:
			pass
		return aMingYan

	def __Prase_Page_OK(self,html_str):
		#解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		aMingYan = []
		selector = etree.HTML(html_str)
		try:
			articleh = selector.xpath('//div[@class="views-field-phpcode"]')
			print("Total:", len(articleh))
			for ainfo in articleh:
				try:
					aContent = ainfo.xpath('.//div[@class="views-field-phpcode-1"]/a[@class="xlistju"]/text()')
					sContent = ''
					for content in aContent:
						sContent += content
					try:
						sFrom = str(ainfo.xpath('.//span[@class="views-field-field-oriarticle-value"]/a[@class="active"]/text()')[0])
					except:
						sFrom = ''
					sLike = str(ainfo.xpath('.//div[@class="views-field-ops"]/a[@class="flag-action"]/text()')[0])
					sLike = str(self.__Delete_No_Digit(sLike))
					try:
						iLike = int(sLike)
					except:
						iLike = 0
					aMingYan.append({'content':sContent,'from':sFrom,'like':iLike})
				except:
					pass
		except:
			pass
		return aMingYan

	def __Print_Page__(self,html_str):
		#解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		print('Print')
		selector = etree.HTML( html_str )
		try:
			articleh = selector.xpath( '//div[@class="views-field-phpcode"]' )
			print( "Total:",len(articleh))
			for ainfo in articleh:
				try:
					sMingYan = ''
					aTmp = ainfo.xpath('.//div[@class="views-field-phpcode-1"]/a[@class="xlistju"]/text()')
					#aTmp = ainfo.xpath('.//div[@class="views-field-phpcode-1"]/text()')
					#aTmp = ainfo.xpath('.//a[@class="xlistju"]/text()')
					for duanluo in aTmp:
						print('*')
						sMingYan += str(duanluo)
					sFrom = str(ainfo.xpath('.//span[@class="views-field-field-oriarticle-value"]/a[@class="active"]/text()')[0])
					sLike = str(ainfo.xpath('.//div[@class="views-field-ops"]/a[@class="flag-action"]/text()')[0])
					sLike = str(self.__Delete_No_Digit(sLike))
					try:
						iLike = int(sLike)
					except:
						iLike = 0
					print (type(sMingYan), sMingYan)
					print (type(sFrom), sFrom)
					print (type(iLike), iLike)

				except:
					pass
			return len(articleh)
		except:
			return 0

	def __Get_Page_Num(self,html_str):
		#解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		selector = etree.HTML( html_str )
		try:
			#articleh = selector.xpath( '//li[@class="pager-item"]/a[@class="active"]/text()' )
			try:
				sPage = selector.xpath('//li[@class="pager-last"]/a[@class="active"]/text()')[0]
				ipage = int(sPage)
				return ipage
			except:
				#print('No last page')
				ipage = 1
				articleh = selector.xpath('//li[@class="pager-item"]/a[@class="active"]/text()')
				for spage in articleh:
					#print(type(spage), spage)
					try:
						ip = int(str(spage))
						if(ip>ipage):
							ipage=ip
					except:
						print('************* Error ******************')
						ipage = 0
				return ipage
		except:
			return 1

	def __Delete_No_Digit(self, divtext):
		# 过滤掉非数字
		digit =  divtext.replace('喜欢','')
		digit = digit.replace('(', '')
		digit = digit.replace(')', '')
		return str(digit)

	def __Delete_No_Digit__(self, divtext):
		# input u'\u53d1\u8868\u4e8e 2017-11-28  16:14:33'		#2空格
		# return 2017-11-28	#1空格
		# 过滤掉非数字
		#print type(timedivtext),timedivtext
		digit =  str(filter( lambda ch: ch in "0123456789", divtext ))		#2017-11-2816:14:33 #0空格
		return str(digit)


class Class_Http_Get_Writer():
	# A class get html and prase it like this url:
	# http://guba.eastmoney.com/news,600683,693158720.html
	# 为解决主页面中夹杂混乱日期的方案
	# 直接返回页面中最后的日期，1、先找zwlitime，返回最后一个，若无，返回zwfbtime
	# <div class="zwfbtime">发表于 2017-08-16 10:45:55 股吧网页版</div>	=楼主，一定有
	# <div class="zwlitime">发表于 2017-12-12  15:53:44</div>			=评论，不一定有

	############## private ################
	def __init__(self):

		self.__BaseUrl = "https://www.juzimi.com"
		self.__dalay = DELAY_BASE					#每个专属代理有一个专属延时，可以根据返回码决定是否增加延时
		#self.__Prase_Page()

	def Test(self):
		while(True):
			RefererUrl = self.__BaseUrl
			Url = 'https://www.juzimi.com/country/%E4%BF%84%E5%9B%BD'
			#Html_Str = Get_Html_String_Use_Private_Proxy(Url, RefererUrl, '0')
			proxy = Class_Proxy()
			Html_Str = proxy.Get_Html_String(Url,RefererUrl,False)
			print(Get_First_Char_Of_Sting(Html_Str,60))
			self.__Print_Page(str(Html_Str))
			time.sleep(random.randint(8, 16))

	def Http_Get_Writer_Url(self):
		for iWriter in range(len(ShortUrl)):

			for page in range(ShortUrl[iWriter].get('page')):
				if(0==page):
					RefererUrl = self.__BaseUrl
					Url = self.__BaseUrl + ShortUrl[iWriter].get('type') + ShortUrl[iWriter].get('country')
				else:
					RefererUrl = self.__BaseUrl + ShortUrl[iWriter].get('type') + ShortUrl[iWriter].get('country')
					Url = RefererUrl + '?page=' + str(page)
				print('page:',page)
				print('Url:', Url)
				#time.sleep( random.randint( self.__dalay, self.__dalay+3 ) )
				oWriter = self.Http_Prase_Page(Url, RefererUrl)
				for writer in oWriter:
					print(ShortUrl[iWriter].get('country'), writer.get('name'),writer.get('url'))
					WRITER_CLASS.Add(ShortUrl[iWriter].get('country'), writer.get('name'),writer.get('url'))
				print(page, 'Total',len(oWriter))
				#self.__Get_pagernums(Html_Str)


	def Http_Prase_Page(self, Url, RefererUrl):
		oWriter = []
		while(0==len(oWriter)):
			id = str(random.randint(0,200))
			Html_Str = Get_Html_String_Use_Private_Proxy(Url, RefererUrl, id)
			#proxy = Class_Proxy()
			#Html_Str = proxy.Get_Html_String(Url, RefererUrl, False)
			print(id, Get_First_Char_Of_Sting(Html_Str,60))
			oWriter = self.__Prase_Page(Html_Str)
			time.sleep(random.randint(self.__dalay, self.__dalay + 3))
		return oWriter

	def __Prase_Page(self,html_str):
		# 解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		oWriter = []
		selector = etree.HTML(html_str)
		try:
			articleh = selector.xpath('//div[@class="views-field-name"]')
			#### print '阅读\t评论\t标题\t作者\t发表日期\t最后更新'
			print("Total:", len(articleh))
			for ainfo in articleh:
				try:
					strUrl = self.__BaseUrl + ainfo.xpath('.//a/@href')[0]
					strWriter = ainfo.xpath('.//a/text()')[0]
					oWriter.append({'name':strWriter,'url':strUrl})
				except:
					pass
		except:
			pass
		return oWriter

	def __Print_Page(self,html_str):
		#解析一个页面，'阅读\t评论\t标题\t作者\t发表日期\t最后更新'
		selector = etree.HTML( html_str )
		try:
			articleh = selector.xpath( '//div[@class="views-field-name"]' )
			#### print '阅读\t评论\t标题\t作者\t发表日期\t最后更新'
			print( "Total:",len(articleh))
			for ainfo in articleh:
				try:
					strUrl = self.__BaseUrl + ainfo.xpath( './/a/@href' )[ 0 ]
					strWriter = ainfo.xpath('.//a/text()')[0]
					print (strUrl,strWriter)
				except:
					pass
			return len(articleh)
		except:
			return 0

