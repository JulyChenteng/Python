import requests
from bs4 import BeautifulSoup

res = requests.get("http://www.liaoxuefeng.com/")
demo = res.text

soup = BeautifulSoup(demo, "html.parser")
print(soup.prettify())  #prettify 粉饰，美化

