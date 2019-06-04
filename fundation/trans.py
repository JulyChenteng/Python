#本程序的作用是利用程序来模拟浏览器来访问服务器然后翻译相应的句子

import urllib.request
import urllib.parse
import json
import time

flag = 1

while(True):
    string = input('请您输入您要翻译的句子（退出请按#）：')

    if (string == '#'):
        break

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict2.index'

    #  第一种写法在调用前创建这个字典对象，第二种方法是调用add_header(key,value)方法
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2687.0 Safari/537.36'

    data = {}

    data['type'] = 'AUTO'
    data['i'] = string
    data['doctype'] = 'json'
    data['xmlVersion'] = '1.8'
    data['keyfrom'] = 'fanyi.web'
    data['ue'] = 'UTF-8'
    data['action'] = 'FY_BY_CLICKBUTTON'
    data['typoResult'] = 'true'

    data = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url,data,head)

    response = urllib.request.urlopen(req)

    html = response.read().decode('utf-8')

    target = json.loads(html)

    print("\n\n"+'翻译结果为：'+ target['translateResult'][0][0]['tgt']+"\n\n")

    # 休息五秒钟
   #time.sleep(5)
