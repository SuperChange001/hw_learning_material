# -*- coding: UTF-8 -*-
# 可以把桌面的所有IMG开头，jpeg结尾的文件，重命名为jpg。
import os
import cv2


path = "/Users/andrew/Desktop/"
files = os.listdir(path)
s = []
MAX_SIZE = 2000

for file in files:
    if file[0:3] == "IMG":
        img = cv2.imread(path+file, cv2.IMREAD_UNCHANGED)
        w = img.shape[1]
        h = img.shape[0]

        if (w > MAX_SIZE) or(h > MAX_SIZE):
            print("Resize: "+file+str(img.shape))

            while (w > MAX_SIZE) or(h > MAX_SIZE):
                w = w/2
                h = h/2
            resized = cv2.resize(img, (int(w), int(h)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(path+file, resized)


