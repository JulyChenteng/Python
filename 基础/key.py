'''
本程序用来测试怎样绑定一个键盘事件在按下去对应的键以后在控制台输出对应的字符
'''
from tkinter import *

root =Tk()

def callback(event):
       '''
       print(event.char) #只能显示数字和字母
       '''
       print(event.keysym)

frame=Frame(root,width=200,height=200)
frame.bind("<Key>",callback) #绑定键盘事件
frame.focus_set() #用来获取焦点（窗口里面好多组件获得焦点才能说明键盘作用的组件）
frame.pack()

mainloop()
