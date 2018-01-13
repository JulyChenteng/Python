import requests

keyword = "python"
try:
    kv = {'wd':keyword}#百度搜索的关键字参数为'wd' 
    res = requests.get("https://www.baidu.com", params=kv)
    print(res.request.url)
    res.raise_for_status()
    print(len(res.text))
except:
    print("爬取失败")

    
