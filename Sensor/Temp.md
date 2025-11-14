# 1. Temp

## 1.1. 参考资料
- [TI precision Labs](https://training.ti.com/ti-precision-labs-temperature-sensors-sensor-accuracy-error-and-repeatability?context=1139747-1139746-1137723-1139630-1137729)
- [TI的惠更斯电桥典型应用](https://www.ti.com/lit/an/sboa247/sboa247.pdf?ts=1599228118710&ref_url=https%253A%252F%252Fwww.ti.com%252Ftool%252FCIRCUIT060006)
- [Guide to Thermocouple](https://www.ti.com/lit/an/sbaa274/sbaa274.pdf?ts=1599364035241&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FADS124S08)
- [仪器放大器的电桥](https://www.ti.com/lit/an/sbaa245a/sbaa245a.pdf?ts=1599228447758&ref_url=https%253A%252F%252Fwww.ti.com%252Fdesign-resources%252Fdesign-tools-simulation%252Fanalog-circuits%252Fdata-converter-circuits.html)
- [只用ADC](https://www.ti.com/lit/an/sbaa329a/sbaa329a.pdf?ts=1599228501051&ref_url=https%253A%252F%252Fwww.ti.com%252Fdesign-resources%252Fdesign-tools-simulation%252Fanalog-circuits%252Fdata-converter-circuits.html)
## 1.2. 名词解释
- PTC：positive temp coefficient
- RTD：resistance Temp device
- IDAC：excite current source

## 1.3. 总结
1. 了解参数的意义：
	1. 准确度 accuracy：测量的值和准确的值之间的误差
	2. 精确度 precision：类似于分辨率
	3. 可重复性 repetition：这一次和下一次的误差
2. 几个概念：
	1. 测量误差和测量的非线性
	2. 校准和线性化
2. 测量温度的方式：
	1. 模拟：
		1. PTC NTC：
			1. 测温范围大，准确度高。但是模拟电路处理起来非常麻烦。
		2. 测量PN结的压降：IC内部采用的方式
	1. 数字：
		1. DS1850
			1. 测量的温度范围不大
			2. 准确度适中。线可以做的很长
1. 非理想参数：测量误差和测量非线性是两码事
	1. offset error：这个是笼统的说法
	2. gain error
	3. 器件存在的测量误差。
	3. 器件的非线性：PTC本身。电阻的误差值是分段的
	4. 器件的非重复性
	5. 放大电路引起的误差：Vos Ib Ios
	3. ADC：量化误差
	4. DCDC：PSRR引起的
2. 校准：校准和线性化也是不一样的
	1. 校准是使用的时候的校准
	2. 线性化是研发的时候使用的拟合方式
	3. 单点校准
	4. 双点校准
	5. 多点校准
3. 线性化：
	1. 电路线性化：并联一个校准电阻，牺牲分辨率，换来线性度
	2. 软件线性化：只针对非线性特性的优化
		2. 查表法
		3. 高次函数法

2. 看一下参考资料里TI推荐的不同类似的惠更斯电桥的驱动和采集方式。非常有借鉴意义


# 2. 基本概念
## 2.1. accuracy
- 温度和误差值：
	- ![Screenshot-2020-09-04 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599203737_20200904151320337_1775733360.jpg)
- 误差的来源：
	- 基准都有问题
	- 测试IC和外围电路导致的误差
	- 测试方式，测试点，测试环境导致的误差 
- 可重复性：
	- 和误差不一样。需要注意。
	- ![Screenshot-2020-09-04 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599203738_20200904151516127_1771394547.jpg)
## 2.2. PTC
1. 优点和缺点：
	1. ![Screenshot-2020-09-04 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599203734_20200904151019388_850488998.jpg)
	2. 阻值和温度不是线性的。需要软件校正
	3. ![Screenshot-2020-09-04 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599203736_20200904151119217_283773207.jpg)
1. 检测方式：惠更斯电桥
	1. ![Screenshot-2020-09-04 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599471601_20200904170413565_1438875652.jpg)

## 2.3. 数字传感器