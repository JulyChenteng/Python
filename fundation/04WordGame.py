temp = input("不妨猜一下我心里想的是哪个数字：")
guess = int(temp)
while guess != 8 :
      temp = input("哎呀，错了，请重新输入：")
      guess = int(temp)

      if guess == 8 :
            print("卧槽，你是小甲鱼肚子里的蛔虫！")
            print("答对了也没有什么奖励")
      else :
            if guess > 8 :
                  print("嗯哼，大了，大了!")
            else :
                  print("嗯哼，小了，小了!")


print("游戏结束！")

      
