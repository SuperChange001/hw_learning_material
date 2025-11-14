# 1. FPGA

本篇文章主要针对Xilinx ZYNQ-7020系列的SoC FPGA

## 1.1. 管脚约束

| 功能名字 | Pin Number | Notes |
| -------- | ---------- | ----- |
| LED0     | M14        | M14   |
| LED1     | M15        | M15   |
| LED2     | K16        |       |
| LED3     | J16        |       |
| KEY0     | N15        |       |
| KEY1     | N16        |       |
| KEY2     | T17        |       |
| KEY3     | R17        |       |
| OSC-FPGA | U18        |       |

管脚约束的模板：

一定要记得时钟约束。

```verilog
set_property PACKAGE_PIN U18 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]

create_clock -period 20.000 -name clk_0 -waveform {0.000 10.000} [get_ports {clk_0}]
```



## 1.2. 数据类型

| 整数     | 标识 | 例子         |
| -------- | ---- | ------------ |
| 二进制   | b    | 8‘b0000_0001 |
| 八进制   | o    | 9'o001       |
| 十六进制 | h    | 8'h001       |
| 十进制   | d    | 8'd1         |
|          |      |              |

## 1.3. 数据的定义：

| 例子                   |                             |      |
| ---------------------- | --------------------------- | ---- |
| Parameter width = 8 ;  | 定义常量                    |      |
| reg [width-1 : 0] a;   | 定义8位的寄存器变量         |      |
| Reg [7:0] ram [255:0]; | 定义了8位的ram，一共256深度 |      |
| 1'bx                   | 不定值                      |      |
| 1'bz                   | 高阻态                      |      |

## 1.4. 三态门处理

在最开始接入的模块，就要把IO分成in和out，再接入后续的模块

![Screenshot-2019-12-27AM9.50.14](https://gitee.com/AndrewChu/markdown/raw/master/1599546603_Screenshot-2019-12-27AM9.50.14.png)

```verilog
assign IO = isOut ? Data_Out : 1'bz;
assign Data_In = IO;
```

## 1.5. PWM CLK 生成

```verilog
assign LED = ( System_Seg < Option_Seg ) ? 1'b1 : 1'b0;
```

## 1.6. FIFO

1. 数据特性：
   1. 只用传入数据，和ram比，不用管地址。
   2. 读写都在clk的上升沿进行。（那就是在下降沿准备数据？）
2. 用处：
   1. 数据暂存
   2. 同步跨时钟域

## 1.7. 常用的通信物理层

### 1.7.1. RS232

1. 物理特性
   1. 异步通信，没有时钟
   2. 全双工，可以同时tx rx
   3. 空闲的时候IO是H
2. 数据格式
   1. 起始位：IO拉低，一个电平
   2. 数据位：8位，LSB在前
   3. 校验位：1位
   4. 停止位：IO拉高，一个电平
3. 发送接收信号同步
   1. 发送：按照bps，一个周期改变输出的IO信号
   2. 接收：接收到第一个下降沿后，开启bps为周期的计时，每次到bps/2，输出采样时钟。

### 1.7.2. RS484

### 1.7.3. RS422

### 1.7.4. SPI

1. 物理特性
   1. 同步通信，有时钟
   2. 全双工，可以同时MOSI, MISO
   3. 空闲的时候cs是H, 拉低表示开启
2. 数据格式
   1. 数据位：8位，MSB在前
3. 发送接收信号同步
   1. 发送：产生clk，在clk下降沿的时候，设置数据
   2. 接收：接收clk，在clk上升沿的时候，读取数据

### 1.7.5. IIC

![img](https://gitee.com/AndrewChu/markdown/raw/master/1599546599_1426240-20180916153357946-538149405.png)

![img](https://gitee.com/AndrewChu/markdown/raw/master/1599546600_1426240-20180916153457230-1442447992.png)

1. 物理特性
   1. 同步通信，有时钟
   2. 半双工，不能同时tx rx
   3. 空闲的scl是h，sda是z
2. 数据格式
   1. 起始位：scl在h的时候，sda变低
   2. 数据位：scl是h的时候，sda必须稳定（不然就是起始或者停止了），MSB在前
   3. 停止位：scl在h的时候，sda变高
   4. ACK: 发送器发送8个数据后，就会在第9时钟释放数据线。
      1. ACK是从机发的，把SDA拉低
      2. NACK是主机接收的时候发的，把SDA置高
3. 发送接收信号同步
   1. 发送：按照bps，一个周期改变输出的IO信号
   2. 接收：接收到第一个下降沿后，开启bps为周期的计时，每次到bps/2，输出采样时钟。

### 1.7.6. CAN

## 1.8. 常用的协议

### 1.8.1. AXI 协议
1. AXI协议是ARM公司所有，在AMBA协议里的一部分
2. AXI一共有三种形式：
	1. AXI-lite：只能传输总线宽度的数据。
	2. AXI：一般形式。支持burst-out。一个地址后可以传输多个数据
	3. AXI-steam：没有地址数据，类似于FIFO，适合大数据传输
1. 信号的建立，是靠每一组信号的握手。发起者发送valid，接受者发送ready
	1. ![Screenshot-2020-09-08 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599616462_20200909095407732_1444770293.jpg)
### 1.8.2. Modbus

### 1.8.3. CAN Open



## 1.9. FAQ

### 1.9.1. 1 设计步骤

1. 画出模块框图，每个模块都预留isEn和done_sig（信号可以是多位的），根据框图把每个模块的接口文件写好。![Screenshot-2019-12-27AM8.46.15](https://gitee.com/AndrewChu/markdown/raw/master/1599546603_Screenshot-2019-12-27AM8.46.15.png)
2. 画出状态机
3. 编写代码
4. **编写仿真代码 **: 针对top层
5. 综合
6. 运行行为级仿真
   1. 仿真的时候，可以改变一些时间常数，便于观察
   2. 重点看第一个周期，和第二个周期的波形
   3. 起始条件和终止条件的波形
7. 管脚约束，时钟也要约束
8. 布线
9. 下载到板子
10. 如果运行过行为级仿真后，下载到板子功能还是不正常，那就加入ILA进行后仿真

不推荐使用ILA，因为加入ILA之后的运行速度会下降很多



20. Clk, rst_n, isEn, done_sig;

### 1.9.2. 2 时钟域的概念

不同时钟域的信号很重要

1. 相同时钟域：使用的是之前的电平。
2. 不同时钟域：使用的是电平触发。就是现在的电平是多少
3. 跨时钟域需要信号同步。
	1. 避免亚稳态。由setup和hold time决定

### 1.9.3. 3 rst_n后的状态

代码：复位之前输出0，复位之后输出1

1. Rst_n和clk上升沿不同步：正常模式![Screenshot-2019-12-25AM10.16.47](https://gitee.com/AndrewChu/markdown/raw/master/1599546601_Screenshot-2019-12-25AM10.16.47.png)
2. Rst_n和clk上升沿同步：当前电平触发![Screenshot-2019-12-25AM10.13.31](https://gitee.com/AndrewChu/markdown/raw/master/1599546600_Screenshot-2019-12-25AM10.13.31.png)
3. signal和clk不同步：正常模式![Screenshot-2019-12-25AM10.23.47](https://gitee.com/AndrewChu/markdown/raw/master/1599546601_Screenshot-2019-12-25AM10.23.47.png)
4. signal和clk同步：当前电平触发![Screenshot-2019-12-25AM10.23.10](https://gitee.com/AndrewChu/markdown/raw/master/1599546601_Screenshot-2019-12-25AM10.23.10.png)

### 1.9.4. 4 state machine 的初始状态

开启计时的时候是上一个状态，触发计时到后，马上关了计时使能。

```verilog
        case(state)
            sIdle:
                if(signal_in) begin
                    isCount <= 1;
                    state <= sDelay_1ms;
                    end
            sDelay_1ms:begin
                if(count_ms == T1ms)begin
                    state <= sStop;
                    isCount <= 0;
                end
            end
            sStop:begin
                state <= sIdle;
            end
        endcase
```



### 1.9.5. 为什么计时器要减1，T1ms=32'd50_000-1

1. 要分清楚是从0开始**维持**，还是1开始维持；
2. 得到最后一个周期要维持在那个数字，就确定了要不要减去1
3. 考虑下一个周期的初始条件

```verilog
`timescale 1 ns/1 ps
module H2L_edge
    (
        input clk, rst_n,
        input signal,
        input isCount
    );

    parameter  T100ns_5cycle = 32'd5;//从1开始维持，在5维持最后一个周期
    reg [31:0]count_5cycle;
    reg signal_out_5cycle;
    always @(posedge clk, negedge rst_n)
    begin
        if(rst_n == 0) begin
            count_5cycle <= 0;
            signal_out_5cycle <= 0;
        end
        else begin
            if(count_5cycle == T100ns_5cycle)
                begin
                    signal_out_5cycle <= 1;
                    count_5cycle <= 1;
                end
            else begin
                count_5cycle <= count_5cycle + 1;
                signal_out_5cycle <= 0;
                end
        end
    end


    parameter  T100ns_4cycle = 32'd5-1;//从0开始计时，在4维持最后一个周期
    reg [31:0]count_4cycle;
    reg signal_out_4cycle;
    always @(posedge clk, negedge rst_n)
    begin
        if(rst_n == 0) begin
            count_4cycle <= 0;
            signal_out_4cycle <= 0;
        end
        else begin
            if(isCount && count_4cycle == T100ns_4cycle) begin
                signal_out_4cycle <= 1;
                count_4cycle <= 0;
                end
            else if (isCount == 0) begin
                count_4cycle <= 0;
                signal_out_4cycle <= 0;
                end
            else begin
                count_4cycle <= count_4cycle + 1;
                signal_out_4cycle <= 0;
                end
        end
    end
endmodule : H2L_edge
```

![Screenshot-2019-12-25AM11.14.07](https://gitee.com/AndrewChu/markdown/raw/master/1599546602_Screenshot-2019-12-25AM11.14.07.png)

### 1.9.6. 6 为什么有的信号输入打一拍，有的信号要打两拍？

时钟域同步的，打一拍；时钟域不同步的，防止竞争冒险，要打两拍

![Screenshot-2019-12-25AM9.38.25](https://gitee.com/AndrewChu/markdown/raw/master/1599546602_Screenshot-2019-12-25AM9.38.25.png)

上图识别出下降沿。

![Screenshot-2019-12-25AM9.39.56](https://gitee.com/AndrewChu/markdown/raw/master/1599546603_Screenshot-2019-12-25AM9.39.56.png)

上图识别不出下降沿

### 1.9.7. 命名规范

- 文件：字母和下划线。文件名不要和信号重复
  - Vga_control_module
  - Sync_module
- 信号命名：
  - 常量：
    - T1s
    - T1ms
  - 变量：
    - Frame_sig
    - Counter_ms

###8 阻塞模式和非阻塞模式? 

1. 阻塞模式： =。一个一个赋值，用在assign里，
2. 非阻塞模式：<=。同时赋值，用在always里，防止竞争冒险

### 1.9.8. 9 三段式状态机？

不必强求三段式状态机，使用仿顺序操作的状态机更加方便理解

### 1.9.9. 仿顺序操作

使用case语句的状态跳转特性，实现上一个状态到下一个状态的顺序跳转。

```verilog
reg isCount;
parameter  T1ms = 32'd10-1;//从0开始计时，在4维持最后一个周期
reg [31:0] count_ms;
always @(posedge clk, negedge rst_n)
begin
    if(rst_n == 0) begin
        count_ms <= 0;
    end
    else begin
        if(isCount && count_ms == T1ms)
            count_ms <= 0;
        else if (isCount == 0) count_ms <= 0;
        else count_ms <= count_ms + 1;
    end
end

parameter sIdle = 0, sDelay_1ms =1, sStop=2;
reg [31:0] state;
always @(posedge clk, negedge rst_n)
begin
    if(rst_n == 0) begin
        state <= 0;
        isCount <=  0;
    end
    else begin
        case(state)
            sIdle:
                if(signal_in) begin
                    isCount <= 1;
                    state <= sDelay_1ms;
                    end
            sDelay_1ms:begin
                if(count_ms == T1ms)begin
                    state <= sStop;
                    isCount <= 0;
                end
            end
            sStop:begin
                state <= sIdle;
            end
        endcase
    end
end
```



### 1.9.10. 11 行为级仿真的注意点

1. 更新了代码之后，要relaunch，再restart
2. 增加/删除了信号之后，要relaunch，再restart。这时，仿真串口的信号要重新拖进来。





















