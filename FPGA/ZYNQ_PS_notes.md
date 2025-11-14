# 1. PS
## 1.1. 管脚约束
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546227_20200511160728060_2052416722.png =693x)
## 1.2. 常用头文件
```
#include "xparameters.h"
#include "xgpiops.h"
#include "xstatus.h"
#include "xplatform_info.h"
#include <xil_printf.h>

```
## 1.3. 常用函数
```
// 1.gpio poll mode
#define GPIO_DEVICE_ID  	XPAR_XGPIOPS_0_DEVICE_ID
XGpioPs Gpio;	/* The driver instance for GPIO Device. */
XGpioPs_Config *ConfigPtr;
/* Initialize the GPIO driver. */
ConfigPtr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);
Status = XGpioPs_CfgInitialize(&Gpio, ConfigPtr,
				ConfigPtr->BaseAddr);//给gpio结构体赋值
XGpioPs_SetDirectionPin(&Gpio, Output_Pin, 1);
XGpioPs_SetOutputEnablePin(&Gpio, Output_Pin, 1);
/* Set the GPIO output to be low. */
XGpioPs_WritePin(&Gpio, Output_Pin, 0x0);	
*DataRead = XGpioPs_ReadPin(&Gpio, Input_Pin);
```
## 1.4. MIO
poll方式的MIO的输入，输出

### 1.4.1. 关键函数
```
#include "xparameters.h"
#include "xgpiops.h"
#include <xil_printf.h>
#define GPIO_DEVICE_ID  	XPAR_XGPIOPS_0_DEVICE_ID
XGpioPs Gpio;	/* The driver instance for GPIO Device. */

int Status;
XGpioPs_Config *ConfigPtr;
Input_Pin = 12;
Output_Pin = 0;

/* Initialize the GPIO driver. */
ConfigPtr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);
Status = XGpioPs_CfgInitialize(&Gpio, ConfigPtr,
				ConfigPtr->BaseAddr);//给gpio结构体赋值
/*
 * 输出：
 * Set the direction for the pin to be output and
 * Enable the Output enable for the LED Pin.
 */
XGpioPs_SetDirectionPin(&Gpio, Output_Pin, 1);
XGpioPs_SetOutputEnablePin(&Gpio, Output_Pin, 1);
/* Set the GPIO output to be low. */
XGpioPs_WritePin(&Gpio, Output_Pin, 0x0);

/* 
 * 输入：
 * Set the direction for the specified pin to be input. */
XGpioPs_SetDirectionPin(&Gpio, Input_Pin, 0x0);
/* Read the state of the data so that it can be  verified. */
*DataRead = XGpioPs_ReadPin(&Gpio, Input_Pin);
```

## 1.5. EMIO
- EMIO不仅仅可以把让PS利用PL的IOB，还可以通过multiplex让PS使用PL的IP。
- EMIO一共有32*2个
- EMIO自动开始从54开始排列，一个IO一个IO的接上。在fpga端要进行管脚约束。

### 1.5.1. 完整代码
```
#include "xparameters.h"
#include "stdio.h"
#include "xgpiops.h"

#define GPIOPS_ID XPAR_XGPIOPS_0_DEVICE_ID
#define MIO_LED0 7
#define MIO_LED1 8
#define MIO_LED2 0
#define MIO_KEY0 12
#define MIO_KEY1 11
#define EMIO_KEY 54

int main() {
    printf("EMIO Test\n");
    XGpioPs gpiops_inst;
    XGpioPs_Config *gpiops_cfg_ptr;
    //初始化gpio结构体
    gpiops_cfg_ptr = XGpioPs_LookupConfig(GPIOPS_ID);
    XGpioPs_CfgInitialize(&gpiops_inst, gpiops_cfg_ptr, gpiops_cfg_ptr->BaseAddr);

    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_LED0, 1);
    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_LED1, 1);
    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_LED2, 1);

    XGpioPs_SetOutputEnablePin(&gpiops_inst, MIO_LED0, 1);
    XGpioPs_SetOutputEnablePin(&gpiops_inst, MIO_LED1, 1);
    XGpioPs_SetOutputEnablePin(&gpiops_inst, MIO_LED2, 1);

    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_KEY0, 0);
    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_KEY1, 0);
    XGpioPs_SetDirectionPin(&gpiops_inst, EMIO_KEY, 0);

    while(1){
        XGpioPs_WritePin(&gpiops_inst, MIO_LED0, 
        ~XGpioPs_ReadPin(&gpiops_inst,MIO_KEY0));
        
        XGpioPs_WritePin(&gpiops_inst, MIO_LED1, 
        ~XGpioPs_ReadPin(&gpiops_inst,MIO_KEY1));

        XGpioPs_WritePin(&gpiops_inst, MIO_LED2, 
        ~XGpioPs_ReadPin(&gpiops_inst,EMIO_KEY));
    }
    return 0;
}
```

## 1.6.  MIO interrupt
- 进行MIO的输入中断。
- 要理解GIC。
- 理解三个中断源
	- PPI：private peripheral interrupt
	- SGI：software generated interrupt
	- SPI：shared peripheral interrupt
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546228_20200511212758399_41549162.png)
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1599546229_20200511212913743_384580459.png)

### 1.6.1. 中断介绍
在Zynq SoC上处理中断
在Zynq SoC中发生中断时，处理器会采取以下措施：
1. 将中断显示为挂起；
2. 处理器停止执行当前线程；
3. 处理器在协议栈中保存线程状态，以便在中断处理后继续进行处理；
4. 处理器执行中断服务例程，其中定义了如何处理中断；
5. 在处理器从协议栈恢复之前，被中断的线程继续运行；

中断属于异步事件，因此可能同时发生多个中断。为了解决这一问题，处理器会对中断进行优先级排序，从而首先服务于优先级别最高的中断挂起。

为了正确实现这一中断结构，需要编写两个函数：一是中断服务例程，用于定义中断发生时的应对措施；二是用于配置中断的中断设置。中断设置例程可重复使用，允许构建不同的中断。该例程适用于系统中的所有中断，将针对通用I/O（GPIO）设置和使能中断。

### 1.6.2. 关键函数
```
#define GPIO_DEVICE_ID XPAR_XGPIOPS_0_DEVICE_ID
#define INTC_DEVICE_ID XPAR_SCUGIC_SINGLE_DEVICE_ID
#define GPIO_INTERRUPT_ID XPAR_XGPIOPS_0_INTR 
XGpioPs gpio;
XScuGic intc;
status = setup_interrupt_system(&intc, &gpio, GPIO_INTERRUPT_ID);
            XGpioPs_IntrClearPin(&gpio, KEY);
            XGpioPs_IntrEnablePin(&gpio, KEY);

// interrupt handler function
static void intr_hander(void *callback_ref){
    XGpioPs *gpio = (XGpioPs *) callback_ref;

    // judge key intr status
    if(XGpioPs_IntrGetStatusPin(gpio, KEY)){
        key_press = TRUE;
        xil_printf("enter interrupt handler!\r\n");
        XGpioPs_IntrDisablePin(gpio, KEY);
    }
}

int setup_interrupt_system(XScuGic *gic_ins_ptr, 
    XGpioPs *gpio, u16 gpio_intr_id){
    XScuGic_Config *IntcConfig;

    IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
    XScuGic_CfgInitialize(gic_ins_ptr, IntcConfig, 
        IntcConfig->CpuBaseAddress);
    
    //enable and setup interrupt exception
    Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
        (Xil_ExceptionHandler) XScuGic_InterruptHandler,gic_ins_ptr);
    Xil_ExceptionEnable();

    //setup interrupt handler
    XScuGic_Connect(gic_ins_ptr, gpio_intr_id,
        (Xil_ExceptionHandler) intr_hander, (void *) gpio);
    //enable gpio device interrupt
    XScuGic_Enable(gic_ins_ptr, gpio_intr_id);

    // interrupt type: falling edge
    XGpioPs_SetIntrTypePin(gpio, KEY, XGPIOPS_IRQ_TYPE_EDGE_FALLING);
    // enable key interrupt
    XGpioPs_IntrEnablePin(gpio, KEY);
    return XST_SUCCESS;
}

```
### 1.6.3. 完整代码
```
#include "xparameters.h"
#include "xgpiops.h"
#include "xscugic.h"
#include "xil_exception.h"
#include "xplatform_info.h"
#include "xil_printf.h"
#include "sleep.h"

#define GPIO_DEVICE_ID XPAR_XGPIOPS_0_DEVICE_ID
#define INTC_DEVICE_ID XPAR_SCUGIC_SINGLE_DEVICE_ID
#define GPIO_INTERRUPT_ID XPAR_XGPIOPS_0_INTR  

#define KEY 11
#define LED 0

static void intr_hander(void *callback_ref);
int setup_interrupt_system(XScuGic *gic_ins_ptr, 
    XGpioPs *gpio, u16 gpio_intr_id);


XGpioPs gpio;
XScuGic intc;
u32 key_press;
u32 key_val;


int main(int argc, char const *argv[])
{
    int status;
    XGpioPs_Config *ConfigPtr;

    xil_printf("gpio interrupt test!");
    
    ConfigPtr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);
    XGpioPs_CfgInitialize(&gpio, ConfigPtr, ConfigPtr->BaseAddr);

    XGpioPs_SetDirectionPin(&gpio, KEY, 0);
    XGpioPs_SetDirectionPin(&gpio, LED, 1);
    XGpioPs_SetOutputEnablePin(&gpio, LED, 1);
    XGpioPs_WritePin(&gpio, LED, 0x1);

    //setup interruption 
    status = setup_interrupt_system(&intc, &gpio, GPIO_INTERRUPT_ID);
    if (status != XST_SUCCESS){
        xil_printf("interrupt setup error!");
        return XST_FAILURE;
    }

    while (1)
    {
        if(key_press){
            usleep(20000);
            if (XGpioPs_ReadPin(&gpio, KEY)==0){
                key_val = ~key_val;
                XGpioPs_WritePin(&gpio, LED, key_val);
            }
            key_press = FALSE;
            XGpioPs_IntrClearPin(&gpio, KEY);
            XGpioPs_IntrEnablePin(&gpio, KEY);
        
        }
    }    
    return XST_SUCCESS;
}

// interrupt handler function
static void intr_hander(void *callback_ref){
    XGpioPs *gpio = (XGpioPs *) callback_ref;

    // judge key intr status
    if(XGpioPs_IntrGetStatusPin(gpio, KEY)){
        key_press = TRUE;
        xil_printf("enter interrupt handler!\r\n");
        XGpioPs_IntrDisablePin(gpio, KEY);
    }
}
int setup_interrupt_system(XScuGic *gic_ins_ptr, 
    XGpioPs *gpio, u16 gpio_intr_id){
    XScuGic_Config *IntcConfig;

    IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
    XScuGic_CfgInitialize(gic_ins_ptr, IntcConfig, 
        IntcConfig->CpuBaseAddress);
    
    //enable and setup interrupt exception
    Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
        (Xil_ExceptionHandler) XScuGic_InterruptHandler,gic_ins_ptr);
    Xil_ExceptionEnable();

    //setup interrupt handler
    XScuGic_Connect(gic_ins_ptr, gpio_intr_id,
        (Xil_ExceptionHandler) intr_hander, (void *) gpio);
    //enable gpio device interrupt
    XScuGic_Enable(gic_ins_ptr, gpio_intr_id);

    // interrupt type: falling edge
    XGpioPs_SetIntrTypePin(gpio, KEY, XGPIOPS_IRQ_TYPE_EDGE_FALLING);
    // enable key interrupt
    XGpioPs_IntrEnablePin(gpio, KEY);
    return XST_SUCCESS;
}
```

## 1.7. AXI GPIO
需要在PL端放置axi gpio模块，然后再在ps端调用
注意点：
axi gpio在ps端就是xgpio。ps端自带的gpio MIO是xgpiops。两者所有的函数都是不一样的。
- MIO：
	- 需要有cfgPtr，然后再initialization。
- AXI:
	- 直接initialization
	- 中断使能要两次
	- 因为axi gpio可以有两个，所以他有 channel，有mask
	- 所有的函数，包括配置和中断处理函数，都是不一样的

![](https://gitee.com/AndrewChu/markdown/raw/master/1599546239_20200516135900908_542281969.png)
### 1.7.1. 完整代码
```
#include "xparameters.h"
#include "xgpiops.h"
#include "xgpio.h"
#include "xscugic.h"
#include "xil_exception.h"
#include "xplatform_info.h"
#include "xil_printf.h"
#include "sleep.h"

#define SCUGIC_ID XPAR_SCUGIC_0_DEVICE_ID
#define GPIOPS_ID XPAR_XGPIOPS_0_DEVICE_ID
#define AXI_GPIO_ID XPAR_AXI_GPIO_0_DEVICE_ID
#define GPIO_INT_ID XPAR_FABRIC_GPIO_0_VEC_ID  

#define MIO_LED 0
#define KEY_CHANNEL 1
#define KEY_MASK XGPIO_IR_CH1_MASK

static void axi_gpio_handler(void *callback_ref);
void instance_init();

XScuGic scugic_inst;
XScuGic_Config *scugic_cfg_ptr;
XGpioPs gpiops_inst;
XGpioPs_Config *gpiops_cfg_ptr;
XGpio axi_gpio_inst;

int led_value = 1;


int main(int argc, char const *argv[])
{
    xil_printf("axi gpio test!");
    instance_init();

    XGpioPs_SetDirectionPin(&gpiops_inst, MIO_LED, 1);
    XGpioPs_SetOutputEnablePin(&gpiops_inst, MIO_LED, 1);
    XGpioPs_WritePin(&gpiops_inst, MIO_LED, led_value);   
    
    XGpio_SetDataDirection(&axi_gpio_inst, KEY_CHANNEL, 1);
    XGpio_InterruptEnable(&axi_gpio_inst,KEY_MASK);
    XGpio_InterruptGlobalEnable(&axi_gpio_inst);

    XScuGic_SetPriorityTriggerType(&scugic_inst, 
        GPIO_INT_ID, 0xA0, 0x1);
    XScuGic_Connect(&scugic_inst, GPIO_INT_ID, 
        axi_gpio_handler, &axi_gpio_inst);
    XScuGic_Enable(&scugic_inst, GPIO_INT_ID);
    //enable and setup interrupt exception
    Xil_ExceptionInit();
    Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
        (Xil_ExceptionHandler) XScuGic_InterruptHandler, &scugic_inst);
    Xil_ExceptionEnable();
    while (1){
    }
    return 0;
}   
    
 void instance_init(){
    scugic_cfg_ptr = XScuGic_LookupConfig(SCUGIC_ID);
    XScuGic_CfgInitialize(&scugic_inst, 
        scugic_cfg_ptr, scugic_cfg_ptr->CpuBaseAddress);
    
    gpiops_cfg_ptr = XGpioPs_LookupConfig(GPIOPS_ID);
    XGpioPs_CfgInitialize(&gpiops_inst, 
        gpiops_cfg_ptr, gpiops_cfg_ptr->BaseAddr);
    
    XGpio_Initialize(&axi_gpio_inst, AXI_GPIO_ID);
 }   

// interrupt handler function
static void axi_gpio_handler(void *callback_ref){
    int key_value = 1;
    XGpio *GpioPtr = (XGpio *) callback_ref;
    
    xil_printf("interrup trigged");
    XGpio_InterruptDisable(GpioPtr, KEY_MASK);
    key_value = XGpio_DiscreteRead(GpioPtr, KEY_CHANNEL);
    if(key_value == 0){
        led_value = ~led_value;
        XGpioPs_WritePin(&gpiops_inst,MIO_LED, led_value);
    }
    XGpio_InterruptClear(GpioPtr,KEY_MASK);
    XGpio_InterruptEnable(GpioPtr, KEY_MASK);
}
```
## 1.8. Customized IP
### 1.8.1. AXI简介
Interface Tpye（接口类型）：共三种接口类型可选，分别是 Lite、 Full 和 Stream。
- AXI4-Lite 接口是简化版的 AXI4 接口， 用于较少数据量的存储映射通信； 
- AXI4-Full 接口是高性能存储映射接口，用于较多数据量的存储映射通信；
- AXI4-Stream 用于高速数据流传输，非存储映射接口。本次实验只需少量数据的通信，
因此接口类型选择默认的 Lite 接口。
### 1.8.2. 创建IP
- 修改顶层的输入输出
- 修改顶层调用的输入输出
- 修改底层，加入对自己写的文件的调用。并且把寄存器分给对应的参数
- 生成ip
	- 可以对ip的参数类型，范围，初始值进行改动
	- 可以改变gui上的参数顺序
### 1.8.3. 关键函数

```
#include "breath_led_ip.h"
#define LED_IP_BASEADDR XPAR_BREATH_LED_IP_0_S0_AXI_BASEADDR
#define LED_IP_REG0 BREATH_LED_IP_S0_AXI_SLV_REG0_OFFSET
#define LED_IP_REG1 BREATH_LED_IP_S0_AXI_SLV_REG1_OFFSET
            BREATH_LED_IP_mWriteReg(LED_IP_BASEADDR, LED_IP_REG1, 0x800000ef);
            led_state = BREATH_LED_IP_mReadReg(LED_IP_BASEADDR, LED_IP_REG0);
       
```

### 1.8.4. 完整代码

```
#include "stdio.h"
#include "xparameters.h"
#include "breath_led_ip.h"
#include "xil_io.h"
#include "xil_printf.h"
#include "sleep.h"

#define LED_IP_BASEADDR XPAR_BREATH_LED_IP_0_S0_AXI_BASEADDR
#define LED_IP_REG0 BREATH_LED_IP_S0_AXI_SLV_REG0_OFFSET
#define LED_IP_REG1 BREATH_LED_IP_S0_AXI_SLV_REG1_OFFSET

int main(int argc, char const *argv[])
{
    int freq_flag;
    int led_state;
    xil_printf("test customized ip!");

    while (1){
        if(freq_flag == 0){
            BREATH_LED_IP_mWriteReg(LED_IP_BASEADDR, 
                LED_IP_REG1, 0x800000ef);
            freq_flag = 1;
        }else
        {
            BREATH_LED_IP_mWriteReg(LED_IP_BASEADDR,
                LED_IP_REG1, 0x8000002f);
            freq_flag = 0;
        }
        led_state = BREATH_LED_IP_mReadReg(LED_IP_BASEADDR, LED_IP_REG0);
        if(led_state == 0){
            BREATH_LED_IP_mWriteReg(LED_IP_BASEADDR, LED_IP_REG0, 1);
            xil_printf("led on\n");
        }
        sleep(5);

        led_state = BREATH_LED_IP_mReadReg(LED_IP_BASEADDR, LED_IP_REG0);
        if(led_state ==1 ){
            BREATH_LED_IP_mWriteReg(LED_IP_BASEADDR,LED_IP_REG0,0);
            xil_printf("led off!\n");
        }    
        sleep(1);
    }
    return 0;
}   
```
## 1.9. 程序固化
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546229_20200512222956589_866569160.png =785x)
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546231_20200512223025395_193778166.png =785x)
1. BootROM 
2. 总结一下 FSBL 的工作内容：
	1. 初始化 PS；
	2. 如果提供了 BIT 文件，则配置 PL；
	3. 加载裸机应用程序到 DDR 中，或者加载 Second-Stage Boot Loader（ SSBL）；
	4. 开始执行裸机应用程序，或者 SSBL。

要重建一个 ZYNQ 的启动镜像我们需要执行以下文件：
1、 Boot ROM 头文件：控制 Boot ROM 设置，比如就地执行、 加密、 FSBL 偏移量、镜像文件大小等；
2、 First-Stage Boot Loader；
3、 PL 配置文件， 即 BIT 文件；
4、 运行在 PS 上的软件应用程序
### 1.9.1. 步骤
1. PL端开启sd卡和qspi的外设
2. 在PS端，对应的bsp里开启 ffs功能
3. 再在boot image里填入
	1. boot.bin生成的路径
	2. fsbl.elf 
	3. .bit
	4. .elf
	5. 以上三个生成文件的顺序也不能乱
6. 烧录sd卡
	1. 直接把bin文件复制进去，注意sd卡的文件格式要是fat32的
	2. 选择sd卡启动方式
1. 烧录qspi
	1. 在sdk里选着烧录flash。
	2. 每次都失败，可能有bug

## 1.10. UART
- 通过AXI总线，挂到APB总线
	- txfifo
		- 空标志位
		- 满标志位
	- rxfifo
		- 空标准
		- 满标准
- 寄存器
	- 控制寄存器 cr
	- 状态寄存器 sr
	- 波特率发生器 baudrate
	- 中断处理 GIC
- 四种模式
	- normal
	- automatic echo
	- local loopback	常用，可以排除是硬件问题
	- remote loopbacl
- 采用中断方法发送数据的顺序如下：
	- 禁用 TxFIFO 空中断；
	- 向 TxFIFO 写数据，可以写入 64 个字节的数据；
	- 检测 TxFIFO 是否为满状态，不停的读取 TFUL 标志和写单个字节的数据；
	- 重复步骤 2 和 3，直到 TxFIFO 已满；
	- 使能 TxFIFO 空中断；等待，直到 TxFIFO 为空，然后从步骤 1 重新开始；
- 采用中断方法接收数据的顺序如下：
	- 使能中断；
	- 等待，直到 RxFIFO 中的数据数量达到触发等级或者发生超时；
	- 从 RxFIFO 中读取数据；
	- 重复步骤 2 和 3，直到 RxFIFO 为空；
	- 清除中断标志。
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546232_20200512223055600_1244427110.png =761x)
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546233_20200512223108516_743199637.png =761x)
### 1.10.1. 关键函数
- 任何一个设备，先要区分是哪个cpu的，那号设备
- 要理解几个缩写
	- mr mask reg
	- sr status reg
	- cr control reg
	- er enable reg
	- dr disable reg
- 理解sr的wtc
	- wtc 是write to clear，
	- 可以先从status reg读完状态，然后对应位写个1，就清除了这个sr。
### 1.10.2. 完整代码

```
#include "xparameters.h"
#include "xuartps.h"
#include "xil_printf.h"
#include "xscugic.h"
#include "stdio.h"

#define INTC_DEVICE_ID XPAR_SCUGIC_SINGLE_DEVICE_ID // which cpu 0/1
#define UART_INT_IRQ_ID XPAR_XUARTPS_0_INTR         // which interrupt device
#define UART_DEVICE_ID XPAR_PS7_UART_0_DEVICE_ID // which uart 0/1

XScuGic Intc;
XUartPs Uart_ps;

int uart_init(XUartPs *uart_ps){
    int status;
    XUartPs_Config *uart_cfg;
    uart_cfg = XUartPs_LookupConfig(UART_DEVICE_ID);
    status = XUartPs_CfgInitialize(uart_ps, 
        uart_cfg, uart_cfg->BaseAddress);
    XUartPs_SelfTest(uart_ps);

    //uart mode set
    XUartPs_SetOperMode(uart_ps, XUARTPS_OPER_MODE_NORMAL);
    XUartPs_SetBaudRate(uart_ps, 115200);
    XUartPs_SetFifoThreshold(uart_ps, 1);
    return 0;
}

int uart_intr_handler(void *call_back_ref){
    XUartPs *uart_instance_ptr = call_back_ref;
    u32 rec_data = 0;
    u32 isr_status;//interrupt status register

    isr_status = XUartPs_ReadReg(uart_instance_ptr->Config.BaseAddress,
        XUARTPS_IMR_OFFSET);
    isr_status &= XUartPs_ReadReg(uart_instance_ptr->Config.BaseAddress,
        XUARTPS_ISR_OFFSET);

    // judge intr triggered?
    if(isr_status &(u32)XUARTPS_IXR_RXOVR){
        rec_data = XUartPs_RecvByte(XPAR_PS7_UART_0_BASEADDR);
        XUartPs_WriteReg(uart_instance_ptr->Config.BaseAddress,
            XUARTPS_ISR_OFFSET, XUARTPS_IXR_RXOVR);
        XUartPs_SendByte(XPAR_XUARTPS_0_BASEADDR, rec_data);
    }
    return 0;
}

int uart_intr_init(XScuGic *intc, XUartPs *uart_ps){
    int status;
    XScuGic_Config *intc_cfg;
    intc_cfg = XScuGic_LookupConfig(INTC_DEVICE_ID);
    XScuGic_CfgInitialize(intc, intc_cfg, intc_cfg->CpuBaseAddress);
    //setup exception handler
    Xil_ExceptionInit();
    Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
        (Xil_ExceptionHandler)XScuGic_InterruptHandler, (void *)intc);
    Xil_ExceptionEnable();
    //connect intr handler func
    XScuGic_Connect(intc, UART_INT_IRQ_ID,
        (Xil_ExceptionHandler) uart_intr_handler, (void *) uart_ps);
    //setup intr trigger mode
    XUartPs_SetInterruptMask(uart_ps, XUARTPS_IXR_RXOVR);
    XScuGic_Enable(intc, UART_INT_IRQ_ID);
    return 0;
}


int main(int argc, char const *argv[])
{
    int status;

    uart_init(&Uart_ps);
    uart_intr_init(&Intc, &Uart_ps);
    while(1);

    return 0;
}
```




## 1.11. 定时器
Zynq SoC拥有许多可用的定时器和看门狗监视器。它们既可作为一个CPU的专用资源也可作为两个CPU的共享资源。如需在您的设计中高效利用这些组件，则需要中断。这些定时器和看门狗监视器包括：
 CPU 32位定时器（SCUTIMER），以CPU频率的一半计时
 CPU 32位看门狗监视器（SCUWDT），以CPU频率的一半计时
 共享64位全局定时器（GT），以CPU频率的一半计时（每个CPU都有其自己的64位比较器；它与GT配合使用，能驱动各个CPU的专用中断）
 系统看门狗监视时钟（WDT），可通过CPU时钟或外部来源进行计时
 一对三重定时器计数器（TTC），每个包含三个独立定时器。在可编程逻辑中，可通过CPU时钟或来自MIO或EMIO的外部来源对TTC进行计时。


定时器本身通过以下四个寄存器来控制：
 专用定时器加载寄存器 – 可将该寄存器用于自动重新加载模式，包含在使能自动重新加载时被重新加载到专用定时器计数器寄存器中的数值。
 专用定时计数寄存器 (Private Timer Counter Register) – 这是真实计数器本身。使能后，一旦寄存器达到零，则会设置中断事件标志。
 专用定时器控制寄存器 – 控制寄存器可使能或禁用定时器、自动重新加载模式以及中断生成，还包含定时器的预分频器。
 专用定时器中断状态寄存器 – 该寄存器包含专用定时器中断状态事件标志。

私有定时器的时钟频率为 CPU 时钟频率的一半，如 ARM 的工作时钟频率为 666.666Mhz，则私有定时
器的时钟频率为 333.333Mhz。私有定时器的特性如下：
1、 32 位计数器，当计数器递减至 0 后产生中断；
2、 8 位预分频计数器，可以更好的控制中断周期；
3、可以配置单次定时或者自动重载模式；
4、通过配置起始计数值来设置定时时间。
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546233_20200513110323149_1337329230.png =761x)

### 1.11.1. 完整代码
```
#include "xparameters.h"
#include "xscutimer.h"
#include "xscugic.h"
#include "xgpiops.h"
#include "xil_printf.h"

#define TIMER_DEVICE_ID XPAR_XSCUTIMER_0_DEVICE_ID
#define INTC_DEVICE_ID XPAR_SCUGIC_SINGLE_DEVICE_ID
#define TIMER_IRPT_INTR XPAR_SCUTIMER_INTR
#define GPIO_DEVICE_ID XPAR_XGPIOPS_0_DEVICE_ID
#define MIO_LED        0
#define TIMER_LOAD_VALUE 0x3F83C3F //定时器重装载值

XScuGic Intc;
XGpioPs Gpio;
XScuTimer Timer;

//mio管脚初始化
int mio_init(XGpioPs *mio_ptr){
    int status;

    XGpioPs_Config *mio_cfg_ptr;
    mio_cfg_ptr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);
    XGpioPs_CfgInitialize(mio_ptr, mio_cfg_ptr, mio_cfg_ptr->BaseAddr);
    XGpioPs_SetDirectionPin(mio_ptr, MIO_LED, 1);//输出模式
    XGpioPs_SetOutputEnablePin(mio_ptr, MIO_LED, 1);
    return 1;
}

//定时器初始化程序
void timer_init(XScuTimer *timer_ptr){
    int status;
    XScuTimer_Config *timer_cfg_ptr;
    timer_cfg_ptr = XScuTimer_LookupConfig(TIMER_DEVICE_ID);
    XScuTimer_CfgInitialize(timer_ptr, timer_cfg_ptr, timer_cfg_ptr->BaseAddr);
    XScuTimer_LoadTimer(timer_ptr, TIMER_LOAD_VALUE);
    XScuTimer_EnableAutoReload(timer_ptr);
}

//定时器中断处理函数
void timer_intr_handler(void *CallBackRef){
    static int led_status = 0;
    XScuTimer *timer_ptr  = CallBackRef;
    xil_printf("enter intr");
    if(led_status==0)
        led_status =1;
    else
        led_status =0;
    
    XGpioPs_WritePin(&Gpio, MIO_LED, led_status);
    XScuTimer_ClearInterruptStatus(timer_ptr);

}

//setup timer with intc
void timer_intr_init(XScuGic *intc_ptr, XScuTimer *timer_ptr){
    //initialize intc
    XScuGic_Config *intc_cfg_ptr;
    intc_cfg_ptr = XScuGic_LookupConfig(INTC_DEVICE_ID);
    XScuGic_CfgInitialize(intc_ptr, intc_cfg_ptr, intc_cfg_ptr->CpuBaseAddress);
    Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
        (Xil_ExceptionHandler)XScuGic_InterruptHandler, intc_ptr);
    Xil_ExceptionEnable();

    XScuGic_Connect(intc_ptr, TIMER_IRPT_INTR, 
        (Xil_ExceptionHandler)timer_intr_handler, (void *)timer_ptr);
    XScuGic_Enable(intc_ptr, TIMER_IRPT_INTR);
    XScuTimer_EnableInterrupt(timer_ptr);
}

int main() {
    int status;
    xil_printf("timer interrupt test!");
    
    mio_init(&Gpio);
    timer_init(&Timer);
    timer_intr_init(&Intc, &Timer);
    XScuTimer_Start(&Timer);
    while (1);
    return 0;
}
```

## 1.12. XADC
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546234_20200513201725445_125107223.png =704x)

### 1.12.1. 完整代码
```
#include "xparameters.h"
#include "xil_printf.h"
#include "xadcps.h"
#include "stdio.h"
#include "sleep.h"

#define XADC_DEVICE_ID XPAR_XADCPS_0_DEVICE_ID

static XAdcPs Xadc_inst;

void xadc_init(void){
    XAdcPs_Config *xadc_cfg_ptr;
    xadc_cfg_ptr = XAdcPs_LookupConfig(XADC_DEVICE_ID);
    XAdcPs_CfgInitialize(&Xadc_inst, xadc_cfg_ptr,xadc_cfg_ptr->BaseAddress);

    XAdcPs_SetSequencerMode(&Xadc_inst, XADCPS_SEQ_MODE_SAFE);
}

int main() {
    int status;

    u32 temp_rawdata;
    u32 vcc_pint_rawdata;
    u32 vcc_int_rawdata;
    u32 vcc_pddr_rawdata;
    u32 vcc_bram_rawdata;

    float temp;
    float vcc_pint;
    float vcc_int;
    float vcc_pddr;
    float vcc_bram;
    
    xil_printf("xadc test!");
    xadc_init();

    while (1){
        temp_rawdata = XAdcPs_GetAdcData(&Xadc_inst, XADCPS_CH_TEMP);
        temp = XAdcPs_RawToTemperature(temp_rawdata);

        vcc_pint_rawdata = XAdcPs_GetAdcData(&Xadc_inst, XADCPS_CH_VCCPINT);
        vcc_pint = XAdcPs_RawToVoltage(vcc_pint_rawdata);

        vcc_int_rawdata = XAdcPs_GetAdcData(&Xadc_inst, XADCPS_CH_VCCINT);
        vcc_int = XAdcPs_RawToVoltage(vcc_int_rawdata);

        vcc_pddr_rawdata = XAdcPs_GetAdcData(&Xadc_inst, XADCPS_CH_VCCPDRO);
        vcc_pddr = XAdcPs_RawToVoltage(vcc_pddr_rawdata);

        vcc_bram_rawdata = XAdcPs_GetAdcData(&Xadc_inst, XADCPS_CH_VBRAM);
        vcc_bram = XAdcPs_RawToVoltage(vcc_bram_rawdata);

        printf("raw temp: %lu, real temp %f C\n", temp_rawdata, temp);
        printf("raw VCCPINT: %lu, real VCCPINT %f V\n", vcc_pint_rawdata, vcc_pint);
        printf("raw VCCINT: %lu, real VCCINT %f V\n", vcc_int_rawdata, vcc_int);
        printf("raw VCCPddr: %lu, real VCCPddr %f V\n", vcc_pddr_rawdata, vcc_pddr);
        printf("raw VCCbram: %lu, real VCCbram %f V\n", vcc_bram_rawdata, vcc_bram);
        
        sleep(5);
    }
    return 0;
}
```


## 1.13. QSPI
- 型号：
	- w25q256：
		- 256Mb
			- page 256B。 131k个
			- sector 16个page。4KB大小
			- block 16个sector。64KB大小
		- qspi通信
			- sck最高到100Mhz
			- 在rising edge 读数据，在falling edge 写数据
		- 3字节地址/4字节地址
			- 3字节的地址，最多存16M*8=128Mb的数据，
			- 为了让flash的容量更大，就要用4字节地址的
			- 老的器件只支持3字节，这个也就是为什么我用qspi固化程序失败的原因
	- at24c64:
		- 64Mb
			- 8000*8bit
				- 4*8bit 是一个page
		- iic通信
			- 要在高电平保持不变

![](https://gitee.com/AndrewChu/markdown/raw/master/1599546236_20200516135749798_1283063640.png =752x)
![](https://gitee.com/AndrewChu/markdown/raw/master/1599546238_20200516135805255_1567297953.png =752x)