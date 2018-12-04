//专门用于模拟浏览器的运行JS生成的页面HTML,只取<body>部分,保存在body.html
//命令行:phantomjs htmlbody.js 区域变电站
//在LeanCloud端注意下面两个依赖要特殊处理
//fonts-wqy 文泉驿点阵宋体、文泉驿微米黑，通常和 phantomjs 配合来显示中文。
//phantomjs 一个无 UI 的 WebKit 浏览器
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

page.settings.userAgent = 'Mozilla/5.13 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)';
console.log('The default user agent is ' + page.settings.userAgent);
//var url0 = 'https://baike.baidu.com/item/' + '%E5%8C%BA%E5%9F%9F%E5%8F%98%E7%94%B5%E7%AB%99'
//var url = 'https://baike.baidu.com/item/'
var cmd = 'phantomjs htmlbody.js url'

var system = require('system');
if (system.args.length === 1) {
    console.log('Try to pass some args when invoking this script!');
}
else {
    var sUrl =system.args[1];
    //console.log(url0)
    //console.log(encodeURIComponent(sUrl))
    //html_body(encodeURIComponent(sUrl))
    console.log(sUrl)
    html_body(sUrl)
}
