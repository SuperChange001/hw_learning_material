# 1. SPI_notes
## 1.1. 参考资料
1. [TI-precision-labs](https://training.ti.com/ti-precision-labs-data-converters?context=1139747-1140267)

## 1.2. 缩写
SPI：serial peripheral interface

## 1.3. 总结：
- SPI是牺牲了电路的简洁性，换取控制的简洁性。
	- IIC用电平逻辑，表达了起始位，结束位。SPI是多了CS_n这个线
	- IIC用SDA一条三态线表示了数据的输入输出。SPI把输入输出变成两条线，就不用判断复杂的三态逻辑了。
	- IIC看似节约了IO，但是性能也被制约了。QSPI就可以实现大容量的数据传说。同时IIC是半双工的，SPI是全双工的。
- 不同片子都要有不同的CS_n，限制了以后扩展外设的能力。必须要改板子才能加节点。
- QSPI：quad SPI。多出来的是数据线，可以提高传输的速度
- SPI的通信开始，建立在CS_n被拉低了。
- IIC是开漏输出。对于总线上的电容有要求，但是难测，所以一般满足上升时间就可以了tr。

## 1.4. 物理层
- SPI只是规定了物理层，协议要根据peripheral来。
- MSB是第一位
- 常规的SPI只有四条信号线，QSPI多出来的是数据线，而且功能可能是复用的，要根据手册
	- CS_n:片选信号，低电平有效
	- SCLK: 时钟信号，主机控制
	- DIN:主机输出
	- DOUT:从机输出
## 1.5. SPI的四种模式
- CPOL：clock polarity 
	- 0： 第一个沿是rising
	- 1：第一个沿是falling
- CPHA：clock phase
	- 0：触发在第一个沿
	- 1：触发在第二个沿
- 可以看出来，SPI都是边沿触发的，只不过在哪里触发是可以调节的。

## 1.6. timing diagram
时序图：
- setup time：
	- 采样时钟前，信号要建立的时间
- hold time：
	- 采样时间后，信号要建立的时间
- propagation time ：
	- 收到非采样时间后，信号延迟的时间
- ![下载](https://gitee.com/AndrewChu/markdown/raw/master/1598334315_20200825134505375_126796732.jpg)


# 2. IIC
先简单的描述一下IIC，因为我之前做FPGA的时候，自己写过IIC的驱动，所以还是有点心得的。

## 2.1. 物理层
- 一定要上拉电阻，因为PHY是开漏的，同时R和分布的C决定了tr
- 和SPI一样是板内通信。想要出板子，还是要差分传输才能又可靠，距离又远
- ![Screenshot-2020-09-03 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599130144_20200903180201504_167003779.jpg)
- IO：
	- SCL：时钟信号，主机发送
	- SDA：数据信号，三态门，主机和从机都可以使用
- arbitration：
	- 开漏输出，类似于CAN。但是是单端信号，还依靠SCL来同步信号。
	- 所以需要上拉电阻，阻值看功耗。
	- 所以是有总线仲裁的。
- 报文：
	- SOF：SCL是高的时候，一个下降沿
	- EOF：SCL是高的时候，一个上升沿
	- SCL高电平，sample SDA。如果SDA这个时候波动了，那就会误认为是error
- 速率，容性负载和上升时间
	- ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130146_20200903183512775_21084976.jpg)
	- ![Screenshot-2020-09-03 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599130145_20200903180228937_579959247.jpg)

## 2.2. 上拉电阻的确定
1. 上拉电阻如果太大
	1. 上升的tr会很大，不能满足要求
1. 上拉电阻如果太小
	1. 因为IC里面的MOSFET是有Rdson的，所以不能如果上拉电阻太小，那么就算是低电平的时候，输出的电压也会高于Vth。

## 2.3. Buffer的使用
1. 两边Vcc不匹配的时候。可以使用合适的buffer转换电平
2. 总的C太大了，可以用buffer做隔离，电容就会变成原先的一般
3. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130343_20200903185215262_2091359510.jpg)

## 2.4. IIC的协议
1.  开始位，结束位，数据位，读写位，ACK
	1. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130147_20200903184821273_51545539.jpg)
	2. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130147_20200903184856189_563532566.jpg)
1. 写数据：
	1. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130342_20200903184951546_1587119033.jpg)
1. 读数据：其实是哟欧dummy write的，把寄存器的指针先弄过去
	1. ![Screenshot-2020-09-03 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599130343_20200903185121944_1854711323.jpg)

# 3. UART

- 最简单的接口，一般只用于debug。因为只能一对一。
- 逻辑分为RS232和TTL232，两者是不兼容的。因为RS232定义的接口电平很高，所以很容易损坏接口。
- 232是LSB先传输的，比较奇葩
- 常用速度9600bps，最高是115200bps
- 一般也就2m的通信距离
- 依靠双方约定了传输速度，来进行数据同步。双方按照约定的速度，可以算出采样的间隔。
- 空闲的时候信号线为高，拉低了表示开始传输。



# 4. FPD
- 高速的信号，都有并行串行化，然后再去串行。
- ![Screenshot-2020-09-03 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599130146_20200903180342007_315195431.jpg)

## 4.1. 曼侧斯特编码
- 直接把时钟和数据信号融合在一起，更加的可靠了。
- 从1变成0，表示1。从0变成1，表示0。
- 速率要求比之前的快了1倍
- 连续传0，也需要先变成1然后再下降到0.

# 5. 信号完整性基础 
- 信号衰减的原因：
	- ![Screenshot-2020-09-03 PM6](_v_images/20200903195123003_1961739970.jpg)
- Jitter的来源
	- ![Screenshot-2020-09-03 PM6](_v_images/20200903195141592_85906748.jpg)