import re

m = re.search(r'[1-9]\d{5}', 'BIT100081 TSU100084')

print(m.string)   #string属性代表待匹配的字符串'BIT100081 TSU100084'
print(m.re)       #re属性表示匹配使用的正则表达式
print(m.pos)      #正则表达式搜索文本的开始位置
print(m.endpos)   #正则表达式搜索文本的结束位置

print(m.group(0)) #group(0方法获得匹配后的字符串
print(m.start())  #匹配字符串在原始字符串的开始位置
print(m.end())    #匹配字符串在原始字符串的结束位置
print(m.span())   #返回(start(), end())
