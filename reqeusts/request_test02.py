import requests
import time

def getHTMLText(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding

        return res.text
    except:
        return "产生异常"

if __name__ == "__main__":
    url = "https://www.baidu.com"
    start_time = time.clock()
    print("test start: %f"%(start_time))

    for i in range(100):
        getHTMLText(url)

    end_time = time.clock()
    print("test start: %f"%(end_time))
    print("It takes %f seconds to finish the work."%(end_time-start_time))
