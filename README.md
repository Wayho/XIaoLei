# XiaoLei

一个简单的使用 ChatterBot和Flask 的 LeanCloud 应用,运行于LeanCloud 的 python3环境。

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

## 相关文档
* [flask-chatterbot](https://github.com/chamkank/flask-chatterbot)
* [ChatterBot](https://github.com/gunthercox/ChatterBot)
* [chatterbot-corpus](https://github.com/gunthercox/chatterbot-corpus)
* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)
