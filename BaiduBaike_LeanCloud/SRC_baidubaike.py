# -*- coding: UTF-8 -*-
import codecs
import lxml
from lxml import etree
import time


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

def Title():

	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# 条目名称  ######################################################################
	# <dd class="lemmaWgt-lemmaTitle-title">
	# <h1 >区域变电站</h1>
	# <a href="javascript:;" class="edit-lemma cmn-btn-hover-blue cmn-btn-28 j-edit-link"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a>
	# <a class="lock-lemma" nslog-type="10003105" target="_blank" href="/view/10812319.htm" title="锁定"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_lock-lemma"></em>锁定</a>
	# </dd>
	try:
		title = selector.xpath( '//dd[@class="lemmaWgt-lemmaTitle-title"]' )[0][0].xpath('string()')
		print("A",type(title), len(title), title)
	except:
		pass

	try:
		title = selector.xpath( '//dd[@class="lemmaWgt-lemmaTitle-title"]//h1/text()' )[0]
		print("B", type(title), len(title), title)
	except:
		pass


	#条目名称,注意要选第一个
	try:
		titles = selector.xpath( '//dd[@class="lemmaWgt-lemmaTitle-title"]' )[0]
		for tmp in titles:
			try:
				title = tmp.xpath('string()')  # link
				print("C", type(title), len(title), title)
			except:
				pass
	except:
		pass

	#条目名称 ####################################################################
	#<dl class="clearfix">
	#<dt>中文名称</dt>
	#<dd>区域变电站</dd>
	#</dl>
	try:
		title = selector.xpath( '//dl[@class="clearfix"]//dd/text()' )[0]
		print("D", type(title), len(title), title)
	except:
		pass


	#return

	# Content ##################################################################
	#<div class="para" label-module="para">区域变电站指电压在35KV及以上330KV以下，向数个地区或大城市供电的变电站。</div>
	#<div class="para" label-module="para">它将远处的高压电力转送到较远的负荷中心，还同时降压后向当地和邻近地区供电。在电网高电压的变电站中，除少数地区为枢纽变电站外，其余均为区域变电站</div>
	try:
		contents = selector.xpath( '//div[@class="para"]' )
		#print (contents)
		for tmp in contents:
			try:
				text = tmp.xpath('text()')[0]  # link
				print(text)
			except:
				pass
	except:
		pass

	# Content ##################################################################
	#<dl class="clearfix">
	#<dt>定&#12288;&#12288;义</dt>
	#<dd>向数个地区或大城市供电的变电站。</dd>
	#</dl>
	try:
		title = selector.xpath( '//dl[@class="clearfix"]//dd/text()' )[2]
		print("D", type(title), len(title), title)
	except:
		pass

	return

	sHtml = Load_From_File("body.html")
	selector = etree.HTML(sHtml)

	# body.html 为通过phantomjs getbody.js 获取的页面内body的源代码,经过了js的运行 #####
	# 底部链接
	try:
		links = selector.xpath( '//a[@class="link-inner"]/text()' )
		print("Links", type(links), len(links))
		for text in links:
			try:
				print(text,)
			except:
				pass
	except:
		pass

	print('*************************')

	try:
		links = selector.xpath( '//a[@class="link-inner"]' )
		print("Links", type(links), len(links))
		for tmp in links:
			try:
				text = tmp.xpath('text()')[0]  # link
				print(text,)
			except:
				pass
	except:
		pass


Title()


