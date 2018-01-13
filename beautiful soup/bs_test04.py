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

      #标签树的平行遍历——属于同一个父节点
      for sibling in soup.meta.next_siblings:  #遍历该节点之后的平行节点
            print(sibling.name)

      for sibling in soup.meta.previous_siblings: #遍历该节点之前的平行节点
            print(sibling.name)
   
