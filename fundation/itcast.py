import requests
res = requests.get("http:\\c.itcast.cn")
savefile = open("itcast.html", "w")
savefile.write(res.content)
savefile.close()
