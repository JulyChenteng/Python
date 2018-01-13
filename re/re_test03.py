import re

#re库默认的是贪婪匹配，即一个字串中有多个符合正则的匹配子串时，输出匹配最长的子串

match = re.search(r'PY.*N', 'PYANYYYANBBBN')
print(match.group(0))

#要想获得最小匹配，则需要对* + ? {m,n}进行扩展*? +? ?? {m, n}?
match = re.search(r'PY.*?N', 'PYANYYYANBBBN')
print(match.group(0))
