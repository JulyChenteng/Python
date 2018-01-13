import requests

def getHTMLText(url):
    try:
        #该网页禁止爬取，我们需要修改headers中user-agent字段，模拟浏览器对网页进行访问
        kv = {'user-agent':'Mozilla/5.0'}
        res = requests.get(url, headers=kv)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        print(res.request.headers)
        print(res.text[:1000])
    except:
        print("爬取失败")

if __name__ == "__main__":
    url = "https://www.amazon.cn/dp/B06X9RCD9S"
    getHTMLText(url)
