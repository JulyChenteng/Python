import re

'''
re库的两种使用方法：
      1. 函数式用法：一次性操作
      2. 面向对象用法：编译后多次操作
'''

#函数式用法
#在字符串中搜索，返回match对象
m = re.search(r'[1-9]\d{5}', ' BIT100081')
if m:
      print(m.group(0))

'''
#从字符串的开始位置开始匹配，返回match对象
match = re.match(r'[1-9]\d{5}', '100081 BIT') #BIT 100081
if match:
      print(match.group(0))
'''   

'''
#匹配源字符串中所有符合正则的字串，返回一个列表类型
ls = re.findall(r'[1-9]\d{5}', '100081 BIT100088')
print(ls)
'''

'''
#利用匹配到的字串对源字符串进行分割，返回列表类型
ls = re.split(r'[1-9]\d{5}', '100081BIT TSU100084HUS100055', maxsplit = 1)
print(ls)
'''

'''
#finditer函数返回一个迭代类型，每个类型是一个match对象
for m in re.finditer(r'[1-9]\d{5}', 'BIT100081 TSU100084'):
      if m:
            print(m.group(0))
'''

'''
#用zipcode替换匹配到的字符串，返回替换后的字符串
str = re.sub(r'[1-9]\d{5}', ':zipcode', 'BIT100081 TSU100084')
print(str)
'''

#面向对象式用法，先编译生成对象，然后利用对象操作
regex = re.compile(r'[1-9]\d{5}')
m = regex.search('BIT 100081')
print(m.group(0))

ls = regex.split('BIT100081 TSU100082')
print(ls)
