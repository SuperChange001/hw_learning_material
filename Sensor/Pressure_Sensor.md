# 1. Pressure_Sensor
先做一个比较简单的总结吧。等后续再做系统级的梳理。电桥那么简单和普通的应用，但是里面也有很多的文章。如果不考虑精度和准确度，其实可以随便做。但是想要做好，还是要对OPA和ADC有了解。这个才是Sensor的基础
## 1.1. 参考资料
- [ADC噪声分析](https://www.ti.com/lit/wp/slyy192/slyy192.pdf?ts=1599364042567&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FADS124S08)
- [Guide to RTD](https://www.ti.com/lit/an/sbaa275/sbaa275.pdf?ts=1599364038801&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FADS124S08)

## 1.2. 名词解释
- IDAC：excite current source
- PGA: programmable gain amplifer


## 1.3. 总结
1. 要关注在以下几个点：
	1. 电桥的结构：惠更斯电桥，还是分压电阻，还是单电阻电流源
	2. 放大电路的结构：仪放，自己搭的2运放仪放，就是普通运放，还是不需要运放
	3. ADC的结构：类型delta-sigma还是SAR。带不带PGA。是不是要阻抗匹配。运放带不带IDAC
	3. 运放和仪放的接口电路：是否要做电荷水库，是否要做抗混叠
	4. Vref的选择：使用内部参考还是外部的。使用外部的是否需要高带宽高电流的buffer




# 2. 电路
1. 参考电路1：
	2. ![Screenshot-2020-09-06 AM11](https://gitee.com/AndrewChu/markdown/raw/master/1599365855_20200906121029387_191336130.jpg)
	3. 使用IDAC电流源。
		1. 可以减少电压源的波动带来的噪声
		2. 可以忽略流到PGA里面的分流。因为阻抗相差很大
	1. 参考电压：
		1. 这里是高边输入，当然也可以是低边输入
		2. 参考电压和输入电压也是同源的，可以把共模干扰去掉
		3. 注意，使用共模和差模滤波电容。差模的截止频率要小于共模的截止频率10倍。因为共模滤波会带来不对称性，导致共模变成差模，所以要用差模把这部分的高频差模干扰滤波。
	1. 输入信号PIN，AIN0：
		1. 同样需要共模和差模电容
		2. 注意输入信号的共模电压不要超过PGA的规定
		3. 注意，要计算一下阻抗匹配是不是问题。
1. 参考电路2：
	1. ![Screenshot-2020-09-06 AM11](https://gitee.com/AndrewChu/markdown/raw/master/1599365856_20200906121618570_335438584.jpg)
	2. 这个电路容易给人误解。以为这个ADC是普通的ADC，那就会有问题。要带PGA的，不然就会导致电容充电的问题。

