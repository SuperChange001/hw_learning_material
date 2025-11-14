# 1. Hall_Effect

## 1.1. 参考资料
- [TI Precision Labs](https://training.ti.com/ti-precision-labs-magnetic-sensors-introduction-hall-effect-position-sensing?context=1139747-1139746-1137749-1139633-1137740)

## 1.2. 名词解释
- Hall Effect：如果一个导体有电流流过，此时叠加了一个电场，那么就会在导体上感应出有方向的电压差。

## 1.3. 总结
1. 知道Hall器件的种类，根据种类来使用。
2. 知道怎么正确地摆放霍尔器件。


# 2. Hall的器件

## 2.1. 三种Hall器件
1. Hall的器件:
	1. 单纯的霍尔效应器件：
		1. 自己拿运放放大把。所以很麻烦，很少用。可靠性，保护性都不强
	2. 霍尔效应的IC
		1. 霍尔锁存器：分SN的
			1. ![Screenshot-2020-09-04 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599229352_20200904221934708_1958575186.jpg)
		2. 霍尔开关：指示SN，或者磁场有没有
			1. ![Screenshot-2020-09-04 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599229353_20200904222002512_946813139.jpg)
		3. 霍尔模拟输出：
			1. ![Screenshot-2020-09-04 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599229353_20200904222057812_234516225.jpg)

2. 怎么正确地摆放Hall IC：和磁力线要垂直就对了。
	1. ![Screenshot-2020-09-04 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599229354_20200904222221500_1147699691.jpg)

## 2.2. Hall的磁滞效应
为了使输出的信号更加可靠，所以以上的三种类型器件都是有磁滞回线的
1. ![Screenshot-2020-09-04 PM11](https://gitee.com/AndrewChu/markdown/raw/master/1599361018_20200905183406377_1173260500.jpg)


# 3. Hall的使用

## 3.1. poles和Hall的数量
1. 极对数Poles：N
	1. 就是是有多少对的磁极在一个磁铁上
	2. 放的越多，转一圈，Hall的输出波形越多
2. Hall的数量：M
	1. 就是放了多少个Hall器件。
	2. 放的越多，可以判断转的方向和角度
3. ![Screenshot-2020-09-04 PM11](https://gitee.com/AndrewChu/markdown/raw/master/1599361019_20200905183521143_260287434.jpg)
4. ![Screenshot-2020-09-05 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599361020_20200905183648325_925325892.jpg)

## 3.2. 接近距离判断
1. 接近距离判断：有触发距离和不触发距离。
	1. 要根据距离，选定合适的磁铁体积大小
	2. ![Screenshot-2020-09-05 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599361021_20200905183747573_1632230420.jpg)
	3. ![Screenshot-2020-09-05 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599361022_20200905183800992_860355836.jpg)
1. 提高SNR
	1. 要么提高输出的信号
	2. 要么减少信号的噪声。如噪声的带宽和噪声的值。降低所有信号的带宽，降低器件的铭感度
	3. ![Screenshot-2020-09-05 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599361023_20200905183952556_1424119172.jpg)


## 3.3. 计算角度
1. 因为有各种distortion，所以不是简单的arcsin就能计算出来。当失真大的时候，就需要使用查找表了。




# 4. 电流采样
1. 使用Hall器件和电流shunt电阻的差别：
	1. ![IMG_0933](https://gitee.com/AndrewChu/markdown/raw/master/1599361026_20200906105515745_1371568018.jpg)
1. 电流夹的原理
	1. ![IMG_0934](https://gitee.com/AndrewChu/markdown/raw/master/1599361027_20200906105527144_854019600.jpg)
	2. 安培定理：
	3. ![IMG_0935](https://gitee.com/AndrewChu/markdown/raw/master/1599361028_20200906105535867_440688106.jpg)
## 4.1. 几种磁性的电流采样IC
1. 电流夹
2. 临界检测
3. 电流直接流入IC
	2. ![IMG_0937](https://gitee.com/AndrewChu/markdown/raw/master/1599361029_20200906105604032_2048688669.jpg)
3. 流入IC，实行电流检测的原理。
	1. ![IMG_0939](https://gitee.com/AndrewChu/markdown/raw/master/1599361030_20200906105613018_659117986.jpg)
	2. 是有隔离的。最后输出
