# coding: utf-8
# base functions for this project
# Standard library imports
import requests
from datetime import datetime, timedelta
import time
import random
import subprocess
import select
import codecs
import psutil

import urllib.request as myurllib

#TIME_START = time.time()
#time.sleep(1)
#print  time.time()-TIME_START

#update = '11-03'
#update_l = str( 2017 ) + '-' + update
#print update_l[:7]

#print filter(lambda ch: ch in "0123456789-:", u'\u53d1\u8868\u4e8e 2017-11-28  16:14:33')

#def Name_of_day( day ):
	#返回：yyyymmdd，补零
    #return str(day.year) + str(day.month).zfill(2) + str(day.day).zfill(2)

'''
import psutil
import os
import psutil
import os

info = psutil.virtual_memory()
print u'内存使用：',psutil.Process(os.getpid()).memory_info().rss
print u'总内存：',info.total
print u'内存占比：',type(info.percent),info.percent
print u'cpu个数：',psutil.cpu_count()
'''

proxy = myurllib.ProxyHandler({'http': '111.225.8.62:9999'})
auth = myurllib.HTTPBasicAuthHandler()
opener = myurllib.build_opener(proxy, auth, myurllib.HTTPHandler)
myurllib.install_opener(opener)
#print( myurllib.urlopen("http://blog.csdn.net/").read())

def Get_Html_String_Use_Local_Proxy( url ):
	return myurllib.urlopen(url).read()

def Get_Html_String_Use_phantomjs( url ):
	OutputShell('phantomjs htmlbody.js ' + url)
	time.sleep(2)
	return Load_From_File('body.html')

def Load_From_File(filename):
	ffile = codecs.open(filename, 'r', 'utf-8')
	text = ffile.read()
	ffile.close()
	return text

def OutputShell( cmd, **params ):
	print( 'shell:',cmd)
	result = subprocess.Popen(
		#[ "ping 127.0.0.1" ],
		#[ "find /usr" ],
		[ cmd ],
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	# read date from pipe
	select_rfds = [ result.stdout, result.stderr ]
	while len( select_rfds ) > 0:
		(rfds, wfds, efds) = select.select( select_rfds, [ ], [ ] ) #select函数阻塞进程，直到select_rfds中的套接字被触发
		if result.stdout in rfds:
			readbuf_msg = result.stdout.readline()      #行缓冲
			if len( readbuf_msg ) == 0:
				select_rfds.remove( result.stdout )     #result.stdout需要remove，否则进程不会结束
			else:
				print( readbuf_msg)

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				print( readbuf_errmsg)
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	return result.returncode

def Is_Dealday(theday):
	#theday: 无需注意是否是00：00
	#input:theday <Type:datetime>
	#返回theday是否周一～周五
	dayOfWeek = 1+theday.weekday()  # weekday() 返回的是0-6是星期一到星期日
	if (6== dayOfWeek):  # 周6
		return False
	elif(7== dayOfWeek):	# 周7
		return False
	else:		#周1～5，均为交易日
		return True

def Get_Dealday_Last(theday):
	#theday: 无需注意是否是00：00
	#input:theday <Type:datetime>
	#返回theday的上一个交易日的datetime,该日的0:00
	#today = datetime.today()
	dayOfWeek = 1+theday.weekday()  # weekday() 返回的是0-6是星期一到星期日
	if (1== dayOfWeek):  # 周1,返回上周5,即3天前
		day0000 = datetime( theday.year, theday.month, theday.day ) - timedelta( days=3 )
	elif(7== dayOfWeek):	# 周7,返回上周5,即2天前
		day0000 = datetime( theday.year, theday.month, theday.day ) - timedelta( days=2 )
	else:		#周2～6的前一天，均为交易日
		day0000 = datetime( theday.year, theday.month, theday.day ) - timedelta( days=1 )
	return day0000

def Get_First_Char_Of_Sting( tmpstr,num ):
	#截取前40个字符，用于经代理采集后，返回非目标代码的情况，这时看看返回了什么
	try:
		tmpstr = (tmpstr.encode('utf-8')) #<type 'unicode'> 转 <type 'str'>
	except:
		pass
	if(num<len(tmpstr)):
		return tmpstr[:num]
	else:
		return tmpstr

def Unset_Private_Proxy( id ):
	# 释放id号的代理
	# call example:
	# http://agentpool.leanapp.cn/unset/?id=12345
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
	url_unset_proxy = 'http://agentpool.leanapp.cn/unset/?id=' + id
	try:
		response = requests.get(url_unset_proxy, headers=headers, timeout=7.3)
	except:
		pass

def Get_Html_String_Use_Private_Proxy( url, Refefer, id ):
	#return HtmlStr
	# 使用自己的proxy池，注意：仅返回目标网页源代码文本
	# 返回:页面Html, <type 'unicode'>
	# call example:
	# http://agentpool.leanapp.cn/html/?u=http://hq.sinajs.cn/list=sh600000&r=http://finance.sina.com.cn/realstock/company/sh600000/nc.shtml
	# http://agentpool.leanapp.cn/html/?id=12345&u=http://hq.sinajs.cn/list=sh600000&r=http://finance.sina.com.cn/realstock/company/sh600000/nc.shtml
	headers = {
		"User-Agent": "Mozilla/5.3(Windows NT 5.1; WOW64) AppleWebKit/527.36 (KHTML, like Gecko) Chrome/51.0.2713.82 Safari/527.36"}
	url_use_proxy = 'http://httppool.leanapp.cn/html/?id=' + id + '&u=' + url + '&r=' + Refefer
	#url_use_proxy = 'http://agentpool.leanapp.cn/html/?id=' + id + '&u=' + url + '&r=' + Refefer
	try:
		response = requests.get( url_use_proxy, headers=headers, timeout=12.3)
	except (IOError) as err:
		print( 'Get_Html_String_Use_Private_Proxy()1 ERROR:', err)
		time.sleep(random.randint(3, 5))
		try:
			response = requests.get(url_use_proxy, headers=headers, timeout=12.3)
		except (IOError) as err:
			print( 'Get_Html_String_Use_Private_Proxy()2 ERROR:', err)
			return '<HTML></HTML>'
	return response.text

def Get_Html_String_Use_Proxy( url, Refefer ):
	# 使用自己的proxy池，注意：仅返回目标网页源代码文本
	# call example:
	# http://proxy.leanapp.cn/gethtml/?url=http://hq.sinajs.cn/list=sh600000&Refefer=http://finance.sina.com.cn/realstock/company/sh600000/nc.shtml
	#return HtmlStr
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
	url_use_proxy = 'http://proxy.leanapp.cn/gethtml/?url=' + url + '&Refefer=' + Refefer
	try:
		response = requests.get( url_use_proxy, headers=headers, timeout=7.3)
	except (IOError) as err:
		print( 'Get_Html_String_Use_Proxy()1 ERROR:', err)
		#time.sleep(random.randint(0, 1))
		try:
			response = requests.get(url_use_proxy, headers=headers, timeout=7.3)
		except (IOError) as err:
			print( 'Get_Html_String_Use_Proxy()2 ERROR:', err)
			#print 'Return WarningProxy.', err
			return 'WarningProxy'
	#print type( response.text )  # <type 'unicode'>
	#print response.text
	#print type( response.content )  # <type 'str'>
	# OLD:可能为状态码，eg 404, 也可能为劫持后的广告代码(response.status_code==200)
	# http://proxy.leanapp.cn/gethtml可能返回‘’(只要错错)
	time.sleep( random.randint( 5, 8 ) )
	return response.text

