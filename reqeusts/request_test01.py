import requests

def getHTMLText(url):
    try:
        res = requests.get(url, timeout = 30)
        res.raise_for_status() #如果状态不是200， 引发HTTPError异常
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return "产生异常"

if __name__ == "__main__":
    url = "https://www.baidu.com"
    print(getHTMLText(url))
