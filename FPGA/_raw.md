# 1. FPGA_notes


## 1.1. 参考资料

## 1.2. 名词解释
- HDL：hardware description language
- FSM：finite state machine
- RTL：register transfer logic 

## 1.3. 总结


# 2. Basics
## 2.1. 变量
- 大小写敏感
- 所有的系统关键字，都是小写的
- 变量名字：
	- 字母大小写+下划线开头
	- 字母大小写+_+$
	- 1024的最大长度


## 2.2. 数字：
- X代表未知
- Z代表高阻
- ![Screenshot-2020-09-07 PM7](https://gitee.com/AndrewChu/markdown/raw/master/1599480356_20200907195510441_1277838853.jpg)
## 2.3. wire reg
端口的数据类型。
1. 其实输入基本都是reg，因为我们要锁住他，下一步使用
2. 输出都是wire，直接输出出去就行了。当然也可以把reg的信号输出

## 2.4. 注释
Single line comments begin with the token // and end with a carriage return
Multi line comments begin with the token /* and end with the token */

## 2.5. always
### 2.5.1. 敏感列表
可以是电平，也可以是沿

### 2.5.2. 组合逻辑
```
always  @ (a or b or sel)
begin
  y = 0;
  if (sel == 0) begin
    y = a;
  end else begin
    y = b;
  end
end
```
1. 这个是个2选1的组合逻辑
2. 注意，使用的是`=`，表示的阻塞式赋值。表示一个串一个，有先后优先级。
3. `assign out = (enable) ? data : 1'bz;`这个是assign开始的组合逻辑。所以组合逻辑有两种形式。
### 2.5.3. 时序逻辑
```
always  @ (posedge clk )
if (reset == 0) begin
  y <= 0;
end else if (sel == 0) begin
  y <= a;
end else begin
  y <= b;
end
```
1. 这个是时钟触发的时序逻辑。就是一个触发器
2. 使用的是 `<=`，是非阻塞实式。大家一起进行。

# 3. FAQ
## 3.1. 锁存器
Note: One thing that is common to if-else and case statement is that, if you don't cover all the cases (don't have 'else' in If-else or 'default' in Case), and you are trying to write a combinational statement, the synthesis tool will infer Latch.


## 3.2. 组合逻辑和顺序逻辑
Combinational elements can be modeled using assign and always statements.
Sequential elements can be modeled using only always statement.
There is a third block, which is used in test benches only: it is called Initial statement.

in the case of combinational logic we had "=" for assignment, and for the sequential block we had the "<=" operator. Well, "=" is blocking assignment and "<=" is nonblocking assignment. "=" executes code sequentially inside a begin / end, whereas nonblocking "<=" executes in parallel.


## 3.3. 奇偶校验
核心思想：
1. 第一次见1，输出才会变1
2. 第二次见1，输出会变0. 开始重复步骤1.类似于计数了。
```
function parity;
input [31:0] data;
integer i;
begin
  parity = 0;
  for (i= 0; i < 32; i = i + 1) begin
    parity = parity ^ data[i];
  end
end
endfunction
```



亚稳态是指触发器无法在某个规定的时间段内到达一个可以确认的状态。使用两级触发器来使异步电路同步化的电路其实叫做“一步同位器”，他只能用来对一位异步 信号进行同步。两级触发器可防止亚稳态传播的原理：假设第一级触发器的输入不满足其建立保持时间，它在第一个脉冲沿到来后输出的数据就为亚稳态，那么在下 一个脉冲沿到来之前，其输出的亚稳态数据在一段恢复时间后必须稳定下来，而且稳定的数据必须满足第二级触发器的建立时间，如果都满足了，在下一个脉冲沿到 来时，第二级触发器将不会出现亚稳态，因为其输入端的数据满足其建立保持时间。同步器有效的条件：第一级触发器进入亚稳态后的恢复时间 + 第二级触发器的建立时间 < = 时钟周期。




11：对于多位的异步信号如何进行同步？

对以一位的异步信号可以使用“一位同步器进行同步”，而对于多位的异步信号，可以采用如下方法：1：可以采用保持寄存器加握手信号的方法（多数据，控制， 地址）；2：特殊的具体应用电路结构,根据应用的不同而不同 ；3：异步FIFO。（最常用的缓存单元是DPRAM）

14：FPGA芯片内有哪两种存储器资源？

FPGA芯片内有两种存储器资源：一种叫block ram,另一种是由LUT配置成的内部存储器（也就是分布式ram）。Block ram由一定数量固定大小的存储块构成的，使用BLOCK RAM资源不占用额外的逻辑资源，并且速度快。但是使用的时候消耗的BLOCK RAM资源是其块大小的整数倍。


FPGA芯片有固定的时钟路由，这些路由能有减少时钟抖动和偏差。需要对时钟进行相位移动或变频的时候，一般不允许对时钟进行逻辑操作，这样不仅会增加时 钟的偏差和抖动，还会使时钟带上毛刺。一般的处理方法是采用FPGA芯片自带的时钟管理器如PLL,DLL或DCM，或者把逻辑转换到触发器的D输入（这 些也是对时钟逻辑操作的替代方案）。


三种资源：block ram;触发器（FF），查找表（LUT）


21：查找表的原理与结构？

查找表（look-up-table）简称为LUT，LUT本质上就是一个RAM。目前FPGA中多使用4输入的LUT，所以每一个LUT可以看成一个有 4位地址线的16x1的RAM。 当用户通过原理图或HDL语言描述了一个逻辑电路以后，PLD/FPGA开发软件会自动计算逻辑电路的所有可能的结果，并把结果事先写入RAM,这样，每 输入一个信号进行逻辑运算就等于输入一个地址进行查表，找出地址对应的内容，然后输出即可




ROM：Read Only Memory，只读存储器，手机、计算机等设备的存储器，但现在的所说的ROM不只是Read Only了，也是可以写入的。

RAM：Random Access Memory，随机存取存储器，手机、计算机的运行内存。

SRAM：Static Random-Access Memory，静态随机存取存储器，只要供电数据就会保持，但断电数据就会消失，也被称为Volatile Memory

DRAM：Dynamic Random Access Memory，动态随机存储器，主要原理是利用电容存储电荷的多少来代表一个bit是0还是1，由于晶体管的漏电电流现象，电容会放电，所以要周期性的给电容充电，叫刷新。SRAM不需要刷新也会保持数据丢失，但是两者断电后数据都会消失，称为Volatile Memory

SDRAM：Synchronous Dynamic Random Access Memory，同步动态随机存储器，同步写入和读出数据的DRAM。

EEPROM：Electrically Erasable Programmable Read Only Memory，电可擦除可编程只读存储器，

DDR：Double Data Synchronous Dynamic Random Access Memory，双倍速率同步动态随机存储器，双倍速率传输的SDRAM，在时钟的上升沿和下降沿都可以进行数据传输。我们电脑的内存条都是DDR芯片。

FLASH： Flash Memory，闪存，非易失性固态存储，如制成内存卡或U盘。


同步 异步。同步复位，异步复位



2 什么是竞争与冒险现象？怎样判断？如何消除？ 

     在组合逻辑中，由于门的输入信号通路中经过了不同的延时，导致到达该门的时间不一致叫竞争。产生毛刺叫冒险。
  如果布尔式中有相反的信号则可能产生竞争和冒险现象。
  解决方法：一是添加布尔式的消去项，二是在芯片外部加电容。


一个CLB包括2个Slices,每个slices包括两个LUT，两个触发器和相关逻辑。Slices可以看成是SpartanII实现逻辑的最基本结构。



1)可编程输入输出单元（IOB）
可编程输入/输出单元简称 I/O 单元，是芯片与外界电路的接口部分，完成不同电气特
性下对输入/输出信号的驱动与匹配要求。FPGA 内的 I/O 按组分类，每组都能够独立 地支持
不同的 I/O 标准。通过软件的灵活配置，可适配不同的电气标准与 I/O 物理特性，可 以调整驱动电流的大小，可以改变上、下拉电阻。目前，I/O 口的频率也越来越高，一 些高端的 FPGA，通过 DDR 寄存器技术可以支持高达 2Gbps 的数据速率。为了便于管 理和适应多种电器标准，FPGA 的 IOB 被划分为若干个组（bank），每个 bank的接口 标准由其接口电压 VCCO 决定，一个 bank 只能有一种 VCCO，但不同 bank 的 VCCO 可以不同。只有相同电气标准的端口才能连接在一起，VCCO 电压相同是接口标准的基 本条件。
2)可配置逻辑块（CLB）
FPGA 的基本可编程逻辑单元是由查找表和寄存器组成的，查找表完成纯组合逻辑功
能。FPGA 内部寄存器可配置成触发器或锁存器。Altera 基本可编程单元 LE 配置为 1 寄存器加一个查找表。
3)嵌入式块 RAM（BRAM）
块 RAM 可被配置为单端口 RAM、双端口 RAM、内容地址存储器（CAM）以及 FIFO
等常用存储结构。CAM 存储器在其内部的每个存储单元中都有一个比较逻辑，写入 CAM中的数据会和内部的每一个数据进行比较，并返回与端口数据相同的所有数据的 地址，因而在路由的地址交换器中有广泛的应用。除了块 RAM，还可以将 FPGA 中的 LUT 灵活地配置成 RAM、ROM 和 FIFO 等结构。
4)丰富的布线资源
布线资源连通 FPGA 内部的所有单元，而连线的长度和工艺决定着信号在连线上的驱
动能力和传输速度。FPGA 芯片内部有着丰富的布线资源，根据工艺、长度、宽度和分 布位置的不同而划分为４类不同的类别。第一类是全局布线资源，用于芯片内部全局时 钟和全局复位/置位的布线；第二类是长线资源，用以完成芯片 Bank 间的高速信号和 第二全局时钟信号的布线；第三类是短线资源，用于完成基本逻辑单元之间的逻辑互连 和布线；第四类是分布式的布线资源，用于专有时钟、复位等控制信号线。
5)底层内嵌功能单元
内嵌功能模块主要指 DLL（Delay Locked Loop）、PLL（Phase Locked Loop）、DSP 和
CPU 等软处理核（Soft Core）。现在越来越丰富的内嵌功能单元，使得单片 FPGA 成为 了系统级的设计工具，使其具备了软硬件联合设计的能力，逐步向 SOC 平台过渡。
6)内嵌专用硬核
内嵌专用硬核是相对底层嵌入的软核而言的，指 FPGA 处理能力强大的硬核（Hard
Core），等效于 ASIC 电路。为了提高 FPGA 性能，芯片生产商在芯片内部集成了一些 专用的硬核。例如：为了提高 FPGA 的乘法速度，主流的 FPGA 中都集成了专用乘法 器；为了适用通信总线与接口标准，很多高端的 FPGA 内部都集成了串并收发器 （SERDES），可以达到数十 Gbps 的收发速度。

