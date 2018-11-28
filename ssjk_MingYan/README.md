# SSJK回复名言

在微信号向公众号端发送消息后,直接转发到LeanCloud端(通过公众号后台配置),

即:使用LeanCloud云引擎作为微信公众号的回调服务器,Lean马上回复

定时通过WeChatClient.message.send_text()发送的消息

juzimi.py:采集juzimi的名言,保存到Class MingJu

```
#使用机器人回复,有个比较耗时的检索任务在这里运行
def message_robot(sFromUserName, sContent):
	#time.sleep(5)
	sMessage = str(oChatBot.get_response(sContent))
	print("<<", sMessage)
	oWeChatClient.message.send_text(sFromUserName, sMessage)
```


```
        	message = xmltodict.parse(to_text(request.data))['xml']
		sOpenid = message['FromUserName']
		sMsgType = message['MsgType']
		print(">>", message)
		if('text' == sMsgType):
			if('0'== message['Content']):
				send_message(sOpenid, '您好,谢谢回复!\r\n您将在每天早中晚分别收到三句名人名言,如需即时收取名人名言,只需向我回复任意消息即可。')
			send_random_message(sOpenid)
		if ('image' == sMsgType or 'voice' == sMsgType):
			#send_message(sOpenid, '您好,谢谢回复!\r\n您将在每天早中晚分别收到三句名人名言,如需即时收取名人名言,只需向我回复任意消息即可。')
			send_random_message(sOpenid)
		elif('event' == sMsgType ):
			if( 'subscribe'== message['Event']):
				send_message(sOpenid, '您好,欢迎关注!\r\n每天早中晚分别自动送您三句名人名言,请回复0以便发送给您(不回复不发送)。')
				send_random_message(sOpenid)
				send_random_message(sOpenid)
				USERINFO_CLASS.Add(sOpenid)
			elif ('unsubscribe' == message['Event']):
				print(sOpenid,' ***** unsubscribe')
		return ''
```



## 相关文档
* [wechatpy](https://github.com/Wayho/wechatpy)
* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)
