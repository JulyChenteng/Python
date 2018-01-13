import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
      try:
            res = requests.get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res.text
      except:
            print("爬取失败!")

if __name__ == "__main__":
      url = "http://www.liaoxuefeng.com/"
      demo = getHTMLText(url)

      soup = BeautifulSoup(demo, "html.parser")
      print(soup.head.prettify())  #prettify()函数格式化html内容
