import codecs
import chardet

poem = '''\
    Programming is fun When the work is
done if you wanna make your work also
fun:
    use Python!
    你好！
'''

'''
 'w'删除已有内容重新写入
 'r'读取文件
 'a'在已有内容后面追加新内容
'''
'''
f = open('./file/poem.txt', 'w')
f.write(poem); # write text to file
f.close()      # close the file

f = open('./file/poem.txt') #默认为'r'模式

while True:
    line = f.readline()
    if len(line) == 0:  #空行表示读取结束
        break
    print(line, end=" ")
    #print内容后面会默认增加一个\n
    #这里end禁止结尾增加\n，改为增加“”

f.close() #close the file
'''

#with语句
#写入文件
'''
with open('poem.txt', 'w') as f:
    f.write(poem)
'''

#读取文件
'''
with open('./file/TIS', 'r', encoding='UTF-8') as f:
    while True:
        line = f.readline()
        if len(line) == 0:
            break

        print(line, end = "")
 '''       
 
with codecs.open("./file/windows","rb") as f:
    data = f.read() 
    print(type(data)) 
    encodeInfo = chardet.detect(data) 
    print(encodeInfo["encoding"])
    print(data.decode(encodeInfo["encoding"]))
