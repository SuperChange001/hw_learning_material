#!/usr/bin/python3
# 使用方式
# 1. 前提：安装了python3，下载了script，使用shell，已经进入了脚本目录
# 2. 例子：`./cornerFreqenceCalculator.py 2 k 3.3 p`
# 3. 参数1：script的名字。 参数2：电阻值。参数3：电阻的单位。参数4：电容值。参数5：电容单位。

import sys
pi = 3.14159
dataLen = len(sys.argv)-1
data = sys.argv[1:]

if dataLen != 4:
    print("参数过多或过少！")
else: 
    r = float(data[0])
    c = float(data[2])
    if data[1] == 'k':
        r = r*1000
    else:
        r = r*1000*1000
    
    if data[3]== 'u':
        c = c/1000/1000
    elif data[3] == 'n':
        c = c/1000/1000/1000
    else:
        c = c/1000/1000/1000/1000

    res = 1.0/(2*pi*r*c)
    print("Fc is: {:.3} KHZ".format( res /1000))
    print("Fc is: {:.3} MHZ".format( res /1000 /1000))
    print("Fc is: {:.3} GHZ".format( res /1000/1000/1000))
    
