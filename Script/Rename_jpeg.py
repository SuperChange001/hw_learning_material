# -*- coding: UTF-8 -*-
# 可以把桌面的所有IMG开头，jpeg结尾的文件，重命名为jpg。
import os


path = "/Users/andrew/Desktop/"
files = os.listdir(path)
s = []

for file in files:
    if (file[0:3] == "IMG") and (file[-2] == "e"):
        print("Rename Image: "+file)
        new_name = file[:-2]+"g"
        os.rename(path+file, path+new_name)