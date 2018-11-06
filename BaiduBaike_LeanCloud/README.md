# BaiduBaike

依托百度百科,从一个条目(节点)开始,爬取关联节点的标题和内容,并存储于LeanCloud中

## htmlbody.js

* 专门用于模拟浏览器的运行JS生成的页面HTML,只取<body>部分,保存在body.html
* 命令行:phantomjs htmlbody.js 区域变电站

```
function html_body(url){
    console.log('html_body');
    //url = 'https://proxy.leanapp.cn/'
    page.open(url, function(status) {
        console.log('accessing network');
        if (status !== 'success') {
            console.log('Unable to access network');
        }
        else {
            var ua = page.evaluate(function() {
                return document.body.innerHTML;
            });
            //console.log(ua);
            //只取<body>部分,若要全部,可返回page.content
            fs.write('body.html', ua, 'w');
            phantom.exit();
        }
    });
}

var fs = require('fs')
var page = require('webpage').create();
console.log('The default user agent is ' + page.settings.userAgent);
page.settings.userAgent = 'SpecialAgent';

var url0 = 'https://baike.baidu.com/item/' + '%E5%8C%BA%E5%9F%9F%E5%8F%98%E7%94%B5%E7%AB%99'
var url = 'https://baike.baidu.com/item/'
var cmd = 'phantomjs htmlbody.js 区域变电站'

var system = require('system');
if (system.args.length === 1) {
    console.log('Try to pass some args when invoking this script!');
}
else {
    var sTitle =system.args[1];
    console.log(url0)
    console.log(url + encodeURIComponent(sTitle))
    html_body(url + encodeURIComponent(sTitle))
}
```

## baidubaike.py
通过 htmlbody.js 生成的body.html,解析各个HTML元素:节点名,节点内容,关联节点表
* Title() 节点名
* Content() 节点内容
* Content2() 节点内容(定义)
* Links 关联节点表

## classbaike.py

对Baike数据库执行操作的对应类

## cloud.py

执行爬取逻辑

```
@engine.define( 'baike' )
#以Baike库中未展开的节点开始执行展开,获取百度百科中的关联节点
def baike():
	sTitle = '变电站'
	while(sTitle):
		sTitle = BAIKE_CLASS.Find_Not_Expand()
		print ('baike',sTitle)
		if(sTitle):
			shellbaike(sTitle)
	print('************ End of Expand **************')
	return True
```

```
#{'title':'区域变电站'}
@engine.define( 'shellbaike' )
#title:节点名
#按节点名执行模拟浏览器的JS运行生成关联节点,并通过baidubaike.Links()得到关联节点
def shellbaike(title):
	OutputShell('phantomjs htmlbody.js '+title)
	time.sleep(5)
	sContent = baidubaike.Content()
	if('' == sContent ):
		sContent = baidubaike.Content2()
	aLinks = baidubaike.Links()
	print(type(aLinks),len(aLinks),aLinks)
	for Title_link in aLinks:
		BAIKE_CLASS.Add(Title_link)
	BAIKE_CLASS.Update_Content(title,sContent,True)
	time.sleep(5)
	return True
```

## 相关文档

* [phantomjs in LeanEngine](https://leancloud.cn/docs/leanengine_webhosting_guide-python.html#hash-1294723055)
* [phantomjs](http://phantomjs.org)
* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)


