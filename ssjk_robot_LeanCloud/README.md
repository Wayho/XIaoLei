# SSJK回复机器人

使用chatterbot的回复机器人,数据来源于XiaoLei_Corpus.

在微信号向公众号端发送消息后,直接转发到LeanCloud端(通过公众号后台配置),

即:使用LeanCloud云引擎作为微信公众号的回调服务器,Lean马上回复空串,避免耗时

在Lean获得回复字串后,直接通过WeChatClient.message.send_text()发送迟到的消息

```
#使用机器人回复,有个比较耗时的检索任务在这里运行
def message_robot(sFromUserName, sContent):
	#time.sleep(5)
	sMessage = str(oChatBot.get_response(sContent))
	print("<<", sMessage)
	oWeChatClient.message.send_text(sFromUserName, sMessage)
```


```
        msg = parse_message(request.data)
		print(">>", str(msg))
		if msg.type == 'text':
			reply = create_reply('', msg)
			message = xmltodict.parse(to_text(request.data))['xml']
			#MESSAGEROBOT.Reset(message['FromUserName'], msg.content)
			_thread.start_new_thread(message_robot, (message['FromUserName'], msg.content,))
		else:
			reply = create_reply('抱歉,仅支持文本', msg)
		#print(type(reply.render()))
		return reply.render()
```



## 相关文档

* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)
