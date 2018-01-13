#获取淘宝搜索页面的信息，提取其中的商品名称和价格
import re
import requests

def getHTMLText(url):
      try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding

            return r.text
      except:
            return ""

def parsePage(ilt, html):
      try:
            plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
            tlt = re.findall(r'\"raw_title\"\:\".*?\"', html) #对双引号的约束—最小匹配

            for i in range(len(plt)):
                  price = eval(plt[i].split(':')[1]) #eval函数将字符串外面的双引号的单引号去除
                  title = eval(tlt[i].split(':')[1])
                  ilt.append([price, title])
      except:
            print("erro in parsePage")

def printGoodsList(ilt):
      tplt = "{:4}\t{:8}\t{:30}"
      print(tplt.format("序号", "价格", "商品名称"))
      
      count = 0
      for info in ilt:
            count = count + 1;
            print(tplt.format(count, info[0], info[1]))

def main():
      goods = "书包"
      depth = 2
      start_url = "https://s.taobao.com/search?q=" + goods
      infolist = []

      for i in range(depth):
            try:
                  url = start_url + '&s=' + str(44*i)
                  html = getHTMLText(url)
                  parsePage(infolist, html)
            except:
                  continue
                  
            printGoodsList(infolist)

main()
