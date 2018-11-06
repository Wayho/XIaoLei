//专门用于模拟浏览器的运行JS生成的页面HTML,只取<body>部分,保存在body.html
//命令行:phantomjs htmlbody.js 区域变电站
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