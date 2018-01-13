import random

secret = random.randint(1, 10)
temp = input("不妨猜一下小甲鱼现在心里想的是哪个数字：")
guess = int(temp)
while guess != secret :
      temp = input("哎呀，猜错了，请重新输入：")
      guess = int(temp)
      if guess == secret :
            print("卧槽，你是小甲鱼肚子里的蛔虫么！")
            print("猜中了也没有奖励！")
      else :
            if guess > secret :
                  print("嗯哼，大了大了！")
            else :
                  print("嗯哼，小了小了")

print("游戏结束，不玩啦！")
