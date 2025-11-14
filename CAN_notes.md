# 1. CAN笔记
## 1.1. 参考文档
1. [CAN we start at the very beginning?](https://e2e.ti.com/blogs_/b/industrial_strength/archive/2015/04/30/can-we-start-at-the-very-beginning)
2. [TI-precision-labs](https://training.ti.com/ti-precision-labs-interface?context=1139747-1138099)

## 1.2. 名词解释
- CAN：controller area network
- LIN：local interconnection network
- CAN FD：flexible data rate
- CISPR25： EMI Comité International Spécial des Perturbations Radioélectriques (CISPR) 25 
- ISO11898-2 ：the physical layer for classical CAN
- GPD：groud potential difference
- CRC：cyclic redundancy check
- ACK: acknowledge
- EOF：end of frame
- IDE：identification extender
- DLC：data length code


## 1.3. 总结：
1. 搞清楚CAN和RS485，这两个真的非常像
	1. PHY的区别：全桥和半桥
	2. 物理信号的区别：有显性和隐形位。还是完全反转信号
	2. 总线仲裁的区别：破坏性还是非破坏性
	3. 协议的区别：CAN定义了协议。485只是PHY
	4. 抗干扰的区别：GPD的定义不一样
	5. 端接电阻的区别：485非常不推荐，不接匹配电阻。CAN是一定要接匹配电阻
	6. 节点数量：485是有UL的说法。CAN只有负载电容的说法，实际上还是看波形把。关注，tr和在75%的周期的信号。
1. CAN抑制共模干扰的方式：
	1. 把匹配电阻分成60+60+C
	2. 还有一种常用的对差分信号的共模信号的滤波方式：当然对CAN的信号不适用。大家要了解。
		1. 3个C
		2. 2个接在信号对PE
		3. 1个接在差分信号之间
		4. 因为共模滤波的两个C，会存在不匹配的原因，会把共模转成差模干扰。所以需要1个差分的C。
		5. 同时差分的C的截止频率要比共模C的截止频率小10倍，那么可以忽略共模转的差模。
# 2. CAN的物理特性
规范是在ISO11898
- ![1598332940_20200825121739173_2012345793](https://gitee.com/AndrewChu/markdown/raw/master/1598333303_20200825132450962_1605644583.jpg)
特性：
- GPD 从-2到7V
- 最高速度1Mbps
	- ![1598332940_20200825121739173_2012345793](https://gitee.com/AndrewChu/markdown/raw/master/1598333304_20200825132501124_1612168474.jpg)
	- 最长40m
- 最多30个节点
- tranceiver要能在54欧的电阻上产生1.5V的电压
	- ISO11898-2 describes the physical layer for classical CAN as a differential bus technology that supports a maximum signaling rate of 1Mbps over a bus length of 40 meters with a maximum of 30 nodes. 
	- transceiver must support a minimum output differential voltage of 1.5 V across a 54Ω load and a nominal differential input capacitance of 10-pF.	
- Dominant state – a minimum 1.5V output differential voltage (VOD) into a 50-65Ω differential load (TXD = low).
- Recessive state – a maximum 50mV VOD into a 50-65Ω differential load (TXD = high).
- CAN的优点：
	- 平衡差分，抗干扰能力强
	- 可以自诊断
	- 可以修复数据错误
- CAN的问题：
	- 有效载荷太小了
	- 速率不可变。在头部为了避免碰撞，可以用低速率的。但是data frame可以使用高速率的啊。
	- The first shortcoming that limits CAN communication today is the amount of overhead that comes with every message, or frame as the CAN standard refers to it. An easy way to look at this is to compare the number of bits of data that can be sent in one frame versus the total number of bits that need to be sent as overhead. For example, CAN limits the number of bytes that can be sent in the data field to eight bytes of data, which is equivalent to 64 bits. A CAN frame with an 11-bit identifier field will have a total 111 bits in each frame, not including stuff bits which to simplify this blog will not be taken into account. That means that 47 bits, or 42.3 percent of the message, is overhead!
	- The second thing that limits CAN communication is the speed, or data rate, at which the information is sent over the bus. This is where the flexible data-rate part of the title comes to play. One of the benefits of CAN is that when multiple nodes try to access the bus at the same time a non-destructive bit-wise arbitration takes place at the beginning of the frame. To ensure that nodes on opposite ends of the bus can properly arbitrate for bus access, the speed of communication is limited by the two-way loop time of the bus. With a propagation delay of roughly five nanoseconds per meter on a twisted pair bus of 24 AWG wire, this delay starts to really reduce the maximum communication speed with longer buses.


## 2.1. 平衡传输
- 理论上，CAN是平衡差分输出的。但是CANL CANH细微的不对称性，就会导致差模转共模干扰。
	- small asymmetries between the CANH and CANL signals can give rise to a differential signal that is not perfectly balanced. When this occurs, the common-mode component of the CAN signal (the average of both CANH
and CANL) will no longer be a constant DC value. Instead, it will exhibit data-dependent noise.
- CAN有共模干扰的原因：
	- H和L的稳态电平有差。
	- 两者之间有延时。导致了有个尖峰。
- 结果：共模干扰可以发射或者传导，影响到其他部件。导致EMI超标
- 解决方式：
	- 把终端电阻分成60+60+C，可以抑制这个高频的共模干扰。
	- choke
		- 优点：把inbalance的共模电流抑制了
		- 缺点：如果产生LC谐振，会导致更大的噪声。而且电感续流，共模电流变化，会感应出很高的电压，损坏IC
	- chokeless：选的IC一致性更加强

# 3. CAN transceiver的构造
- CAN的基本结构：
	- 控制器和收发器：
		- 控制器：负载data link的操作，如stuffing，atribution。
		- 收发器：物理层的转换。单端的TXD转换成CANH/L。要满足ISO11898的物理层要求，如驱动能力，差分输出。
	- 显性位dominant：看CANL的电平，是0.
	- 隐形位recessive：
		- 其实是高阻，靠终端电阻泄放能量
	- 终端电阻：
		- 120欧：
		- 60+60+C解地：抑制共模干扰
	- 结构一定要对称：在dominant和recessive的时候，共模电压都要是VCC/2
	- 注意，放电的波形！
	- ![1598332936_20200825121614967_507762532](https://gitee.com/AndrewChu/markdown/raw/master/1598333304_20200825132615152_291998852.jpg)
	- driver：没有看到receiver的结构，可能和RS485一致。
		- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598332933_20200823134853501_1478642698.png)

## 3.1. 3V和5V的CAN兼容性
尽量不要混着用，但是考虑到3V的CAN可以少用一个电源，现在也流行了。其实是兼容的，从以下几个方面：
- 标准考虑了这种情况，所以3V的CAN的Vcm不是VCC/2，而是在2V左右
- 虽然比5V的Vcm=2.5V稍微低了一点，但是GPD的规定是-2到7V，所以影响不大。
- Vcm的不平衡，会导致一定的共模电压跳动，产生EMI，所以可以用电容端接的形式



## 3.2. 端接的重要性
- 不同于RS485，没有终端电阻的时候也能工作，只是会导致高频信号反射，最终让波形难看一点，眼图闭合一些。	
	- 485是H桥驱动，0和1都是强驱动
- 如果CAN不加终端电阻，那么他会在recessive status放不了电，导致报文错误
	- CAN是开漏输出形式，0是强信号，是显性的；1是弱信号，是被动地在终端电阻上放电才行的。
	- properly terminating the bus is very important because it ensures that the recessive edge decays properly, and in time for the next bit’s sample point.
	- when you lose one of the two terminations, the recessive edge takes over twice as long to decay (120ns vs. 251ns). This delay will increase with larger and more capacitively loaded networks. For the scenario shown in Figure 4, with no termination resistors the bus will not decay back to the recessive state even after 18.0µs! For cases where the RC delay is too slow, 
	- 终端电阻要匹配好，不然差模转共模，共模转差模。干扰了系统，也影响了信号质量。
	- Any variation in resistance will convert the common-mode noise present on the network into differential noise, thus compromising the receiver’s noise immunity.
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598332935_20200824183504600_1899782783.png )
- 转折频率要比通信的速率高，要不然连通信的基波也衰减了。
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598332935_20200824183522075_862370285.png)

# 4. 通信
1. 采样点是在75%的位置
	1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1598332944_20200825122309235_617583312.png)
1. 传播延时+长线的通信速率
	1. ![下载](https://gitee.com/AndrewChu/markdown/raw/master/1598333305_20200825132715092_1519483973.jpg)
1. IC的三种状态：
	1. normal ：都活着
	2. standby：receiver还活着
	3. sleep：都睡着了
1. 报文
	1. 	![](https://gitee.com/AndrewChu/markdown/raw/master/1598332948_20200825123213587_1835263014.png)
	2. SOF：一个显性位
	3. Message ID：是用来做arbitration总线仲裁的，低的值，优先级更加高
	3. RTR：0是数据帧，1是远程帧
	4. IDE：说明ID是11位的还是更多
	5. DLC：数据是多少位的
	6. data field: 传输DLC个Bytes
	7. CRC：15位，使用15-crc-can
	8. ACK：是从机响应的，收到报文就回一个0
	9. EOF：发出7个1，说明结束了
	10. bit stuffing：5个连续的信号之后，会反向填充
		1. CRC，ACK，EOF是固定长度的，不会填充
	1. Frame types：
		1. data frame
		2. remote frame
		3. error frame
		4. overload frame
# 5. CAN FD
FD：flexible datarate  
1. CAN FD的优点
	- 速度快到5m
	- payload从8bytes到64
	- data frame和CRC可以以更高的速度传输。仲裁段因为传输延时，还是不能更快
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598332949_20200825131016664_957854437.png)
2. CAN FD可以向下兼容
	1. 但是主控IC要认识，同时物理层也要支持更高速度


# 6. 协议
CANOPEN已经是更高层的协议。data link的协议CAN已经自带了



# 7. LIN
LIN是低成本，低速度，没有安全功能的地方使用的总线，是CAN的子总线

LIN：![下载 (1)](https://gitee.com/AndrewChu/markdown/raw/master/1598333306_20200825132813851_1261168024.jpg)

Physical：![](https://gitee.com/AndrewChu/markdown/raw/master/1598332951_20200825131630267_13094875.png)






