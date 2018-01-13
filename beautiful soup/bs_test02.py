import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
      try:
            res = requests.get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res.text
      except:
            print("爬取失败")

if __name__ == "__main__":
      url = "http://www.liaoxuefeng.com/"
      demo = getHTMLText(url)

      soup = BeautifulSoup(demo, "html.parser")
      #print(soup.head.contents)  #返回的是一个元组
      #print(soup.body.contents)
      len(soup.head.contents) #返回head标签子节点的个数

      #标签树的下行遍历——从上往下遍历
      '''
      for child in soup.head.children:  #遍历儿子节点
            print(child)
      '''

      for child in soup.head.descendants: #遍历子孙节点
            print(child)
