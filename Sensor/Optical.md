# 1. Optical


## 1.1. 参考文档
1. [光谱](https://training.ti.com/13-ti-precision-labs-ambient-light-sensors-how-human-eye-sees-light?context=1139747-1139746-1140283-1140286)
2. [光电池电路](https://www.ti.com/lit/an/sboa220a/sboa220a.pdf?ts=1599450862236&ref_url=https%253A%252F%252Fwww.ti.com%252Fdesign-resources%252Fdesign-tools-simulation%252Fanalog-circuits%252Famplifier-circuits.html)


## 1.2. 名词解释
- LED：lighting emission diode


## 1.3. 总结
1. 光学的内容主要包括两块：
	2. 光谱相关的内容
	3. 光电池的微弱信号处理
1. 光谱的知识：
	1. 可见光只是光谱里非常小的一段
	2. 紫外---可见光--近红外--远红外。波长越来越大，频率越来越低。波长短的光，对于人体杀伤力很大。
	3. 紫外杀毒，红外加热。
	3. 有温度的物体，都会发射热辐射。辐射的波长和颜色有关系。所以我们看到热的物体是红色或者黄色的。
		1. 人体的热辐射，因为温度低，所以在远红外的。所以人体运动传感器，可以是工作在远红外的被动式传感器
		2. 摄像头工作在近红外，没有热辐射的效果，只能自己主动发出近红外光，依靠物体反射来探明。
1. 光源的知识：
	1. 白炽灯，光谱非常的宽，而且能量集中在远红外。所以发热非常大，发光效率很低
	2. LED，发出的光是很窄的频谱，集中在可见光，所以效率很高。发出的光是一种颜色的。发出白光需要多种LED混合
	1. 太阳光其实是蓝光强，但是大气层有反射吸收作用，使得光谱很平均。
1. 光强的测量：
	1. 白炽灯以前标注的是W，现在标注的Lum。单位距离，单位面积的光强是Lux。
	2. Lux是按照人眼的接收敏感度进行加权系数的。如果光强是w单位的，那就是没有加权系数的。
	3. 很多时候，我们关注的是人眼接收的加权系数的，因为是为了人来调节环境光
	4. 不同的光源，在可见光和IR区域的分布是不一样的。所以可以分别测量这两个值，进行光源的判断。

# 2. 光谱
## 2.1. 光是电磁场
1. 光是一种电磁场，那么他的传播方向和B/E的关系。和波长，频率的关系。
	1. ![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372622_20200906135947206_1840466056.jpg)


## 2.2. 波长和颜色的关系
1. 波长和颜色的关系
	1. ![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372624_20200906140011308_500153379.jpg)
2. 不同的光传感器
	1. ![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372626_20200906140042710_185176582.jpg)
1. 不同的光源：
	1. 热辐射：![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372628_20200906140920777_1943655216.jpg)
	2. 太阳：![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372629_20200906140950259_1549918193.jpg)
	3. 白炽灯：![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372630_20200906140959958_1283569644.jpg)
	4. LED：![Screenshot-2020-09-06 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599372631_20200906141018774_889883074.jpg)



# 3. 感光IC的选择
1. 感光IC，可能是按照人眼对光谱的权重系数校准的，所以适合测试人眼判断的光强弱。
	1. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375763_20200906145949296_1816076660.jpg)
1. 使用积分球，可以测试光源的LUM
	1. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375765_20200906150016644_1739847897.jpg)


2. 光电池。这个是最常用的感光元件
	1. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375766_20200906150051911_1681556971.jpg)
	2. 简化使用，有模拟式的，也有数字式的
		1. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375768_20200906150121894_1850613671.jpg)
		2. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375773_20200906150130626_288811250.jpg)
	1. 如果光谱和我们选的IC的分布不一致。那么就可以加滤波器，把部分的光给滤除了。达到一定的区分光谱的效果。低成本的光谱仪就是加filter
		1. ![Screenshot-2020-09-06 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599375774_20200906150236608_1309536151.jpg)


# 4. 微弱信号处理。
参考TI的光电池处理电路。其实最重要的几个点：
1. 截止频率的计算。要理解Cf和Rf是组成反馈网络的了高通滤波，但是对运放整体是低通。所以截止频率由这两个参数决定
2. 为什么要计算GBW。其实是在规定的fc位置，计算F。因为引入了寄生的电容之后，在f=200khz的时候，计算运放的反馈系数F，其实是有一个值的。具体的请回顾MF法计算运放的噪声增益。
3. 同时，这个图省略了加入JFET的电路，加入JFET可以隔离运放的偏置电流，因为是MOS的运放，其实这个值已经非常小了。
4. 查看了运放的手册，说明了运放驱动大电容，会造成不稳定。因为和运放的输出电阻组成了一个极点，造成相位裕度不够。解决方式就是加入Riso或者ESR很大的电容，可以补偿回一个零点。