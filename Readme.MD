# XiaoLei

## 小程序版
包含两个应用:
* Xiaolei_Leancloud
* XiaoLei_MiniApp
Xiaolei_Leancloud为XiaoLei_MiniApp提供云服务,Xiaolei_Leancloud可以独立以web方式运行

包含两个工具:

* praseword.py:把txt转yml
* train.py:生成db.sqlite3

## XiaoLei_LeanCloud

一个简单的使用 ChatterBot和Flask 的 LeanCloud 应用,运行于LeanCloud 的 python3环境。

### db.sqlite3

来源于使用train.py得到,基于如下步骤:

1.使用../XiaoLei_Corpus/praseword.py 把 GBT50297.txt 转为 GBT50297.yml

2.把 GBT50297.yml 复制到 /home/XXX/.pyenv/versions/3.6.4/lib/python3.6/site-packages/chatterbot_corpus/data/chinese

3.python train.py

XiaoLei_Corpus和PowerProject_LeanCloud中的praseword.py是一样的

## XiaoLei_Corpus

把 GBT50297.txt 转为 GBT50297.yml。

## PowerProject_LeanCloud

在LeanCloud 中存储<电力工程基本术语标准20130604>,也可转为chatterbot-corpus的yml,运行于LeanCloud 的 python2环境。

praseword.py 是在云端执行的

##################################################
# XiaoLei

## 公众号版

## BaiduBaike_LeanCloud

依托百度百科,从一个条目(节点)开始,爬取关联节点的标题和内容,并存储于LeanCloud中

## ssjk_robot_LeanCloud

SSJK回复机器人

使用chatterbot的回复机器人,数据来源于XiaoLei_Corpus.

在微信号向公众号端发送消息后,直接转发到LeanCloud端(通过公众号后台配置),

即:使用LeanCloud云引擎作为微信公众号的回调服务器,Lean马上回复空串,避免耗时

在Lean获得回复字串后,直接通过WeChatClient.message.send_text()发送迟到的消息

##################################################

## 小程序机器人客服聊天 .zip


## 相关文档
* [flask-chatterbot](https://github.com/chamkank/flask-chatterbot)
* [ChatterBot](https://github.com/gunthercox/ChatterBot)
* [chatterbot-corpus](https://github.com/gunthercox/chatterbot-corpus)
* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)