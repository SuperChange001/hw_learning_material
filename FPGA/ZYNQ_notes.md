# 1. 正点原子FPGA

## 1.1. 缩写
1. SCU：snoop control unit 一致控制器
2. MMU：memory management unit
3. OCM：onchip memory
4. FPU：浮点运算单元
5. MIO：multiplex IO 复用IO
6. EMIO：extended MIO 扩展复用IO，占用了FPGA的IO资源
7. AXI： advanced extenxible interface 高级可扩展总线，ARM的
8. AMBA： advanced microcontroller bus architecture
9. bsp： board support package
10. hdf：hardware definition file----规定了外设的物理地址
11. mss：microprocessor software specification--提供了软件的外设demo
12. FSBL: first stage boot loader
13. SSBL: Second stage boot loader
14. PCAP: Processor configuration access port
15. POR: Power on reset
16. TTC: triple timer counter
17. SWDT: software watch dog timer


## 1.2. 开发板信息
ZYNQ-7020 核心板主控芯片为 XC7Z020CLG400-2， 85K LC（逻辑单元）， 4.9Mbit BRAM
ZYNQ-7020 核心板板载两片 4Gbit DDR3 内存，芯片型号为 NT5CB256M16EP-DI，总容量为 8Gbit （ 1GB）；
PL 端 50Mhz 晶振
PS 端 33.333Mhz 晶振
领航者核心板的 eMMC 芯片型号为 KLM8G1GETF
## 1.3. 管脚分配
### 1.3.1. Constrain
```
set_property IOSTANDARD LVCMOS33 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]
set_property IOSTANDARD LVCMOS33 [get_ports {led[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports key]

set_property PACKAGE_PIN U18 [get_ports clk]
set_property PACKAGE_PIN J15 [get_ports rst_n]
set_property PACKAGE_PIN H18 [get_ports {led[1]}]
set_property PACKAGE_PIN J18 [get_ports {led[0]}]
set_property PACKAGE_PIN L20 [get_ports key]

create_clock -period 20.000 -name clk -waveform {0.000 10.000} [get_ports clk]

set_property -dict {PACKAGE_PIN L20 IOSTANDARD LVCMOS33} [get_ports key_in]
```

### 1.3.2. PL
| name      | Dir | IO  | Info                | Volt |
| :-------- | :-- | :-- | :------------------ | :--- |
| sys_clk   | i   | U18 | 50M clock          |      |
| rst_n     | i   | J15 | reset normal high  |      |
| key[0]    | i   | L20 | normal high        |      |
| key[1]    | i   | J20 | normal high        |      |
| led[0]    | o   | J18 | High--on  Low--off |      |
| led[1]    | o   | H18 | High--on  Low--off |      |
| touch key | i   | L19 | touch--high        |      |
| beep      | o   | G18 | high--on           |      |
### 1.3.3. PS
管脚资源：
		 *	0 - 31,  Bank 0
		 *	32 - 53, Bank 1
		 *	54 - 85, Bank 2
		 *	86 - 117, Bank 3
主要用到的是bank0/1，后面2个是PL的EMIO的。
主要：要区分ARM的GPIO的bank，和封装的物理供电bank是不一样的
- ![下载](https://gitee.com/AndrewChu/markdown/raw/master/1599556216_20200908171008792_90007644.jpg)
## 1.4. FPGA基础
- 早期的soc都是定制化的，所以开发周期很长，投入大
- PLD 可编程，
	- SPLD：乘积项。使用与或逻辑阵列，输出逻辑单元。
	- CPLD：乘积项很多，IO有自己的逻辑控制
		- LAB：logical block PLA 可编程的块
		- PIA：programmable interconnection
	- FPGA：LUT lookup table
		- CLB: configurable logical block 
		- IOB: IO block
		- PIM: programmable interconnection matrix
		- Altera
			- LE：一个寄存器+一个LUT
			- LAB: 10个LE
		- Xilinx 7：
			- CLB：
				- 2个slice
					- 4个LUT 8个触发器 和其他逻辑
					- ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546168_20200429140221995_1378165193.png )
			- Block RAM:
				- 1个36K，或者2个18K，总线宽度18，那么有2048个
				- 也可以配置为更加小
			- 布线资源：用户不用管
				- 全局
				- 长线
				- 短线
				- 分布式的布线资源
			- 底层嵌入功能单元
				- PLL： phase locked loop
				- DLL： delay locked loop
### 1.4.1. PL简介
7020的PL一共有三个IO bank。一样的IO bank使用一样的电压供电。
bank13 bank34 bank35
### 1.4.2. 时钟PLL
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546176_20200503101148911_363152962.png )
### 1.4.3. RAM
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546180_20200503101813363_1996497005.png)

### 1.4.4. USART
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546182_20200503102016969_693178660.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546183_20200503102625118_154953645.png )
### 1.4.5. RS485
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546190_20200503212938363_643893809.png)
1. 一主多从，主问从答。
	1. 因为没有总线仲裁，多对多，自由发送就会导致总线物理层出问题
2. 挂载节点
	1. 和驱动芯片有关系
	2. 和接收芯片的收入阻抗有关系，一般是>12KΩ
	2. 和通信距离有关系
		1. 主要是分布电容会变大，带不起来
	3. 一般是32，128，256个从机，但是一个地址要做主机
		1. 要有地址位，不然无法区分从机
1. 波特率和通信距离
	1. 100kbps可以到1km
	2. 因为速率越低，对噪声和波形畸变的容忍就越大，就可以把距离做的更加大
1. 要分清楚物理层和网络层
	1. 物理层：485 CAN
	2. 网络层：modbus canopen。网络层就有了报文的概念
	3. 数据链路层：总线仲裁，软硬结合的地方
1. 协议层：
	1. 常用的是modbus。要注意，每次收发的是一个字节，把很多个字节的数据组成一帧报文
	2. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546188_20200503212349522_808714696.png )
### 1.4.6. IIC
1. 物理层
	1. 2线，
		1. SDA 数据线。注意是开漏的，都需要上拉电阻
		2. SCL 同步时钟
	1. 物理走线就决定了，只能一主多从，主机给出SCL，从机同步
1. 数据链路层
	1. 总线仲裁：因为其开漏的模式，所以一个从机拉低，都拉低了总线。所以有总线仲裁
1. 网络层：
	1. 起始位，数据位，应答位，结束位。MSB在前，先发送。usart是LSB在前发送。
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546192_20200505092723570_142712308.png )
	2. 读写控制：跟在地址位后面，r是1，w是0.
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546192_20200505100612756_1974010504.png )
	3. 单次写：主机发送完器件地址和数据地址后+0，从机产生应答完0后，主机发送停止位
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546193_20200505100751166_719678225.png )
		1. 单次写入之后，需要延时10ms保证数据正确
	4. 多次写：和单次写的差别是，主机一直不产生停止位，最后才产生停止位
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546194_20200505100903217_1004027671.png )
		1. 注意，一次写不能超过一个page，这里是32B
		2. 写入需要延时10ms
	5. 读当前地址：主机发送完器件地址后+1，从机回复数据+主机nack后，主机发送停止位
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546194_20200505101016685_1914052018.png )
	6. 随机读地址：需要有个dummy write虚写操作，把地址指针给转到当前位置
		1. 没有数据的单次写+读当前地址
			1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546195_20200505101133070_167234466.png )
	1. 顺序读：在随机读的基础上，主机每次发送ack，从机就会一直发送数据
		1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546195_20200505101314620_1801059786.png )
	2. ACK的理解
		1. ack是为了让主机知道读写有没有成功。
			1. 所以主机写的时候，从机发送ack，ack就是成功写入，nack就是没有成功
			2. 其实主机读的时候不用ack，因为主机自己知道有没有读成功。这个时候ack就用来做连续读和单词读的标志，nack就是读完成的标志。
### 1.4.7. SPI QSPI

### 1.4.8. CAN

### 1.4.9. TFT
1. 其实TFT的显示不复杂，要把行同步和帧同步搞清楚就行。
2. 每一种同步，都有四个参数，下图没有把sync的时长画出来。要注意sync的有效值是高还是低
3. 要计算TFT的时钟频率：1s=刷新率*行像素*列像素  行列像素都有4个部分
4. 要计算出当前位置的xy像素，再去请求这点的RGB888的数值。请求的动作要超前DE一个时钟，因为是寄存器输出。
3. 显示方式有两种：
	1. DE模式
		1. 就是只在数据有效的区域拉高DE信号，其他位置都是低
			1. DE信号可以由组合逻辑产生。那么计时就要到>=sync+hbp 和<sync+hbp+hfp
			2. 就相当于从0计时到sync+hbp-1，因为是电平触发的
		2. 同时要把HS和VS两个信号一直拉高
		3. 其实DE模式不关心两个同步，只关心有效的显示区域  
	4. HV mode 行场同步
		1. 就是要计算HS 和VS的时序，在有效的时候拉低同步
		2. 其实画一幅图片，起作用的是HS。会有一个计数器计算V_cnt,当这个值已经跑完一帧，才会给出一个VS有效信号
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546185_20200503102734047_1555731351.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546186_20200503102821324_1563414032.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546187_20200503102909368_1837214779.png)
### 1.4.10. HDMI
物理层特性，网络层特性
1. 全称：high definition multimedia interface
2. 向下兼容DVI digital video interface
	1. 只能传音频，接口更大
1. 物理层使用TMDS transition minimized differential signaling
	1. 四队差分信号：
		1. 3对用于RGB
		2. 1对是同步clk
	1. 热拔插，IIC，CEC customer electrical control信号
		1. IIC用于读取display的数据
	2. 会把HS VS放入到blue通道，从8bit变成10bit，需要serializer实现，时钟变为原先10倍
		1. 不是简单的变成串行，是需要TMDS编码的。实现直流平衡，跳转次数在5次以内
	3. 消隐时间。
		1. 就是de无效地时候，对应传输控制字符
		2. 划定同步的边界
		3. 同时也可以把音频放入消隐时间
	2. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546191_20200505084448735_1166705295.png)
### 1.4.11. 原语
就是fpga内已经固话好的硬件模块，可以直接调用。这些模块：
1. 比较简单，功能比较单一，但是非常常用


## 1.5. PS简介
PS里不仅仅是ARM
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546169_20200429141944734_1255951948.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546171_20200429142141613_1167623673.png )


### 1.5.1. AXI总线
AXI总现在PS和PL上一共有9条。主机是控制总线并发起会话的，而从机是做响应的
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546172_20200429143639674_545505825.png )
一共有三类AXI总线
1. 通用AXI总线
	1. 32位数据总线
	2. 透明不带fifo
	3. 4条，2个PS master，2个PL master
2. 加速器一致性端口
	2. 64位总线
	3. PL和SCU之间的单个异步链接， 实现APU的cache和PL的数据一致性
	4. PL做主机
3. 高性能端口
	1. 32位或者64位
	2. 带fifo
	3. PL做主机

## 1.6. Verilog
### 1.6.1. 运算优先级
非》算术》移位》关系》位运算》逻辑》条件
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546196_20200506094804568_1693612244.png )
### 1.6.2. 避免锁存器的产生
latch是和D触发器对应的。锁存器更像是组合逻辑。
寄存器指的是一种概念，可以存储数据的单元，所以可以是latch也可以是触发器
我们主要比较latch和时序寄存器的区别。
1. 两者的特点：
	1. 寄存器的输出端平时不随输入端的变化而变化，只有在时钟有效时才将输入端的数据送输出端（打入寄存器）
	2. 而锁存器的输出端平时总随输入端变化而变化，只有当锁存器信号到达时，才将输出端的状态锁存起来，使其不再随输入端的变化而变化
	3. 所以锁存器会受到glitch的影响，如果真的要用锁存器，就要把信号同步好
3. 用法：
	2. 若数据有效一定滞后于控制信号有效，则只能使用锁存器；
	3. 数据提前于控制信号而到达并且要求同步操作，则可用寄存器来存放数据。
1. 结论
	1. 组合逻辑中的，语句不完整会导致锁存器。注意，在时序逻辑里永远不会有锁存器
		3. 以下两种情况，就会导致latch
			1. always @(*) 然后 if后面没有else。
			2. case语句没有全，
		1. 为什么？
			1. 因为正常的情况是为了生成一个选择器，但是条件没全，就说明输出不仅仅和输入有关系，也有可能和上一个输入有关系，可以被锁存住。这就会自动生成锁存器
	2. 锁存器就是组合逻辑，容易产生竞争冒险和电平毛刺。
	3. 只有当时钟信号建立后，信号还没建立的情况，才会用锁存器。
	4. FPGA里的基本单元可以配置成触发器和锁存器，所以不存在锁存器耗资源的说法。
		1. 但是锁存器没有时序，让静态分析变得困难
		2. 容易引入干扰
		3. 其实锁存器比触发器更加快。cpu里用的很多，但是fpga没必要用它
		3. 既然如此，为什么不做成一个触发器呢？
### 1.6.3. 二维数组定义
`reg   [127:0] char[31:0]; `
1. 第一维度 128
2. 第二维度 32
3. 就是32个 长度为128的数组
## 1.7. 开发板介绍
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546173_20200429145728253_708711732.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546178_20200503101332682_814152499.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546177_20200503101300722_363307560.png )
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546179_20200503101349333_1842735656.png )


## 1.8. FAQ
### 1.8.1. 竞争和冒险
1. 产生原因
	1. 出现在组合逻辑中，时序逻辑中不会产生
	2. 组合逻辑中只要会出现：A=B+B'，那就会产生竞争
1. 解决办法：
	1. 组合逻辑的输出加电容。难以实现
	2. 把组合逻辑变成时序逻辑，由时钟同步触发
	3. 组合逻辑中增加冗余项，让任意情况下不会出现A=B+B'

### 1.8.2. 同步电路和异步电路
1. 基础概念
	2. 同步电路：时钟触发的电路，大家都已时钟沿为输出的标准
		1. d触发器
			1. 速度慢
	2. 异步电路：各自信号都能触发输出
		1. latch
			1. 速度快
1. 区别：
	1. fpga里要避免使用latch，但是可以使用latch
	2. 同步电路指的是全局是同步，局部也可以是异步的
1. 举例：
	1. ![Screenshot-2020-09-08 AM11](_v_images/20200909094802319_1139541821.jpg)


### 1.8.3. 同步复位和异步复位
1. 基本概念：
	1. 同步复位：
		1. 在clk时钟触发下，一起复位
	1. 异步复位：
		1. 直接让rst信号，控制D触发器复位。D触发器都是有置位和复位脚的
1. 差异：
	1. alter使用的基本触发器就是带复位的，所以他们推荐使用异步复位。
		1. 使用同步复位。要额外做一个选择器，选择rst和signal
	2. 但是xilinx推荐的是同步复位
		1. 同时，控制信号需要使用复位
		2. 数据信号不要使用复位
		3. 复位用的多了会导致时钟难以约束

### 1.8.4. D触发器
xilinx的D触发器，也是带有clr和pre的，分别用来复位和置位
1. RTL视图
	1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546200_20200513151812572_1301533236.png )
	2. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546199_20200513151748312_1626629878.png )
1. 要理解，if else在fpga里就是选择器。这里用同步复位来做个例子
	1. ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546200_20200513151911758_600669110.png )
### 1.8.5. 100M带宽的示波器，测量100M的方波
1. 基础概念：
	1. 100M带宽指的是示波器的-3db衰减频率是100M。所以100M的输入，输出是-3db。-3db对电压是0.707，对功率是半功率0.5。
	2. 100M的方波：基频是100Mhz，高频谐波是奇次波。
		1. 基波的幅度 2*Vin/pi
		2. 奇次波的幅度 1/3 1/5

### 1.8.6. 建立时间和保持时间
1. 建立时间
	1. setup time：在clk来之前，信号要保持稳定的时间
	2. setup slack：建立裕度
3. 保持时间：
	1. hold time：在clk之后，信号要保持稳定的时间
	2. hold slack
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546198_20200513140858263_2134582668.png)
- 传输延时
	- Tcycle +Tskew > Tco+Tgate +Tsetup
	- Thold +Tskew > Tco+Tgate
	- ![Screenshot-2020-09-08 PM12](_v_images/20200909094851970_1146622336.jpg)

### 1.8.7. 状态机编码方式
1. 独热码
	1. 只有一位是1，其他都是0
	2. 浪费了寄存器资源，因为编码很长
	3. 节约了逻辑资源，因为一次只要比较一位，不用每一位都比较
	4. 适合少量状态，fpga
	5. 因为变化的信号少，所以适合高速信号
2. 二进制码
	1. 普通的8421二进制编码。
	2. 节约了寄存器资源，因为可以表示很多个状态
	3. 但是逻辑资源用的很多
	4. 适合cpld
3. 格雷码
	1. 一次只变化一位的二进制码，适合状态数很多
	2. 因为只变化一位，所以产生的功耗小，
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546199_20200513140950846_69094294.png)


### 1.8.8. Xilinx SDK debug
需要在对应的BSP里设置编译的标志位 -g。这个是编译的优化等级
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546201_20200516135545790_2022597829.png )















