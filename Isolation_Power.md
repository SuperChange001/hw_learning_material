# 1. _Isolation_Power

## 1.1. 参考资料
- [所有笔记的链接](https://gitee.com/AndrewChu/hardware-design)  
- [TI Precision Labs ](https://training.ti.com/ti-precision-labs-isolation-what-galvanic-isolation?context=1139747-1135015-1139269-1135013)

## 1.2. 名词解释
- GPD： ground potential difference
- CTI：电起痕指数。和爬电距离有关。和材质有关
- CMTI：common mode transient immunity

## 1.3. 总结：
1. 5种隔离程度：
	1. functional isolation：功能绝缘。没有考虑隔离
	2. basic isolation：基本绝缘。满足基本的隔离
	3. supplement isolation：附加绝缘。第二种保护的绝缘
	3. double isolation：双重绝缘。basic+supplement
	4. reinforce isolation：增强绝缘。基本隔离的指标提高到2倍或者double isolation
	5. ![Screenshot-2020-09-03 PM7](https://gitee.com/AndrewChu/markdown/raw/master/1599135391_20200903200349666_651362957.jpg)
2. 爬电距离和电气间隙：
	1. 爬电距离：沿着表面爬
	2. 电气间隙：击穿空气的距离
	3. 这两个参数都和很多参数有关系，下面会详细列出来怎么确定这两个距离。同时也要和安全组的人确认参数是否一致。不然设计都是白做的。
3. 隔离的作用：
	3. 功能安全，防止人触电。隔离开了GND回路
	1. GPD：抑制地弹
	2. 抑制EFT等直接加在线缆上的干扰
1. 隔离的种类：
	1. 光耦：有延时，寿命不长，速率低，功耗高。考虑CTR长时间会变，温漂也会变。
	2. 电感隔离：
	3. 电容隔离：都需要使用开关调制。隔离度高。
		1. OOK：信号被调制到载波上，穿过隔离带。功耗大。速率快，CMTI好。失效安全
		2. edge base：检测的是输入信号的沿。失效模式需要考虑
1. 隔离的器件：
	1. 数字隔离器件
	2. 隔离的运放和ADC
	3. 隔离的门驱动
1. CMTI：就是源端加了共模干扰，输出不会输出错误的码。越高越好。代表IC越稳定



- 部件和产品级的功能安全认证：
	- ![Screenshot-2020-08-31 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598927772_20200831161157455_2068621287.jpg)

# 2. 基础
1. 需要知道的知识点：
	1. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135381_20200903134834994_178482398.jpg)
	2. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135382_20200903134850887_834756059.jpg)
	3. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135383_20200903134958748_1254664350.jpg)
	4. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135386_20200903135102196_1389741357.jpg)
	5. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135386_20200903135110759_1562344674.jpg)
1. 隔离输入和数字隔离：
	1. 功能类似，但是输入范围更大，同时只要输出供电，类似于光耦
		1. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135387_20200903135158762_1803882762.jpg)
		2. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135388_20200903135314685_1644405694.jpg)
	1. 和光耦的区别：
		1. ![Screenshot-2020-09-03 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599135390_20200903135326324_1049628116.jpg)


# 3. 认证和标准
## 3.1. 标准
## 3.2. creepage和clearance
1. 两者的差别
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135392_20200903201237260_821017383.jpg)
	2. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135392_20200903201313155_52388057.jpg)
1. creepage的决定
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135393_20200903201409824_546026023.jpg)
	2. 电起痕参数：和材质有关系：
		1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135394_20200903201456574_1036346305.jpg)
	1. 海拔修正因子和工作电压
		1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135395_20200903201538989_1087977947.jpg)
1. 怎么样满足creepage
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135395_20200903201612774_1978591610.jpg)
1. 额外的：CMTI
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599135826_20200903202208768_2038240986.jpg)
# 4. EMC和测试
1. 不同产品族和不同测试项的标准
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599136373_20200903203017004_259161229.jpg)
1. 测试的内容：
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142132_20200903214203407_1999696978.jpg)
1. EMC优化的方向
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599136374_20200903203045620_1868940525.jpg)
1. CISPR11 分的EMI四种类别
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599136375_20200903203159268_748034204.jpg)
1. EMS的瞬态三兄弟
	1. ![Screenshot-2020-09-03 PM8](https://gitee.com/AndrewChu/markdown/raw/master/1599136375_20200903203240598_747007290.jpg)


## 4.1. RE
1. 标准一般以准峰值
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142133_20200903214301117_1646310070.jpg)

## 4.2. CE
1. 注意用LISN采集信号，和隔离电网的干扰
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142133_20200903214411762_1701672550.jpg)

## 4.3. CS
1. CDN:电容耦合网络，把测试器产生的干扰耦合到信号线或者电源线上
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142134_20200903214527456_1176847567.jpg)
## 4.4. EFT
1. 也需要CDN。注意不同产品族，对要做EFT的线缆要求不一样
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142135_20200903214605507_1843271809.jpg)


## 4.5. ESD
1. 要明白器件级别的是人体模型HBM和器件模型CDM，这个能量小很多。IEC61000是系统级别。这个能量会比器件级别大很多。
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142136_20200903214707471_791616196.jpg)


# 5. 隔离器件的PCB EMC技巧
1. 通用技巧：减少EMI
	1. ![Screenshot-2020-09-03 PM9](https://gitee.com/AndrewChu/markdown/raw/master/1599142136_20200903220633462_1563666784.jpg)
1. PCB layout的技巧
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599142137_20200903220713343_1644791400.jpg)
	2. 边缘守护：孔的距离要计算
	3. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599142137_20200903220736662_1281091776.jpg)
	4. 缝合电容：给共模电流一个回路，可以使压差变小，发射变小。和变压器的寄生电容处理是一致的。
	5. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599142138_20200903220845196_146986544.jpg)

# 6. 隔离电源的设计
1. 隔离电源的种类：
	1. 变压器
	2. 变压器+LDO
	3. 隔离电源集成到隔离IC上
	4. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143124_20200903222310935_1710625093.jpg)
	5. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143125_20200903222345019_1236977866.jpg)
2. 集成的隔离电源：
	1. 好处：简单，空间少
	2. 坏处：牺牲了效率，f更高EMI更高
	3. 更加要注意layout的技巧
	4. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143126_20200903222444908_917591361.jpg)


# 7. 隔离运放和ADC
1. 没什么好讲的，就是隔离的运放和ADC。要不然这种模拟信号还是很难隔离处理的。
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143975_20200903223909915_1663156032.jpg)
	2. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143976_20200903223914330_1043849805.jpg)
	3. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599143977_20200903223921015_1656819740.jpg)

# 8. 隔离驱动
1. 功率MOS和一般MOS的参数差异
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599144534_20200903224649823_696589896.jpg)
	1. 开关损耗，先给Cg充电，然后给Cgd充电
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599144535_20200903224718780_1496671159.jpg)
1. 非隔离半桥驱动：主要是Iq很小，所以延时很大
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599144536_20200903224736914_1119637294.jpg)	
1. 隔离的驱动：使用更加灵活，耐GPD也很强。
	1. ![Screenshot-2020-09-03 PM10](https://gitee.com/AndrewChu/markdown/raw/master/1599144537_20200903224822189_1287446028.jpg)

## 8.1. 功率级隔离
1. 普通H桥驱动，变压器隔离，电容隔离驱动的比较
	1. 不耐高压，空间和认证麻烦
	2. ![Screenshot-2020-09-04 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599181339_20200904085649545_1383044823.jpg)
1. 关键参数：
	1. 传输延时：从输入的阈值触发，到有10%输出的时间。
	2. time skew：不同器件之间的传输延时
	3. pule duration distortion：上升和下降的传输延时的差
	4. CMTI：变化率超过多少的输入信号，会影响到输出
	5. ![Screenshot-2020-09-04 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599181342_20200904085942324_1127415104.jpg)
	6. 主要讲一下传输延时：
		1. 普通H桥驱动，最慢的是电平抬升模块，当然其他的滤波模块也有延时。
		2. 传输延时和输入的电压和温度有很大关系。如果这个设计很关键，就要考虑这些因素
		3. ![Screenshot-2020-09-04 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599181343_20200904090157135_391033790.jpg)
		4. ![Screenshot-2020-09-04 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599181344_20200904090205351_794625567.jpg)