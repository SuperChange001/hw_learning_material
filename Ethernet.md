# 1. _Ethernet

## 1.1. 参考资料
- [TI Ethernet portfolio overview](https://training.ti.com/industrial-ethernet-key-phy-requirements)
- [Ethernet PHY](https://software-dl.ti.com/public/hpmp/sitara/eth_sys_hw_am_devices/presentation_html5.html)
- [POE](https://training.ti.com/ieee8023bt-new-features?context=1137930-1139677-1128369)
## 1.2. 名词解释
1. PDU：protocol data unit
2. LLC: logical link control
3. MAC:media access control
4. PHY:physical
5. MII:media independent interface
6. MDI:media dependent interface
7. PCS：Physical coding sublayer
8. PMA：physical media attach
9. PMD：physical media dependent
10. MLT：multi level transmission
11. PAM：pulse amplitude modular
12. POE: power over Ethernet
13. PSE：power source equipment
14. PD：powered device

## 1.3. 总结
1. 以太网的layout，水晶头下面的gnd要挖空。因为不同的参考平面，水晶头里是有变压器隔离的。
2. OSI7层：
	1. PHY在物理层
	2. MAC在数据链路层
1. 理解Ethernet的层级
	1. 重点在理解media：就是物理媒介
	2. MII连接了PHY和MAC，是单端信号，要等长
	3. MDI连接了PHY和网口，是差分信号。

1. MAC我们不用管，意味着数据链路层以上我们不关心。我们就只关心PHY，PHY和MAC之间的MII走线。
2. PHY里面的PCS是处理软件编码的，工作都在这一块
3. PMA和PMD其实是一起的，都是和media打交道。但是为了避免不同的media导致的不同的协议，所以提取了和media更加紧密的PMD出来。
4. 注意百兆和千兆网的MII和MDI其实都是不一样的。千兆忘得MII要求更多了，对Layout也更加严格了。
5. Bootstrap电阻，也是需要考虑的一个点。
6. 时钟清晰了误码率
7. MDIO是控制总线，和Ethernet是分离的，只是为了PHY的诊断。所有MDIO的信号都不会在网线上体现
8. POE：在网线上提供44V到57V的直流电
	1. 怎么实现：2条线是一个pair，会有一个变压器。那么在2个pair的2个变压器的中心抽头，注入直流信号，就相当于两个变压器有共模电压差。到了PD再把直流的压差提取出来。
	2. 发展历史
		1. IEEE802.3af：1类.PD13W
		2. 802.3at：2类。PD25W
		3. 802.3bt：3-4类。PD71W


# 2. PHY

## 2.1. OSI模型
- ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194601_20200904123627682_1452002655.jpg)
4. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189647_20200904105211639_1475192288.jpg)
5. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189648_20200904105319891_1081590865.jpg)
- Ethernet的三大块
	- ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194603_20200904123659219_577562767.jpg)
## 2.2. PCS
- PCS:不愧是coding的层，负责编码，信息检测和冲突检测
	- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189649_20200904105556757_1974498746.jpg)
	- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189650_20200904105604923_720663698.jpg)


## 2.3. PMA
- PMA：PCS和PMD之间传话的
	- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189652_20200904105816429_343899784.jpg)

## 2.4. PMD
- PMD：解释了为什么需要PMA，因为PMD会依赖于media，不同的media会导致PMD不一样。但是标准想要把物理层的东西和PCS这个编码层分开，所以就娱乐PMA
- 
- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189653_20200904105943952_644343265.jpg)


# 3. 电路模块
1. 电路上的模块
	1. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189654_20200904110350370_344098194.jpg)
	2. ![Screenshot-2020-09-04 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1599189671_20200904111633354_347293779.jpg)
1. MAC interface的种类
	1. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189655_20200904110509283_156166398.jpg)
	2. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189658_20200904110549955_96013751.jpg)
1. 延时：
	1. 这里主要写的是PHY里面的延时
	2. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189661_20200904110634037_1208206965.jpg)

## 3.1. SDF
1. 一帧数据的开始SFD
	1. ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189662_20200904110917119_1907137869.jpg)

## 3.2. Power
- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189664_20200904111013165_457534157.jpg)

## 3.3. Layout
-  ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189665_20200904111100035_1004021959.jpg)
- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189666_20200904111116649_2038799481.jpg)
- MII是等长的  MDI是差分的
	- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189667_20200904111226406_1988805948.jpg)
	- ![Screenshot-2020-09-04 AM9](https://gitee.com/AndrewChu/markdown/raw/master/1599189668_20200904111331025_902674614.jpg)

## 3.4. Layout建议2
1. 总览
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194604_20200904123830505_629508778.jpg)
1. 线长匹配，要匹配到失调端，不然走线都是有延时的
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194604_20200904123934761_164646176.jpg)
1. 参考平面决定了信号的回流路径。走线阻抗会使得EMI严重
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194605_20200904124027613_736783278.jpg)
	2. 类似于3W，保持1.5W就能使得EMI被吸收80%
	3. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194605_20200904124106438_1403791615.jpg)
1. 不得不跨分割，使用缝合电容。类似于抑制共模干扰。也是提供AC回路
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194605_20200904124157226_886442447.jpg)
1. 3W原则，防止串扰。距离板边的缩进。不然容易把能量泄露出去
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194606_20200904124236472_556402711.jpg)
## 3.5. 线缆pin
1. 百兆和千兆以太网的线缆CAT类别是不一样的
2. 百兆网的信号对：1发一收。3MLT
	1. ![Screenshot-2020-09-04 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1599189669_20200904111442004_1707354002.jpg)
	2. ![Screenshot-2020-09-04 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1599189670_20200904111606174_552610030.jpg)
1. 千兆网：2发2收。PAM5
	1. ![Screenshot-2020-09-04 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1599189672_20200904111646031_1190872543.jpg)
	2. ![Screenshot-2020-09-04 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1599189673_20200904111748943_2042178638.jpg)

## 3.6. bootstrap
1. 启动电阻的选取：
	1. IC可能是2阈值的，也可能是5阈值的。
	2. 同时也要考虑内部的电阻和他的精度
	3. 电阻要根据模式来选取。具体的要看手册。


## 3.7. clock
1. 使用的crystal的类型
2. 需要的起振电阻，限流电阻，负载电容。
3. 晶振的jitter对信号质量的影响
4. PHY对于晶振的要求。比如PPM，温漂精度。

## 3.8. redriver和retimer
1. redriver就是个中继，进行简单的信号放大，当线长超过了标准。也对一些jitter有修正效果
2. retimer可以调节时序。
3. jitter：
	1. 有来源的：串扰，信号反射，时延不匹配，DCDC的电源噪声
	2. 随机噪声：白噪声
	1. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599190353_20200903195141592_85906748.jpg)


# 4. 协议：
- MII，RMII RGMII：pin数量，参考时钟的复用。
	- ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599194603_20200904123742180_598337053.jpg)

# 5. POE


## 5.1. 基本原理
1. PSE怎么注入电源
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198015_20200904132926479_1723816966.jpg)
1. 优点：
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198016_20200904133015111_1863543562.jpg)
1. 发展历史
	1. IEEE802.3af：1类.PD13W
	2. 802.3at：2类。PD25W
	3. 802.3bt：3-4类。PD71W
	2. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198016_20200904133044455_1194848296.jpg)

## 5.2. 802.3at
1. 12 36两组线圈注入
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198017_20200904133319714_1264671552.jpg)
## 5.3. 802.3bt
1. 到了bt。所有线圈都注入，一共2组。为了降低阻抗
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198017_20200904133433694_353547438.jpg)

### 5.3.1. handshake
1. 检测有没有PD，然后检测PD的分类，需要给他多少电流
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198018_20200904133527213_171578591.jpg)
1. 检测：
	1. ![Screenshot-2020-09-04 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1599198018_20200904133615969_853387557.jpg)
1. 分类：
	1. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198019_20200904133627570_1288232701.jpg)
1. at的握手
	1. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198020_20200904133658799_562106852.jpg)
1. bt的握手
	1. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198020_20200904133729130_1771405109.jpg)
	2. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198021_20200904133919082_2003005380.jpg)
	3. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198022_20200904133923896_1675850433.jpg)
	4. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198022_20200904133959857_385300680.jpg)
	5. ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198022_20200904134005712_1529426511.jpg)

## 5.4. 保护

### 5.4.1. inrush
- 优点烦躁，就贴图把。。。等用到了再来写心得。
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198631_20200904134950193_80253101.jpg)
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198632_20200904134957907_775060993.jpg)
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198632_20200904135006506_1477832972.jpg)
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198633_20200904135014471_1221108887.jpg)
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198633_20200904135019867_247919102.jpg)
- ![Screenshot-2020-09-04 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599198634_20200904135024496_1800972300.jpg)