# Thread practical example
import cv2 as cv
for i in dir(cv):
    if 'EVENT' in i:
        print(i)
# print("\033[37m f;sdjo \033[31m kweojfewf \033[37m")
# from threading import Thread
# import time
# import importlib
# print(time.time())
# importlib.reload(time)
# print(time.time())

# def x(y):
#     time.sleep(1)
#     print(y)
# for i in range(6):
#     x("hello")
# print("completed")
# thread=[]
# for i in range(6):
#     thread.append( Thread(target=x, args={"hello"}) )
# for i in thread:
#     i.start()
# for i in thread:
#     i.join()