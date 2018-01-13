
import requests
import os

url = "http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg"
root = "D://notes/Python笔记//pics//"
path = root + url.split('/')[-1]

try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        kv = {'user-agent':'Mozilla/11.0'} 
        res = requests.get(url, headers=kv)
        print(res.request.headers)
        with open(path, 'wb') as f:
            f.write(res.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")
except:
    print("爬取失败")
