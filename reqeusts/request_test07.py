import requests

url = "http://m.ip138.com/ip.asp?ip="

try:
    res = requests.get(url + '202.204.80.112')
    res.raise_for_status()
    res.encoding = res.apparent_encoding

    print(res.text[-500:])
except:
    print("爬取失败")
