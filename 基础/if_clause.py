#此程序主要是练习py中的if和while语句，熟悉下py程序的编写流程

print("Type integer, each followed by Enter, or just Enter to finish")

total = 0
count = 0

'''
while True:
    line = input("integer : ")
    if line:
        try:
            number = int(line)
        except ValueError as err:
            print(err)
            continue
        total += number
        count += 1
    else:
        break
'''

#加入EOFError异常处理以便支持文件重定向
while True:
    try:
        line = input("integer : ")
        if line:
            number = int(line)
            total += number
            count += 1
            
    except ValueError as err:
        print(err)
        continue
    except EOFError:
        break

if count:
    print("count = ", count, ", total = ", total, ", avg = ", total / count)
