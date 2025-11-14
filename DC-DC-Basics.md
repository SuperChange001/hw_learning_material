# 1. DC-DC-Basics
作为一个不是以电源设计为方向的硬件工程师。我的目标是掌握LDO，BUCK，BOOST，BUCK-BOOST，FLYBACK这几种拓扑。其他的拓扑如正激，半桥，全桥，PFC等我就不做了解。  
建议大家先看`基本元件`里的所有内容。R C L D的参数并不是大家想的那么简单，用好BJT和MOSFET更是每一个EE的基本功。  

## 1.1. 参考资料
1. [所有笔记的链接](https://gitee.com/AndrewChu/hardware-design)   
2. ADI-电源大师课(关注ADI智库微信，有免费版本的，就是播放器非常简陋)
2. [DCDC粗略介绍](https://training.ti.com/dc-dc-fundamentals-introduction?context=38908-374)
3. [DCDC-电容电感的参数](https://training.ti.com/capacitor-selection-overview?context=44120-1138819-1936)
4. [Load transient calculation](https://training.ti.com/dc-load-lines-how-they-can-benefit-your-next-design?context=1139912-1139916)
4. [DCDC架构](https://training.ti.com/buck-regulator-architectures-overview?context=5177-722)
3. 精通开关电源设计-中文版-第一版
- [Common Mistakes in DC/DC Designs](https://training.ti.com/common-mistakes-dcdc-buck-converters-part-selection?context=1127730-1135482-1139329-1135476)
- [Fixed Frequency vs Constant On-Time Control of DC/DC Converters](https://training.ti.com/fixed-frequency-vs-constant-time-control-dcdc-converters)
- [how to measure loop gain](https://training.ti.com/introduction-measuring-loop-gain-power-supplies?context=1127730-1135482-1139330-1135452)

## 1.2. 名词解释
1. DCDC：直流到直流变换器
2. ACDC：交流到直流变换器
3. SMPS：switching mode power supply
3. LDO：low dropout 低压差线性稳压电源
3. BUCK：降压变换器
4. BOOST：升压变换器
5. BUCK-BOOST：升降压开关电源
6. FLYBACK：就是反激式隔离电源
7. CCM：continuous conduct mode
8. DCM：discrete conduct mode
9. VMC：voltage mode control
10. CMC： current mode control
11. SRF：self-resonant frequency 

## 1.3. 总结

了解一个电源，主要有以下几个方面：
1. 常用拓扑：
	- 工作原理，
	- 充电回路，放电回路。
	- 每个节点的电压电流波形
2. 评价指标：
	- 纹波电压：Vripp
	- 暂态响应：line regulation，load regulation
	- 环路稳定性：1/2/3类补偿
3. 关键器件选型：
	- L：类型，容量。Isat，Irms，DCR，寄生电容，谐振频率
	- C：类型，容量，耐压，Irms，ESR，ESL，谐振频率
	- D：类型，Vf，If，Trecover，耐压，漏电流
	- MOSFET：损耗和功耗分析，If，Vce，Rdson，Cgd：Mealy Effect


几个基本概念是贯穿整个分析过程的：
1. 设计的要求：**输入电流和输出电流都是稳定的值**。在line regulation和load regulation时候除外
5. 电容的电压不能突变。`I=C*∂V/∂t`电容上的电流表示了电容上电压的变化率
6. 电感的电流不能突变。`V=L*∂I/∂t`电感的电压表示了电感上电流的变化率。法拉第定律
2. 电流流入电容的时间积分，就是电容的电压抬升。如果想要稳态工作，电容上的电压不波动，**一个周期内电容**的电流的I_total_mean=0。`Q=CV, Q=∫Idt`。
3. 电感上的磁通，就是瞬时电流的值。如果想让电感进入稳态，那么ΔΦ=0，那么ΔI=0。所以**一个周期内电感**上：ΔI_on=ΔI_off。`Φ=LI V=∂Φ/∂t`

几个经验技巧：
1. ΔIripp一般是Io的0.3-0.5
	1. 考虑到电感的体积和纹波电压的tradeoff
1. 开关频率和电感值
	1. 一般我们不喜欢电感变大，因为容量变大到2倍，体积变为4倍。
	2. 增大f，可以用小的L
	3. f大了，EMC特性就差了。
1. 输出电容：
	1. 纹波电压决定了电容的值。
	2. ESR决定了纹波电压
1. 输入电容：
	1. 容值？
	2. 一般使用的电解电容，他有个参数是Irms，一定要考虑


# 2. 电源的功能和参数
1. 电源的基本功能：
	3. 软启动
	4. 过流检测
	5. 欠压检测
	6. 过压检测
	4. 自举电路

- ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429487_20200826160836948_221409603.jpg)
- 参数：![](https://gitee.com/AndrewChu/markdown/raw/master/1598418391_20200826124100110_157821832.png)

# 3. BUCK
- 最重要：![](https://gitee.com/AndrewChu/markdown/raw/master/1598599909_20200503103347117_1500091518.png )
- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598429489_20200826161007687_1570382011.jpg)
## 3.1. LDO和BUCK的区别
- ![1](https://gitee.com/AndrewChu/markdown/raw/master/1598426470_20200826152023864_136200090.jpg)
- ![Screenshot-2020-08-26 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598426470_20200826152059649_2066799400.jpg)

## 3.2. 参数选择
- 效率的因素： 
	- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598431686_20200826161852936_1963656293.jpg)
- 输出纹波电压&动态响应
	- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598431687_20200826161935201_1796931395.jpg)
- 选择f和L
	- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598431687_20200826163444292_803454723.jpg)
- 选择MOS，功耗计算
	- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598431688_20200826163500228_1499949476.jpg)
- 选择电容
	- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598431688_20200826163518436_98588033.jpg)


## 3.3. LTspice
电压：![下载](https://gitee.com/AndrewChu/markdown/raw/master/1598418560_20200826130900595_1357945239.jpg)
各点的电流波形：![下载 (1)](https://gitee.com/AndrewChu/markdown/raw/master/1598418560_20200826130915220_26134601.jpg)

## 3.4. BUCK的电容
### 3.4.1. 输入输出电容的电流RMS
- 输出电容的电流RMS：
	- 简单，计算三角波的RMS
- 输入电容的电流RMS：
	- 复杂，背公式吧
	- 也有简单的等效公式：![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429480_20200826152452287_1007826601.jpg)
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598418392_20200826124136922_369226379.png)

### 3.4.2. 稳态的纹波
- 以上两者都会影响到电容的选择，主要是C和ESR上
- 用波形分析，哪种分量占主导：
	- ![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423995_20200826133251363_421801672.jpg)
- 经过复杂的公式推导后，我们可以得到一个近似的公式：ESR和C和输出纹波的关系
	- 近似公式，在中ESR区域有点不准。
	- 其实图中还根据ESR和C的关系，分为高中低ESR区域
	- ![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423995_20200826133439947_1091633552.jpg)
	- ![IMG_0314](https://gitee.com/AndrewChu/markdown/raw/master/1598423996_20200826133731669_1367654032.jpg)
	- 看似这个近似公式是吧ESR和C上的纹波均方相加了。
### 3.4.3. 高频纹波
之前计算的都是基于纹波电流产生的纹波电压。事实上还有第二种纹波，是因为电感的寄生电容，导致谐振，产生一个电流spike。这个时候，需要并联谐振电容来吸收尖峰。You will not know the capacitor values until after you test the running power supply for ringing noise。
- 为什么我们已经加的电容起不到作用：
	- 寄生参数![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423997_20200826134637228_434730862.jpg)
	- 电容的ESL：![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423998_20200826134959839_1171560215.jpg)
	- 走线的ESL：![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423999_20200826135049057_356513661.jpg)
- 选择合适的高频电容：
	- 谐振频率和容值，封装，材质有关系
	- 谐振频率：![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423999_20200826135219350_1396211999.jpg)

### 3.4.4. transient response的纹波
就是负载突然变大变小，导致的输出纹波产生的overshoot和undershoot。  
这个需要计算电容的C和ESR。一个笼统的公式`I*t=C*dv`，这里没有考虑ESR，同时t也是很难得到的。  
建议使用ADI的CAD工具去挑选合适的C，可以抑制住overshoot。  
loop gain的带宽越大，transient response的幅度越小

## 3.5. 电流的模式
电流模式：
1. CCM：电感的电流不会到0
2. DCM：电感的电流会到0，然后关断


## 3.6. 控制模式
控制模式：
1. VMC：电压模式控制
	1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1598426468_20200826151815031_720104941.png)
2. CMC：电流模式控制
	1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1598426469_20200826151832775_1733392542.png)
	2. ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429480_20200826155017138_1083644917.jpg)

## 3.7. 补偿
- 二型
	- ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429483_20200826155145240_1642820673.jpg)
	- ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429485_20200826155224475_89262717.jpg)
- 三型
	- ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429482_20200826155123676_301131438.jpg)
	- ![Screenshot-2020-08-26 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598429484_20200826155205726_854740888.jpg)

## 3.8. 最小开通时间
有些BUCK IC有一个参数：最小开通时间
这个参数的作用：
	- IC可以控制MOS最小的开启时间
	- 计算：
		- 输入16，输出1.8，那么D=0.8
		- Ton=D*T=D/T>30ns
		- 如果算出来的Ton很小，那么MOS管会来不及关断

## 3.9. EMC考虑
环路中，di/dt,dv/dt变化大的节点，EMC的影响会很大。  
di/dt：会耦合到线路的寄生电感上  
dv/dt：会耦合到对地的寄生电容上


# 4. BOOST
## 4.1. 输入输出电容的电流RMS
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598418394_20200826124435890_467658384.png)

# 5. BUCK-BOOST
## 5.1. 输入输出电容的电流RMS
- 只看前面两个开关是buck。只看后面两个开关是boost
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598418393_20200826124357872_1507495670.png)


# 6. FLYBACK
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598418395_20200826124632829_144311868.png)
- ![Screenshot-2020-08-27 PM12](https://gitee.com/AndrewChu/markdown/raw/master/1598773635_20200828085118275_1558878844.jpg)



# 7. 环路控制模式

电压控制模式
很稳定，很好。需要三型补偿网络
但是如果有CCM VCM模式的时候，补偿网络效果不同，需要compromise


使用网分测试电源的环路增益
穿越频率越高，瞬态响应越好，但是越不稳定。
穿越频率越低，就是阻尼系数越大，瞬态响应越差，但是越稳定
使得穿越频率在开关频率的1/5，会有45°的相位裕度

current mode 会忽略刚开始的spike。所以也有了一个minimal on time

占空比大于50%需要斜率补偿


# 8. Layout 建议

## 8.1. 电感的漏磁
[SRF分析](https://e2e.ti.com/blogs_/b/powerhouse/archive/2020/06/18/understanding-and-managing-buck-regulator-output-ripple)
BUCK的纹波
流过电容的电流是三角波
电容的ESR：三角波
C：正弦波
ESL：方波
但是电感会有寄生电容，产生自谐振，导致了一个spike。
解决方式：寄生电容小的，谐振频率高的。
多个输出电容并联，可以减小ESR ESL
减少dv/dt，在开关节点，串联一个小电阻，会减慢沿，但是降低效率



电感漏磁怎么办:
1. 选个带屏蔽壳的电感
2. 漏的磁，最终会感应到电容的ESL上，但是V=ΔΦ/Δt？
3. 输出电容，远离电感

# 9. 电源防护
- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598429490_20200826161114327_585439125.jpg)

# 10. 锂电池充电
- ![Screenshot-2020-08-26 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598429490_20200826161055129_1106730586.jpg)


# 11. 其他总结的资料
这里的内容，已经包含了很多电源大师课的内容。如果还想细致地了解一下，请看我做的
- [笔记：电源大师课](https://gitee.com/AndrewChu/hardware-design/raw/master/电源大师课.pdf)
- [开关电源参数设计](https://gitee.com/AndrewChu/hardware-design/raw/master/PDF/开关电源.pdf)

# 12. FAQ：
加强内容：MOS的损耗分析。电流控制电压控制。1，2，3型补偿？？这几点又忘了……   

## 12.1. 为什么输出有一串的电容并联
1. 暂态响应对电容的容值有更强的要求，一般只能用电解电容满足容量要求。
	1. 同时为了控制电解电容的ESR，需要并联陶瓷电容。
2. 吸收spike。
	1. 因为电感有寄生电容，有个谐振频率会让电感电流有个spike
	2. 这个spike会流过电容，产生高频的纹波spike。
	3. 这个时候需要输出电容吸收掉这个spike。
		1. 电容一直在考虑ESR，ESL。在高频下也有一个谐振频率。这个频率点的阻抗最低，能最好地吸收spike。
		2. 每个电容的谐振频率是不一样的，所以就要并联很多个电容，组成不同的谐振频率的吸收点。
3. 以上两个原因就是为什么输出会并联一堆的电容。简单的说就是要组成大容量，小ESR，多个谐振频率吸收峰

## 12.2. 为什么有了BUCK等拓扑，还要用各种控制原理
常用的控制原理有：
1. 电压控制
	1. 把输出的电压，经过分压采样电阻之后，和误差放大器的Vref比较，最终控制D。
2. 电流控制
	1. 在电压控制的基础上
	2. 多了，电流采样的环节，采集了输入的电流。

这些控制原理实现了闭环控制。如果只有BUCK，那么就是开环控制，Vin变了，D也不变，输出就不稳定了。引入了闭环控制之后，就要分析环路的稳定性，分析补偿方式。  
因为电压控制和电流控制引入的传函不同，零极点个数也不同，所以补偿方式也不同，但是补偿都是基于误差放大器的反馈网络进行补偿的。  


## 12.3. 为什么我们没有关注电源的稳定性
1. 首先理论分析复杂
	1. 因为有控制器和PWM环节
1. 其次实验室是可以测量的，但是需要网分。
	1. 给反馈电阻上注入一个小信号，测量输出的信号，多次测量就可以得到闭环传输函数了
1. 因为IC内置了反馈补偿网络
2. 就算外置了补偿网络。按照典型设计，选取一样的电容电感，就可以用它的补偿网络。

## 12.4. 怎么测试寄生参数
寄生参数测量![Screenshot-2020-08-26 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598423997_20200826134759827_445591747.jpg)















