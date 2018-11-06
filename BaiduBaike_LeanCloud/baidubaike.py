# -*- coding: UTF-8 -*-
import codecs
from lxml import etree

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

#解析各个HTML元素:
#节点名,节点内容,关联节点表
def Title():
	# 节点名
	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# 条目名称  ######################################################################
	# <dd class="lemmaWgt-lemmaTitle-title">
	# <h1 >区域变电站</h1>
	# <a href="javascript:;" class="edit-lemma cmn-btn-hover-blue cmn-btn-28 j-edit-link"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a>
	# <a class="lock-lemma" nslog-type="10003105" target="_blank" href="/view/10812319.htm" title="锁定"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_lock-lemma"></em>锁定</a>
	# </dd>
	sRet = ''
	try:
		title = selector.xpath( '//dd[@class="lemmaWgt-lemmaTitle-title"]//h1/text()' )[0]
		sRet = str(title)
	except:
		pass
	return sRet

def Content():
	#节点内容
	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# Content ##################################################################
	#<div class="para" label-module="para">区域变电站指电压在35KV及以上330KV以下，向数个地区或大城市供电的变电站。</div>
	#<div class="para" label-module="para">它将远处的高压电力转送到较远的负荷中心，还同时降压后向当地和邻近地区供电。在电网高电压的变电站中，除少数地区为枢纽变电站外，其余均为区域变电站</div>
	sRet = ''
	First = True
	try:
		contents = selector.xpath( '//div[@class="para"]/text()' )
		for text in contents:
			if(First):
				sRet += str(text)
				First = False
			else:
				sRet += '\n' + str(text)
	except:
		pass
	return sRet

def Content2():
	#节点内容(定义)
	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# Content ##################################################################
	# <dl class="clearfix">
	# <dt>定&#12288;&#12288;义</dt>
	# <dd>向数个地区或大城市供电的变电站。</dd>
	# </dl>
	sRet = ''
	try:
		text = selector.xpath('//dl[@class="clearfix"]//dd/text()')[2]
		sRet += str(text)
	except:
		pass
	return sRet

def Links():
	#关联节点表
	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# body.html 为通过phantomjs getbody.js 获取的页面内body的源代码,经过了js的运行 #####
	# 底部链接
	aRet = []
	try:
		links = selector.xpath( '//a[@class="link-inner"]/text()' )
		print("Links", type(links), len(links))
		for text in links:
			aRet.append( str(text))
	except:
		pass
	return aRet

#sContent = Content2()
#print(type(sContent), len(sContent),sContent)
#print(Links())


