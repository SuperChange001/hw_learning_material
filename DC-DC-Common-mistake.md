# 1. ACDC-DCDC-Common-mistake
## 1.1. 前提
阅读之前的`基本元件`,`DCDC basics`章节

## 1.2. 名词解释
1. snubber：变压器发射电压的吸收电路
2. UVLO：under voltage 

## 1.3. 参考文档
- [所有笔记的链接](https://gitee.com/AndrewChu/hardware-design)
- [common mistakes in DCDC](https://training.ti.com/common-mistakes-dcdc-buck-converters-part-selection?context=1127730-1135482-1139329-1135476)
- [Common Mistakes in Flyback Power Supplies and How to Fix Them](https://training.ti.com/common-mistakes-flyback-power-supplies-and-how-fix-them-audible-noise-and-input-capacitors?context=1127730-1139938-1139945-1139886)
- ADI-电源大师课

## 1.4. 总结：
看看TI的技术支持，给出的ACDC, DCDC设计的常见错误，这个对我们自己在设计电源的时候还是有一定的参考意义的！   
只要是有负反馈的网络，就要考虑变成正反馈的可能性，就要考虑环路稳定性。   
1. DCDC:
	1. 比ACDC简单多了。更多的问题在器件选型上。选择合适的电感，输入电容，输出电容，二极管或者MOSFET，最终达到设计的纹波和暂态响应。
2. ACDC:
	1. 我只会去学习flyback的ACDC,也称为反激式电源。特点是简单，源边储存能量，副边在另外一半周期消耗能量，适合小功率75W一下。
	2. 其他复杂的拓扑，没有精力去了解了。
	2. 问题复杂多了，主要是因为多了变压器和MOSFET控制IC，这个控制IC还需要上电启动配合。
	2. 问题更多的是在对flyback架构的理解和对控制IC内部各种保护机制的理解。
	3. 


# 2. DCDC 
## 2.1. Issue1：minimal on time
- DCDC的MOSFET有个参数是最小导通时间。意味着MOSFET只要一导通，至少需要维持那么长时间的导通
- 概念是和接触器的最小导通负载电流类似。也是很容易被忽略的一个参数。就是当负载电流小于一个值的时候，接触器就算闭合了，也不会导通。
- 最小导通时间，ADI智库里也介绍了
- 这个限制，意味着DCDC的D不能太小，意味着Vo太小的时候，会有问题
- 公式：Vout > fsw*Vin*t_on_min

## 2.2. Issue2: Thermal due to efficiency
- MOSFET的损耗会影响开关电源的发热
- 其实我觉得他的这个例子不好。因为DCDC的效率，是由多方面决定的
	- IC的工作电流，给MOSFET的G充电的功耗
	- MOSFET的导通损耗：Rdson
	- MOSFET的开关损耗，开和关都有
	- 续流D的损耗，包括反向漏电流和正向Vf
- 这里例子，他就拿出了Rdson，容易给人误导
- 当然，如果fsw选的很小，Rdson容易变成主导因素
- 选一个Rdson小的MOSFET，可能比较贵，同时Qsw也会变差。

## 2.3. Issue3: Poor inductor
- 选错了电感，让电感的电流进入了饱和状态，那么电感就会失去电感的特性
- 纹波电流，选择负载电流的30%，我们就可以得到电感上的最大电流
- 最大电流，要小于电感的铜电流，小于磁电流。就是小于Irms，小于Isat


## 2.4. Issue4：Insufficient input Cap
- 输入电容小了，当load突然变大，母线的电压就会下降，Vo的电压也会变小，而且会有一定的震荡波形
- 这个波形可能和环路稳定性不好，导致的震荡有点类似。差别在于这种情况，输入电压也波动了。
- 输入电容的选择：
	- 其实最关心的是Irms，这个计算公式和D有关，D=0.5的时候最大，详细看DCDC basics
	- 同时也要关心容量。C=QV=∫Idt*V，意味着我们要知道I，和恢复时间，波动的V，就知道了C的大小

## 2.5. Issue5：Poor Compensation
- 其实就是环路稳定性不好。幅频裕度和相位裕度不够
- 他给出的现象是DCDC的D在不停跳变
- 其实环路稳定性不好，最明显的问题会在：时域波形的过冲很大，频域波形的Q很大。


## 2.6. Issue6: Soft start
- 软启动的设置不对，当后端负载很大的时候，就会过流保护

## 2.7. Issue7： Poor layout
- 没搞清楚电压突变，电流突变的环路，随意地摆放电容，会导致Vo的波形震荡
- 其实也要从环路稳定性来分析：电容放的远了，会引入走线电感。一方面削弱了电容的作用，另一方面传函也可能改变了。最终导致环路稳定性不够

## 2.8. Issue8：Poor Thermal
- 例子里是地平面跨分割了，破坏了电流的环路，走线的电阻增大，最终发热

## 2.9. Issue9：Wrong voltage measurement
- 测量电压：
	- 要开启20M带宽抑制
	- 拿掉地环
	- 用1倍探头


## 2.10. Issue10：Wrong pode measurement
- 加入的AC电压太大：
	- 改变了直流工作点，在高频不停地波动
- 加入的AC电压太小
	- 测试信号，被噪声淹没，在低频的时候不停波动



# 3. ACDC
## 3.1. 总结
1. FLYBACK的基本架构
	- 整流桥+π型滤波+flyback驱动和snubber吸收发射电压+PWM IC+输出电压监控+IC上电供电电路 
	- 关键点：
		- 反激式电源，源边导通副边截止，源边截止副边导通。所以要考虑磁饱和的问题
		- snubber电路吸收Vor，Vor是站在输入的电压上的，所以如果用TVS，那要考虑开启电压，也要考虑MOS的击穿电压。效率考虑
		- 只要是使用了负反馈的电路，都要考虑环路稳定性。因为怕有延时单元，把负反馈变成正反馈了。
	- ![Screenshot-2020-09-02 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599008000_20200902085027085_1098337220.jpg)
2. 常见的问题点：
	- 启动的问题：供电不够，供电跌落太大需要加大稳压电容
	- 关断问题：过流保护，过压保护。具体是要看手册的
	- 效率和发热：变压器的铜损和磁损。MOSFET的开关损耗。Snubber吸收带来的损耗
	- 待机功耗：不要用固定PWM的IC，其他外围电路也可以适当设计
	- Layout问题：回流路径，电流跨分割，走线的寄生电感
	- 稳定性问题：怎么用好二型补偿
	- 发声问题：电感震动
	- 大电容的问题：怎么选型，Irms和容量都要考虑，寿命考虑。
	- ![Screenshot-2020-09-02 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599008003_20200902085312913_1824146790.jpg)

## 3.2. 电源不能启动
1. 启动负载太大：考虑到效率问题，启动电路的R是很大的，所以带不动大负载。要把大负载从PWM IC启动电路的负载去掉
2. 上电一会就掉电了：输入电压的UVLO起作用，电容太小了。要考虑多大的容值，才能稳定住一定的电压跌落

## 3.3. 电源启动一会就掉电了
1. 输出的过压保护：分压电阻没选好
2. 过流保护：会测量MOS上的电流，但是这个电流会有spike，需要RC滤波。这个滤波频率要大于10倍的开关频率，不然会有问题。
3. 常见的几种保护机制：
	1. ![Screenshot-2020-09-02 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599010897_20200902091910689_1892441065.jpg)


## 3.4. 温度特性差
1. 这个问题很典型的表示了光耦应该怎么用：一定要考虑CTR，同时也要清楚IC内部的结构，里面的负载多大
2. 简单的说，就是CTR受到温度的影响很大，原电路就没有留够CTR，导致温度一上去，那就问题更大了。
3. ![Screenshot-2020-09-02 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599010898_20200902092501494_256845202.jpg)

## 3.5. 发热：
1. MOSFET是个大热源。先看是不是正常工作了，因为MOSFET有个体二极管，有时候不正常工作，还是能从这个二极管续流。
2. 然后计算一下是开关损耗大，还是导通损耗大。开关损耗是要考虑米勒效应的。
3. 门极驱动的常识：
	1. 要串联一个电阻，作为限流。不然电流太大损坏IC
	2. 电阻可以减少电压突变，减少EMI
	2. 要并联一个反向二极管，让电容快速放电，避免影响死区
	3. ![Screenshot-2020-09-02 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599010899_20200902092955592_1677624921.jpg)
1. snubber也就是clamp发热：
	1. 因为吸收电压的阈值没选对。要考虑输入电压的
	2. ![Screenshot-2020-09-02 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599010900_20200902093135156_718797541.jpg)
2. 其他内容不想做了……晚点吧