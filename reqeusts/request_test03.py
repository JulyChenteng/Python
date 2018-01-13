import requests

def getHTMLText(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        print(res.text[:1000])
    except:
        print("爬取失败")

if __name__ == "__main__":
    url = "https://item.jd.com/2967929.html"
    getHTMLText(url)
