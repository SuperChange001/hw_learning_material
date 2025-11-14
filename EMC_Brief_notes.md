# 1. EMC_Brief_notes
EMC在很多书里会被描述成电路的黑魔法。EMC包括EMI和EMS。两者的整改思路是一致的，一般EMI干扰严重的设备，EMS性能也不会好的。这个笔记主要简单的记录一些工程上，在设计阶段和整改阶段的EMC措施。

## 1.1. 名词解释 

- EMC：electromagnetic compatibility
- EMI：electromagnetic interference 。interference 干扰别人，辐射出去
- EMS：electromagnetic susceptibility。suspectibility 被别人干扰，耐受程度
- CISPR：International Special Committee on Radio Interference
- IEC：international electrical commitee 
- RE：radio emission
- CE：conduct emission
- RS：radio susceptibility
- CS：conduct susceptibility
- ESD：electrostatic dischagre
- EFT：electo fast transient
- Surge：
- THD：totle harmonic distortion
- AN: artifical network
- LISN:line impedance stabilization network
- PK: peak 
- AVG: average
- QP: quasi peak

## 1.2. 参考资料
- [所有笔记的链接](https://github.com/SuperChange001/hw_learning_material)   
- 电子产品设计EMC分析评估-郑军旗
- [我的笔记：Product_EMC_Evaluation](https://github.com/SuperChange001/hw_learning_material/blob/master/Product_EMC_Evaluation.md)
- [EMC for isolator-TI](https://training.ti.com/ti-precision-labs-isolation-introduction-emc-tests-isolation?context=1139747-1135015-1139269-1147201)


## 1.3. 有关标准
- 首先是按照产品族，每个行业都有自己的行业标准
- 接着行业标准里会规定使用哪种EMC的通用标准进行测试，会裁剪测试内容和指定criteria。
- 图：![Screenshot-2020-09-01 AM10](https://gitee.com/AndrewChu/markdown/raw/master/1598928848_20200901105403477_60520596.jpg)
- 图： ![Screenshot-2020-08-31 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1598927514_20200901082907814_5714924.jpg)
- 安规标准：	- ![Screenshot-2020-08-31 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598927772_20200831161157455_2068621287.jpg)


## 1.4. 总结
1. 公式：
	1. I=C*∂u/∂t
	2. u=L*∂i/∂t
	3. 理解麦克斯韦方程组
2. EMC分析：干扰源+传播路径+敏感器件
	1. 干扰源：DCDC，时钟，高速通信总线
	2. 传播途径：共模干扰，差模干扰。寄生电容耦合。
		1. 共模干扰是我们研究的重点：因为共模电流的回路如果不特意设计，很容易从线缆的寄生电容耦合到PE，形成天线辐射。
		2. 每种器件，在高频下，就会有很多的非理想特性，特别是寄生电容会形成意想不到的共模电流回路。
	3. 敏感器件：
		1. 一般指的是EMS里的器件，模数电路都是有电平阈值的。
		2. 如果是EMI，那就是被50欧拾取的共模电流信号、被100欧拾取的高频差模电流信号。
2. 共模和差模，共模电压和共模电流。
	1. 共模电压和共模电流没有必然关系。因为他们的共模阻抗未知。但是共模电压的突变，必然会导致共模电流的变化。
3. EMI的频谱特点：
	1. 30M以下走的是线缆，是传导干扰
	2. 30M以上是空间辐射，是辐射干扰
	3. 为什么？
		1. 因为线缆要是1/4或者1/2的整数倍，天线的辐射效应才会最强。
		2. 所以辐射的波长和线缆的长度是有关系的。1Ghz的RE，至少线要长于10cm。30Mhz的RE，线要长于10m。这里的线缆也可以是PCB走线的长度
		3. 所以30M以下的能量，想要空间辐射是很难得。
1. 什么东西会成为高增益的天线？
	1. 什么是电磁场？
		1. 电场：两个点，有电势差，就会有电场。一定不要往电路内部走线的电场想。要往走线外部的空间电场想。
		2. 磁场：有电流，就有磁场。直的电流产生环形磁场，环形电流产生直的磁场
	1. 什么是近场和远场：
		1. 近场分为电场还是磁场
		2. 远场就是混合的电磁场，相交成90°往前传递。
	2. 天线的载体：
		2. 线缆：尤其是长线缆，会发出更多的能量。所以能把线做短就做短
		2. PCB的长导线：原理和线缆一直
		3. 大的散热器：结构就很像波导。表面的长度也非常的长
		4. 大的铜皮：像个环路天线
	1. 天线的驱动源：
		1. 电压驱动：偶极子天线用电压驱动，近场是很强的电场。
			1. ![IMG_0973](https://gitee.com/AndrewChu/markdown/raw/master/1598927516_20200901094642679_194828485.png)
		2. 电流驱动：环形天线用电流驱动，近场是很强的磁场。     
			1. ![IMG_0974](https://gitee.com/AndrewChu/markdown/raw/master/1598927516_20200901094654190_746670960.png)
3. 设计时候的EMC注意点：
	1. PCB叠层：
		1. 4层：信号--GND--VCC--信号
		2. 6层：信号--GND--信号--VCC--GND--信号
	2. PCB布局：
		1. 所有的接插件在一遍，边上放上几个接地桩
		2. 模数分开，高频信号远离线缆。面得从线缆发射出去
		3. GND平面，要保证高频信号的GND阻抗很小。
		4. GND不要设计成一个环形，避免成为环形天线
	2. 线缆：
		1. 线缆的屏蔽层：要么接GND，要么接PE，悬空就会成为天线。建议接PE
		2. 线缆的屏蔽端接：pig tail effect。要360度端接
		3. 把线缆设计短，可以省很多事：
			1. 有些测试，明确了只对3m以上的线
			2. 短线，不容易成为天线。
	2. 接地：
		1. GND和PE：单点接地还是多点接地
		2. AGND和DGND：磁珠，铜皮；多点还是单点
	3. 内部地平面阻抗和电流回路：
		1. 如果电流回流的地平面阻抗很大，那就会形成电流驱动的天线。
		2. 所以要把有高频电流的地平面阻抗控制住。
	3. 外壳：
		1. 金属还是塑壳
		2. 开了多少缝，缝的尺寸会和辐射出去的波长有关系
	4. DCDC：
		1. 搞清楚电压突变回路和电流突变回路。然后把环路控制到最小。
		2. DCDC会有辐射，这个是不能避免的
		3. 远离线缆和板边
		4. 实在没办法，可以在开关节点并联一个小电容，降低slew rate和dv的突变。这样牺牲了效率
	1. 变压器：
		1. 因为寄生电容，原副边会走共模电流。加一个stitch cap，可以减少电压值突变值，减少辐射发射
	5. 晶振：
		1. 下面铺地
		2. 不要放置在板子边缘，不要放置在开缝的边缘
	6. 外部高速总线
		1. 用滤波和防护设计。加入choke。注意choke的结电容
	7. 内部高速总线
		1. 包地加地桩。
		2. 走到板子的内层。
		3. 3W和20H。
	9. 滤波器的位置：卡在壳体，清晰地分出滤波区域和未滤波区域，两者不会互相干扰
	10. ![下载](https://gitee.com/AndrewChu/markdown/raw/master/1598927515_20200901084546820_565183252.jpg)
	11. ![Screenshot-2020-09-01 AM11](https://gitee.com/AndrewChu/markdown/raw/master/1601269962_20200901111457198_729040155.jpg)
4. 整改的时候的注意点：
	1. 根据频谱，判断是哪个噪声源的高频谐波泄露了
	2. 污染源一般都是ACDC模块，一般是一上电就会超标。搞清楚哪些设备内集成了ACDC和DCDC等开关器件，和他们的工作频率。
	3. 加磁环把：
		1. 原理：就是共模扼流圈。LN线上的共模信号会看到很大的阻抗。
		2. 不是个数越多越好。加剧耦合电容，磁环失去效果了
		2. 不是圈数越多越好。增加的插入损耗，不会成倍数增加。
		3. 超标的频率要和磁环的特征频率一致
		4. 选择多个频点不一样的磁环串联，效果会更好。
	1. 加电容：磁环是堵住干扰，电容是给个低频回路到PE。要case by case
	2. 改接地：一般都是分析出地平面的阻抗大，会形成ΔV驱动的天线。要减少阻抗。



# 2. 测试内容：

## 2.1. 基本测试项：
分为板级和系统级。因为AC-DC已经帮我们做了很多EMC相关的东西，如电压跌落，谐波。我们可以关注在板级。但是要记住，EMC是个系统级的测试。抛开系统只做单板的EMC意义也不大
- 测试内容：![Screenshot-2020-08-31 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1598927514_20200901083736934_1388417942.jpg)
- 我们只关注在以上5个方面，TI总结的还是很到位的。
- 完整的测试内容： ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598927509_20200826164539021_733415856.jpg)



# 3. 差模和共模
## 3.1. 总结
1. 我们关心的是共模电流，不是共模电压。 
2. 对于CAN来说：只要保证共模电压在dominant和recessive的时候维持不变，那就不会有问题，共模电流会非常小。如果在跳动，那么就会辐射出来。
3. 共模电流如果从线缆上流过，那就会造成很强的辐射。 
4. 共模和差模，会因为电路结构的非理想性，互相转换

## 3.2. 分析
很多人对于共模信号的认识也就基于以下几点：
1. 首先分析共模和差模，一定要有两条线。可以是CANL和CANH，也可以是VCC和GND。
2. 差模就是我们关注的两个信号的差/2。
	1. 差模是信号对信号
	2. 差模电流方向：一个流入，一个流出
	3. 差模电压并不能说明什么。因为I=V/R。两个节点有差模电压，因为R很大，那就没有差模电流。
	4. 我们研究的是**差模电流，不是差模电压！**
3. 共模就是两个信号的和/2。
	1. 共模是信号对PE的，所以VCC和GND也可以当做一对差分信号来研究
	2. 共模电流方向：同方向。
	3. 共模电压不能说明什么。我们关心的是共模电流。但是电路每个节点对PE都有寄生电容。这个就意味着，只要信号f越高，对PE的阻抗就会很小，信号就会从PE走了。
	4. 共模信号的关键在于PE。PE不一定等于GND，PE可能会被抬起来。


对我们的系统来说，差模是我们想要的信号，而共模不是我们设计的参数，我们也没有给共模信号设计环路。导致共模电流如果泄放不当，那就会有很大的环路，就会引起很大的EMC问题。  
差模和共模的关系：  
1. 电路中，因为器件参数的非理想性，导致我们想要的信号产生一定的畸变。我们经常听说差模可以转共模，共模转差模。
	1. 比如差分对，理论上我们想要的是差模信号。但是如果两个BJT的参数不一致，那么就有一部分的差模会变成共模信号，CMRR参数会直线下降
	2. 比如CAN的tranceiver，如果内部的两个管子，一个压降1V，一个压降0.8V，那么CANH/L的共模电压就不是2.5V了，而是2.4V。但是静默的时候却又是2.5V。那么共模电压就会有一个跳变。这里的共模电压，对PE可能是一个环路的，但是平常的时候电流非常小，但是对于f很高的跳变，共模电流就会很大。
2. 对于CAN来说：
	1. dominant的时候：H电压4.5V，L电压0.5V，CM电压2.5V，DM电压2V。
	2. recessive的时候：H/L的电压都是2.5.CM电压2.5V，DM电压0V。
	3. 那我们就会奇怪了，共模电压一直都是2.5V，那么应该有一个很大的共模电流啊？为什么我们实际看到的CAN的电流，就是对称的，从H进,L出。
		1. 因为共模电压有了，但是我们不知道共模阻抗，主要是寄生电容。只有当f很高的时候，这个环路的Z才会很小，共模电流才会出现。
		2. 所以一个节点的共模电压再大都没关系，只要他不跳动。
		3. 如果一个节点的CM电压跳动了，那就必然会对PE有电流流过的行为，这个就是EMC超标的原因
- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598927510_20200826164548028_234396735.jpg)

# 4. EMI

## 4.1. 传导的耦合模型
- 电容耦合：
	- 线缆和PE
	- 地平面和PE
	- 变压器的源边和副边
		- 所以两边可以加个电磁屏蔽层
		- 或者两边串联一个电容。争取把ΔV做到最小。
	- 隔离光耦，源边和副边也有2pf的寄生电容
- 电感耦合：
	- 当环路有个电流突变，如果有寄生电感，就会产生很大的感应电动势
	- 也可以是和外界形成互感，其实本质是一样的。

## 4.2. EMI分析的方法
1. ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598927511_20200826164608381_923795459.jpg)
2. ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598927512_20200826164612961_302007899.jpg)


# 5. 测试设备
- 频谱仪：没啥好说的。一般都是准峰值测试为标准。对谐波有个加权系数
- LISN：给EUT供给直流电。会把EUT回馈给电压的高频差模和共模噪声，用50欧的阻抗采样后给频谱仪
- CDN：耦合去耦网络。通过电容耦合的方式，把共模干扰加到线缆上。典型的就是EFT

# 6. 常用EMC器件
## 6.1. XY电容
安规电容，注意型号和容值都是有要求的
## 6.2. 旁路小电容
提供给高频的泄放回路。可以有效地防止信号从线缆辐射出去
## 6.3. 滤波电容
1. 物理模型：
	1. 低频下就是个电容
	2. 高频下：是电容串电阻串电感。
		1. 要开始考虑引线电感了
		2. 同时，引线之间也会有耦合电容，会破坏高频环路
		3. 高频的阻抗就是要考虑串联谐振了。谐振频率不会特别高，所以电容的高频特性不好
1. 使用穿心电容
	1. 优点：利用了引线电感，组成滤波

## 6.4. 共模电感
1. 两组线圈绕在一组磁芯上。同名端在同一边。使用的铁氧体
2. 共模信号的磁通叠加，等于电感量很大的电感
	1. v=l*di/dt 解释不通
	2. 从阻抗的角度 z=jwL,那么L越大，对同频率的共模信号，阻抗越大
1. 对差模信号，磁通相减。但是需要考虑漏感。
	1. 利用漏感，可以做差模滤波。
	2. 因为磁通相消，那么久可以当成只有Rdc的导线
	3. 漏感产生的原因
		1. 两个线圈的圈数不一样
		2. 线圈绕的不够密，有漏磁

## 6.5. 磁珠
1. 物理模型：电感和电阻的并联
	1. 低频下是个电感
	2. 高频下是个电阻
	3. 是个耗能元件
	4. 有阻抗的特性曲线，在特定频点下Z最小，类似选通网络
1. 关键参数
	1. 通流量
	2. 交流阻抗
	3. 直流阻抗，及其导致的压降
1. 使用磁珠的时候一定要想清楚：
	1. 一般使用在模拟和数字GND。让高频的干扰不会在模数GND之间传递。
	2. 那就是要给高频的模拟噪声一个泄放路径。用个电容接到PE上。不要把所有的路都堵死，那么高频的模拟噪声就会从找个耦合电容的路径了。
## 6.6. 磁环
整改的时候的补救措施。
## 6.7. 滤波器
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598927507_20200503103437782_580127246.png)

- 主要针对传导辐射和传导抗扰度。频段是150k~30Mhz。

- 主要参数
  - 分为直流和交流，一般是交流的滤波器比较多。
  - 频谱的插入损耗
  	- 要针对辐射超标段，选择对应效果最好的滤波器
  



# 7. Layout建议
1. 护沟的布局
	1. ![IMG_1033](https://gitee.com/AndrewChu/markdown/raw/master/1601269963_20200928131144980_494939182.jpg)
1. 网络接口的布局
	1. ![IMG_1037](https://gitee.com/AndrewChu/markdown/raw/master/1601269964_20200928131229722_176214326.jpg)





# 8. FAQ

## 8.1. DCDC中的EMC
One of the easiest ways to mitigate EMI is with the right printed circuit board (PCB) layout. For a buck converter, your most important considerations are:

Reducing the surface area of high transient voltage (dv/dt) nodes.
Reducing the loop area of high transient current (di/dt) loops.

Slew-rate control reduces the turnon time of the high-side field-effect transistor (FET), which reduces energy in the high-frequency harmonics. Simply add a small resistor in series with the boot capacitor, or use a boot resistor on the dedicated RBOOT pin of devices that have this feature built-in. Slowing the slew of the FETs improves EMI but decreases efficiency,


## 8.2. DCDC
有些时候，把电感掉个方向，。因为漏磁是有方向的，也许可以抵消板子其他的EMI

## 8.3. 怎么判断是否是高频信号
1. 判断信号是否是高频信号？
	1. 看信号的上升沿。决定了信号的上限带宽。f=0.35/Tr。
	2. 再计算最短的波长λ=C/f。
	3. 如果走线大于波长的1/16，那就是高频信号。
1. 为什么要区分高频信号？
	1. 因为判断是否要用传输线理论去分析电路。是否要考虑阻抗匹配和反射。









