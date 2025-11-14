# 1. SDK-use-note

## 1.1. Basic

### 1.1.1. BSP

| category | Name   | Pin   | NOTE                   |
| -------- | ------ | ----- | ---------------------- |
| PS       | LED1-2 | 0 13  |                        |
| PS       | KEY1-2 | 50 51 | 注意选择block电压 1.8V |
|          |        |       |                        |



### 1.1.2. Vivado setting

![Screenshot-2019-11-04AM11.00.08](https://gitee.com/AndrewChu/markdown/raw/master/1599546825_Screenshot-2019-11-04AM11.00.08.png)

![Screenshot-2019-11-04AM11.11.21](https://gitee.com/AndrewChu/markdown/raw/master/1599546826_Screenshot-2019-11-04AM11.11.21.png)

![Screenshot-2019-11-04AM11.15.55](https://gitee.com/AndrewChu/markdown/raw/master/1599546827_Screenshot-2019-11-04AM11.15.55.png)

### 1.1.3. C basics

```c
# if
if (a==1){
		b=1;
}
else if (a==2){
		b=2;
}
```



```c
# while
while(1){
		printf("dead loop ");
}
```



```c
# switch
switch(ITEM){
		case 1:
				a=1;
				break;
    case 2:
    		a=2;
    		break;
}
```



## 1.2. 01_LED

### 1.2.1. Vivado

```verilog
`timescale 1ns / 1ps
module led(
    input sys_clk,
    input rst_n,
    (* MARK_DEBUG="true" *)  output reg [3:0] led
);
(* MARK_DEBUG="true" *) reg[31:0] timer_cnt;
always@(posedge sys_clk or negedge rst_n)
    begin
    if (!rst_n)
        begin
        led <= 4'd0 ;
        timer_cnt <= 32'd0 ;
        end
    else if(timer_cnt >= 32'd49_999_999)
        begin
        led <= ~led;
        timer_cnt <= 32'd0;
        end
    else
        begin
        led <= led;
        timer_cnt <= timer_cnt + 32'd1;
        end
    end
endmodule

```

### 1.2.2. SDK

No content

## 1.3. 02_HDMI

## 1.4. 03_ps_hello

### 1.4.1. vivado

> 1. Place ZYNQ IP core, and configure it

![Screenshot-2019-11-04AM11.26.55](https://gitee.com/AndrewChu/markdown/raw/master/1599546828_Screenshot-2019-11-04AM11.26.55.png)![Screenshot-2019-11-04AM11.27.25](https://gitee.com/AndrewChu/markdown/raw/master/1599546829_Screenshot-2019-11-04AM11.27.25.png)

![Screenshot-2019-11-04AM11.25.30](https://gitee.com/AndrewChu/markdown/raw/master/1599546828_Screenshot-2019-11-04AM11.25.30.png)、

### 1.4.2. SDK

![Screenshot-2019-11-04PM12.25.44](https://gitee.com/AndrewChu/markdown/raw/master/1599546830_Screenshot-2019-11-04PM12.25.44.png)

Short cut for locat function: `cmd+f`

## 1.5. 04_ps_timer

使用ps端的私有定时器，控制ps端的led。

因为所有外设都是ps的，所有fpga端不用constrain IO，只需要把ARM的硬核拖出来配置好。

### 1.5.1. vivado

![Screenshot-2019-11-04PM12.34.32](https://gitee.com/AndrewChu/markdown/raw/master/1599546830_Screenshot-2019-11-04PM12.34.32.png)



### 1.5.2. SDK

refer to the attached source code

```C

#include "xparameters.h"
#include "xscutimer.h"
#include "xscugic.h"
#include "xil_exception.h"
#include "xil_printf.h"

/************************** Constant Definitions *****************************/

/*
 * The following constants map to the XPAR parameters created in the
 * xparameters.h file. They are only defined here such that a user can easily
 * change all the needed parameters in one place.
 */
#ifndef TESTAPP_GEN
#define TIMER_DEVICE_ID		XPAR_XSCUTIMER_0_DEVICE_ID
#define INTC_DEVICE_ID		XPAR_SCUGIC_SINGLE_DEVICE_ID
#define TIMER_IRPT_INTR		XPAR_SCUTIMER_INTR
#endif

#define TIMER_LOAD_VALUE	XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ/2-1

/**************************** Type Definitions *******************************/

/***************** Macros (Inline Functions) Definitions *********************/

/************************** Function Prototypes ******************************/

int ScuTimerIntrExample(XScuGic *IntcInstancePtr, XScuTimer *TimerInstancePtr,
			u16 TimerDeviceId, u16 TimerIntrId);

static void TimerIntrHandler(void *CallBackRef);

static int TimerSetupIntrSystem(XScuGic *IntcInstancePtr,
				XScuTimer *TimerInstancePtr, u16 TimerIntrId);

static void TimerDisableIntrSystem(XScuGic *IntcInstancePtr, u16 TimerIntrId);

/************************** Variable Definitions *****************************/

#ifndef TESTAPP_GEN
XScuTimer TimerInstance;	/* Cortex A9 Scu Private Timer Instance */
XScuGic IntcInstance;		/* Interrupt Controller Instance */
#endif

/*
 * The following variables are shared between non-interrupt processing and
 * interrupt processing such that they must be global.
 */
volatile int TimerExpired;

/*****************************************************************************/
/**
* Main function to call the Cortex A9 Scu Private Timer interrupt example.
*
* @param	None.
*
* @return	XST_SUCCESS if successful, otherwise XST_FAILURE.
*
* @note		None.
*
******************************************************************************/
#ifndef TESTAPP_GEN
int main(void)
{
	int Status;

	xil_printf("SCU Timer Interrupt Example Test \r\n");

	/*
	 * Call the interrupt example, specify the parameters generated in
	 * xparameters.h
	 */
	Status = ScuTimerIntrExample(&IntcInstance, &TimerInstance,
				TIMER_DEVICE_ID, TIMER_IRPT_INTR);
	if (Status != XST_SUCCESS) {
		xil_printf("SCU Timer Interrupt Example Test Failed\r\n");
		return XST_FAILURE;
	}

	xil_printf("Successfully ran SCU Timer Interrupt Example Test\r\n");
	return XST_SUCCESS;
}
#endif

/*****************************************************************************/
/**
*
* This function tests the functioning of the Cortex A9 Scu Private Timer driver
* and hardware using interrupts.
*
* @param	IntcInstancePtr is a pointer to the instance of XScuGic driver.
* @param	TimerInstancePtr is a pointer to the instance of XScuTimer
*		driver.
* @param	TimerDeviceId is the Device ID of the XScuTimer device.
* @param	TimerIntrId is the Interrupt Id of the XScuTimer device.
*
* @return	XST_SUCCESS if successful, otherwise XST_FAILURE.
*
* @note		None.
*
******************************************************************************/
int ScuTimerIntrExample(XScuGic *IntcInstancePtr, XScuTimer * TimerInstancePtr,
			u16 TimerDeviceId, u16 TimerIntrId)
{
	int Status;
	int LastTimerExpired = 0;
	XScuTimer_Config *ConfigPtr;

	/*
	 * Initialize the Scu Private Timer driver.
	 */
	ConfigPtr = XScuTimer_LookupConfig(TimerDeviceId);

	/*
	 * This is where the virtual address would be used, this example
	 * uses physical address.
	 */
	Status = XScuTimer_CfgInitialize(TimerInstancePtr, ConfigPtr,
					ConfigPtr->BaseAddr);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}

	/*
	 * Perform a self-test to ensure that the hardware was built correctly.
	 */
	Status = XScuTimer_SelfTest(TimerInstancePtr);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}

	/*
	 * Connect the device to interrupt subsystem so that interrupts
	 * can occur.
	 */
	Status = TimerSetupIntrSystem(IntcInstancePtr,
					TimerInstancePtr, TimerIntrId);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}

	/*
	 * Enable Auto reload mode.
	 */
	XScuTimer_EnableAutoReload(TimerInstancePtr);

	/*
	 * Load the timer counter register.
	 */
	XScuTimer_LoadTimer(TimerInstancePtr, TIMER_LOAD_VALUE);

	/*
	 * Start the timer counter and then wait for it
	 * to timeout a number of times.
	 */
	XScuTimer_Start(TimerInstancePtr);

	while (1) {
		/*
		 * Wait for the first timer counter to expire as indicated by
		 * the shared variable which the handler will increment.
		 */
		while (TimerExpired == LastTimerExpired) {
		}

		LastTimerExpired = TimerExpired;
		/*
		 * If it has expired a number of times, then stop the timer
		 * counter and stop this example.
		 */
		if (TimerExpired == 9) {
			XScuTimer_Stop(TimerInstancePtr);
			break;
		}
	}
	/*
	 * Disable and disconnect the interrupt system.
	 */
	TimerDisableIntrSystem(IntcInstancePtr, TimerIntrId);

	return XST_SUCCESS;
}

/*****************************************************************************/
/**
*
* This function sets up the interrupt system such that interrupts can occur
* for the device.
*
* @param	IntcInstancePtr is a pointer to the instance of XScuGic driver.
* @param	TimerInstancePtr is a pointer to the instance of XScuTimer
*		driver.
* @param	TimerIntrId is the Interrupt Id of the XScuTimer device.
*
* @return	XST_SUCCESS if successful, otherwise XST_FAILURE.
*
* @note		None.
*
******************************************************************************/
static int TimerSetupIntrSystem(XScuGic *IntcInstancePtr,
			      XScuTimer *TimerInstancePtr, u16 TimerIntrId)
{
	int Status;

#ifndef TESTAPP_GEN
	XScuGic_Config *IntcConfig;

	/*
	 * Initialize the interrupt controller driver so that it is ready to
	 * use.
	 */
	IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
	if (NULL == IntcConfig) {
		return XST_FAILURE;
	}

	Status = XScuGic_CfgInitialize(IntcInstancePtr, IntcConfig,
					IntcConfig->CpuBaseAddress);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}


	Xil_ExceptionInit();



	/*
	 * Connect the interrupt controller interrupt handler to the hardware
	 * interrupt handling logic in the processor.
	 */
	Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_IRQ_INT,
				(Xil_ExceptionHandler)XScuGic_InterruptHandler,
				IntcInstancePtr);
#endif

	/*
	 * Connect the device driver handler that will be called when an
	 * interrupt for the device occurs, the handler defined above performs
	 * the specific interrupt processing for the device.
	 */
	Status = XScuGic_Connect(IntcInstancePtr, TimerIntrId,
				(Xil_ExceptionHandler)TimerIntrHandler,
				(void *)TimerInstancePtr);
	if (Status != XST_SUCCESS) {
		return Status;
	}

	/*
	 * Enable the interrupt for the device.
	 */
	XScuGic_Enable(IntcInstancePtr, TimerIntrId);

	/*
	 * Enable the timer interrupts for timer mode.
	 */
	XScuTimer_EnableInterrupt(TimerInstancePtr);

#ifndef TESTAPP_GEN
	/*
	 * Enable interrupts in the Processor.
	 */
	Xil_ExceptionEnable();
#endif

	return XST_SUCCESS;
}

/*****************************************************************************/
/**
*
* This function is the Interrupt handler for the Timer interrupt of the
* Timer device. It is called on the expiration of the timer counter in
* interrupt context.
*
* @param	CallBackRef is a pointer to the callback function.
*
* @return	None.
*
* @note		None.
*
******************************************************************************/
static void TimerIntrHandler(void *CallBackRef)
{
	XScuTimer *TimerInstancePtr = (XScuTimer *) CallBackRef;

	/*
	 * Check if the timer counter has expired, checking is not necessary
	 * since that's the reason this function is executed, this just shows
	 * how the callback reference can be used as a pointer to the instance
	 * of the timer counter that expired, increment a shared variable so
	 * the main thread of execution can see the timer expired.
	 */
	if (XScuTimer_IsExpired(TimerInstancePtr)) {
		XScuTimer_ClearInterruptStatus(TimerInstancePtr);
		TimerExpired++;
		xil_printf("%d times\r\n",TimerExpired);
		if (TimerExpired == 9) {
			XScuTimer_DisableAutoReload(TimerInstancePtr);
		}
	}
}

/*****************************************************************************/
/**
*
* This function disables the interrupts that occur for the device.
*
* @param	IntcInstancePtr is the pointer to the instance of XScuGic
*		driver.
* @param	TimerIntrId is the Interrupt Id for the device.
*
* @return	None.
*
* @note		None.
*
******************************************************************************/
static void TimerDisableIntrSystem(XScuGic *IntcInstancePtr, u16 TimerIntrId)
{
	/*
	 * Disconnect and disable the interrupt for the Timer.
	 */
	XScuGic_Disconnect(IntcInstancePtr, TimerIntrId);
}
```



## 1.6. 05_ps_gpio

1. PS GPIO input/output
2. PS GPIO  interuput mode
3. PL GPIO input/output
4. PL GPIO  interuput mode
5. PL GPIO EMIO (TBD)

PS端的管脚约束已经自带，只要修改PL的IO constrain

### 1.6.1. vivado

只需要约束PL端的IO，PS端的IO在配置ZYNQ的时候已经会自动生成了

![Screenshot-2019-11-04PM2.39.20](https://gitee.com/AndrewChu/markdown/raw/master/1599546831_Screenshot-2019-11-04PM2.39.20.png)

### 1.6.2. SDK

1. PS GPIO input/output
2. PS GPIO  interrupt mode
3. AXI GPIO input/output
4. AXI GPIO  interrupt mode

#### 1.6.2.1. PS GPIO input/output

```c
/* PS GPIO input/output */

#include "xparameters.h"
#include "xgpiops.h"
#include "xil_printf.h"
//#include "xscugic.h"
//#include "xil_exception.h"
#include "sleep.h"

/* GPIO paramter */
#define MIO_0_DEVICE_ID        XPAR_PS7_GPIO_0_DEVICE_ID
#define INTC_DEVICE_ID	XPAR_SCUGIC_SINGLE_DEVICE_ID
#define KEY_INTR_ID     XPAR_XGPIOPS_0_INTR
#define GPIO_INPUT      0
#define GPIO_OUTPUT     1

XGpioPs GPIO_PTR ;
//XScuGic INTCInst;
int main(){
	int led_status=0x1;
	XGpioPs_Config *GPIO_CONFIG ;
	// GPIO driver init
	GPIO_CONFIG = XGpioPs_LookupConfig(MIO_0_DEVICE_ID) ;
	XGpioPs_CfgInitialize(&GPIO_PTR, GPIO_CONFIG, GPIO_CONFIG->BaseAddr) ;
	//set MIO 0 as output
	XGpioPs_SetDirectionPin(&GPIO_PTR, 0, GPIO_OUTPUT) ;
	//enable MIO 0 output
	XGpioPs_SetOutputEnablePin(&GPIO_PTR, 0, GPIO_OUTPUT) ;
	XGpioPs_WritePin(&GPIO_PTR, 0, 0x1) ;

	//set MIO 50 as input
	XGpioPs_SetDirectionPin(&GPIO_PTR, 50, GPIO_INPUT) ;
	XGpioPs_ReadPin(&GPIO_PTR,50) ;
	while(1){
		xil_printf("%d",XGpioPs_ReadPin(&GPIO_PTR,50));
		led_status = ~led_status;
		XGpioPs_WritePin(&GPIO_PTR, 0, led_status) ;
		sleep(1);
	}
}

```

#### 1.6.2.2. PS GPIO  interrupt mode

```c
/* PS GPIO input interrupt */
#include "xparameters.h"
#include "xgpiops.h"
#include "xil_printf.h"
#include "xscugic.h"
#include "xil_exception.h"
#include "sleep.h"

/* GPIO paramter */
#define MIO_0_DEVICE_ID        XPAR_PS7_GPIO_0_DEVICE_ID
#define INTC_DEVICE_ID	XPAR_SCUGIC_SINGLE_DEVICE_ID
#define KEY_INTR_ID     XPAR_XGPIOPS_0_INTR
#define GPIO_INPUT      0
#define GPIO_OUTPUT     1
int key_flag;

void my_IntrInitFuntion(XScuGic *InstancePtr , u16 DeviceId, XGpioPs *GpioInstancePtr);
void my_GpioHandler(void *CallbackRef);

XGpioPs GPIO_PTR ;
XScuGic INTCInst;
int main(){
	int led_status=0x1;
	XGpioPs_Config *GPIO_CONFIG ;
	// GPIO driver init
	GPIO_CONFIG = XGpioPs_LookupConfig(MIO_0_DEVICE_ID) ;
	XGpioPs_CfgInitialize(&GPIO_PTR, GPIO_CONFIG, GPIO_CONFIG->BaseAddr) ;
	//set MIO 0 as output
	XGpioPs_SetDirectionPin(&GPIO_PTR, 0, GPIO_OUTPUT) ;
	//enable MIO 0 output
	XGpioPs_SetOutputEnablePin(&GPIO_PTR, 0, GPIO_OUTPUT) ;
	XGpioPs_WritePin(&GPIO_PTR, 0, 0x1) ;

	XGpioPs_SetDirectionPin(&GPIO_PTR, 13, GPIO_OUTPUT) ;
	XGpioPs_SetOutputEnablePin(&GPIO_PTR, 13, GPIO_OUTPUT) ;
	XGpioPs_WritePin(&GPIO_PTR, 13, 0x1) ;

	//set MIO 50 as input
	XGpioPs_SetDirectionPin(&GPIO_PTR, 50, GPIO_INPUT) ;
	XGpioPs_ReadPin(&GPIO_PTR,50) ;
	//set interrupt type
	XGpioPs_SetIntrTypePin(&GPIO_PTR, 50, XGPIOPS_IRQ_TYPE_EDGE_RISING) ;
	//enable GPIO interrupt
	XGpioPs_IntrEnablePin(&GPIO_PTR, 50) ;

	XGpioPs_SetDirectionPin(&GPIO_PTR, 51, GPIO_INPUT) ;
	XGpioPs_SetIntrTypePin(&GPIO_PTR, 51, XGPIOPS_IRQ_TYPE_EDGE_RISING) ;
	XGpioPs_IntrEnablePin(&GPIO_PTR, 51) ;

	// self defined intrupt function
	my_IntrInitFuntion(&INTCInst, MIO_0_DEVICE_ID, &GPIO_PTR) ;
	xil_printf("Boot up");
	while(1){
		if (key_flag){
			key_flag = 0;
			led_status = ~led_status;
			XGpioPs_WritePin(&GPIO_PTR, 0, led_status) ;
			XGpioPs_WritePin(&GPIO_PTR, 13, led_status) ;
			xil_printf("key is pressed\n\r");
		}
	}
}

void my_IntrInitFuntion(XScuGic *InstancePtr , u16 DeviceId, XGpioPs *GpioInstancePtr){
	XScuGic_Config *IntcConfig;
	//check device id
	IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
	//intialization
	XScuGic_CfgInitialize(InstancePtr, IntcConfig, IntcConfig->CpuBaseAddress) ;
	//set priority and trigger type
	XScuGic_SetPriorityTriggerType(InstancePtr, KEY_INTR_ID, 0xA0, 0x3);// important
	XScuGic_Connect(InstancePtr, KEY_INTR_ID, (Xil_ExceptionHandler)my_GpioHandler, (void *)GpioInstancePtr) ;// important
	//Enable GIC
	XScuGic_Enable(InstancePtr, KEY_INTR_ID) ;
	Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT, (Xil_ExceptionHandler)XScuGic_InterruptHandler, InstancePtr);
	Xil_ExceptionEnable();

}

void my_GpioHandler(void *CallbackRef){
	XGpioPs *GpioInstancePtr = (XGpioPs *)CallbackRef ;
	xil_printf("triggered\n\r");
//	sleep(0.02);
	if (XGpioPs_IntrGetStatusPin(GpioInstancePtr, 50)){
		XGpioPs_IntrClearPin(GpioInstancePtr, 50) ;
		key_flag = 1;
		xil_printf("\t50\n\r");
	}
	else if (XGpioPs_IntrGetStatusPin(GpioInstancePtr, 51)){
		XGpioPs_IntrClearPin(GpioInstancePtr, 51) ;
		key_flag = 1;
		xil_printf("\t51\n\r");
	}

}

```

#### 1.6.2.3. AXI GPIO input/output

NOTE:

1. `Device ID ` is refer to how many HW blocks of XGPIO in the FPGA. The first value is 0
2. `Channel ID` is refer to how many channels are used in one XGPIO block. usually only one channel, the first value is 0

```c
#include "xgpio.h"
#include "sleep.h"

#define GPIO_OUTPUT_DEVICE_ID	XPAR_GPIO_0_DEVICE_ID
#define GPIO_INPUT_DEVICE_ID	XPAR_GPIO_1_DEVICE_ID
#define CHANNEL1 1
#define printf xil_printf	/* A smaller footprint printf */

XGpio GpioOutput; /* The driver instance for GPIO Device configured as O/P */
XGpio GpioInput;  /* The driver instance for GPIO Device configured as I/P */

int main(void)
{
	u32 LED_s = 0x6U;
	u32 ButtonData;
	/*output LED*/
	XGpio_Initialize(&GpioOutput, GPIO_OUTPUT_DEVICE_ID);
	XGpio_SetDataDirection(&GpioOutput, CHANNEL1, 0x0);
	XGpio_DiscreteWrite(&GpioOutput, CHANNEL1, 0x0);

	/*input button*/
	XGpio_Initialize(&GpioInput, GPIO_INPUT_DEVICE_ID);
	XGpio_SetDataDirection(&GpioInput, CHANNEL1, 0xFFFFFFFF);
	ButtonData = XGpio_DiscreteRead(&GpioInput, CHANNEL1);
	printf("First Button Data is 0x%x \n\r", ButtonData);

	while (1){
		printf("read from button:0x%x\n\r", XGpio_DiscreteRead(&GpioInput, CHANNEL1));
		XGpio_DiscreteWrite(&GpioOutput, CHANNEL1, LED_s);
		LED_s = ~LED_s;
		sleep(1);
	}
}
```

#### 1.6.2.4. AXI GPIO  interrupt mode

```c

#include "xgpio.h"
#include "xil_exception.h"
#include "xscugic.h"
#include "sleep.h"
#include "xil_printf.h"

#define GPIO_OUT_DEVICE_ID			XPAR_GPIO_0_DEVICE_ID
#define GPIO_IN_DEVICE_ID			XPAR_GPIO_1_DEVICE_ID
#define CHANNEL1					1

#define INTC						XScuGic
#define INTC_DEVICE_ID				XPAR_SCUGIC_SINGLE_DEVICE_ID
#define INTC_GPIO_INTERRUPT_ID		XPAR_FABRIC_AXI_GPIO_1_IP2INTC_IRPT_INTR
#define printf xil_printf

/************************** Function Prototypes ******************************/
void GpioHandler(void *CallBackRef);
int my_GpioSetupIntrSystem(INTC *IntcInstancePtr, XGpio *InstancePtr,
			u16 DeviceId, u16 IntrId, u16 IntrMask);

void my_GpioDisableIntr(INTC *IntcInstancePtr, XGpio *InstancePtr,
			u16 IntrId, u16 IntrMask);

XGpio GpioInput; /* The Instance of the GPIO Driver */
XGpio GpioOutput; /* The Instance of the GPIO Driver */
INTC Intc; /* The Instance of the Interrupt Controller Driver */

static u16 GlobalIntrMask; /* GPIO channel mask that is needed by the Interrupt Handler */
static volatile u32 IntrFlag; /* Interrupt Handler Flag */

int main(void)
{
	u32 LED_s = 0x6;
	/* input with intc */
	XGpio_Initialize(&GpioInput, GPIO_IN_DEVICE_ID);
	XGpio_SetDataDirection(&GpioInput, CHANNEL1, 0x1);
	my_GpioSetupIntrSystem(&Intc, &GpioInput, GPIO_IN_DEVICE_ID, INTC_GPIO_INTERRUPT_ID, CHANNEL1);
//	my_GpioDisableIntr(&Intc, &GpioInput, INTC_GPIO_INTERRUPT_ID, CHANNEL1);

	/* output  */
	XGpio_Initialize(&GpioOutput, GPIO_OUT_DEVICE_ID);
	/* Set the direction for all signals to be outputs */
	XGpio_SetDataDirection(&GpioOutput, CHANNEL1, 0x0);
	/* Set the GPIO outputs to low */
	XGpio_DiscreteWrite(&GpioOutput, CHANNEL1, LED_s);

	while (1){
		if (IntrFlag){
			IntrFlag = 0;
			printf("Button input: 0x%x\n\r", XGpio_DiscreteRead(&GpioInput, CHANNEL1));
			XGpio_DiscreteWrite(&GpioOutput, CHANNEL1, ~XGpio_DiscreteRead(&GpioOutput, CHANNEL1));
		}
	}
}

int my_GpioSetupIntrSystem(INTC *IntcInstancePtr, XGpio *InstancePtr,
			u16 DeviceId, u16 IntrId, u16 IntrMask)
{
	GlobalIntrMask = IntrMask;
	XScuGic_Config *IntcConfig;

	IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
	XScuGic_CfgInitialize(IntcInstancePtr, IntcConfig, IntcConfig->CpuBaseAddress);
	XScuGic_SetPriorityTriggerType(IntcInstancePtr, IntrId, 0xA0, 0x3);

	XScuGic_Connect(IntcInstancePtr, IntrId,
				 (Xil_ExceptionHandler)GpioHandler, InstancePtr);
	XScuGic_Enable(IntcInstancePtr, IntrId);
	XGpio_InterruptEnable(InstancePtr, IntrMask);
	XGpio_InterruptGlobalEnable(InstancePtr);
	Xil_ExceptionInit();
	Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
			 (Xil_ExceptionHandler)XScuGic_InterruptHandler, IntcInstancePtr);
	Xil_ExceptionEnable();
	return 0;
}

void GpioHandler(void *CallbackRef)
{
	XGpio *GpioPtr = (XGpio *)CallbackRef;
	IntrFlag = 1;
	printf("button pressed\n\r");
	/* Clear the Interrupt. which one to clear */
	XGpio_InterruptClear(GpioPtr, GlobalIntrMask);
//	XGpio_InterruptClear(GpioPtr, INTC_GPIO_INTERRUPT_ID);

}


void my_GpioDisableIntr(INTC *IntcInstancePtr, XGpio *InstancePtr,
			u16 IntrId, u16 IntrMask)
{
	XGpio_InterruptDisable(InstancePtr, IntrMask);
	XScuGic_Disable(IntcInstancePtr, IntrId);
	XScuGic_Disconnect(IntcInstancePtr, IntrId);
	return;
}
```

## 1.7. 06_ps_UART

### 1.7.1. vivado

### 1.7.2. SDK

```c
/* ------------------------------------------------------------ */
/*				Include File Definitions						*/
/* ------------------------------------------------------------ */

#include "xparameters.h"
#include <stdio.h>
#include "xil_printf.h"
#include "sleep.h"
#include "xscugic.h"
#include "uart_parameter.h"


#define UART_DEVICE_ID      XPAR_XUARTPS_0_DEVICE_ID
#define INTC_DEVICE_ID		XPAR_SCUGIC_SINGLE_DEVICE_ID
#define UART_INT_IRQ_ID		XPAR_XUARTPS_1_INTR

/* Statement */
#define UART_TX      0
#define UART_RXCHECK 1
#define UART_WAIT    2

/* maximum receiver length */
#define MAX_LEN    2000

/************************** Variable Definitions *****************************/

XUartPs Uart_PS;		/* Instance of the UART Device */
XScuGic IntcInstPtr ;

/* UART receiver buffer */
u8 ReceivedBuffer[MAX_LEN] ;
/* UART receiver buffer pointer*/
u8 *ReceivedBufferPtr ;
/* UART receiver byte number */
volatile u32 ReceivedByteNum ;

volatile u32 ReceivedFlag  ;

/*
 * Function declaration
 */
int UartPsSend(XUartPs *InstancePtr, u8 *BufferPtr, u32 NumBytes) ;
int UartPsRev (XUartPs *InstancePtr, u8 *BufferPtr, u32 NumBytes) ;

int SetupInterruptSystem(XScuGic *IntcInstancePtr,	XUartPs *UartInstancePtr, u16 UartIntrId);
void Handler(void *CallBackRef);

int main(void)
{
	int Status;
	XUartPs_Config *Config;

	u32 SendByteNum ;
	u8 *SendBufferPtr ;
	u8 state = UART_TX ;

	ReceivedBufferPtr = ReceivedBuffer ;

	ReceivedFlag = 0 ;
	ReceivedByteNum = 0 ;

	Config = XUartPs_LookupConfig(UART_DEVICE_ID);
	if (NULL == Config) {
		return XST_FAILURE;
	}
	Status = XUartPs_CfgInitialize(&Uart_PS, Config, Config->BaseAddress);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}
	/* Use Normal mode. */
	XUartPs_SetOperMode(&Uart_PS, XUARTPS_OPER_MODE_NORMAL);
	/* Set uart mode Baud Rate 115200, 8bits, no parity, 1 stop bit */
	XUartPs_SetDataFormat(&Uart_PS, &UartFormat) ;
	/*Set receiver FIFO interrupt trigger level, here set to 1*/
	XUartPs_SetFifoThreshold(&Uart_PS,1) ;
	/* Enable the receive FIFO trigger level interrupt and empty interrupt for the device */
	XUartPs_SetInterruptMask(&Uart_PS,XUARTPS_IXR_RXOVR|XUARTPS_IXR_RXEMPTY);
	SetupInterruptSystem(&IntcInstPtr, &Uart_PS, UART_INT_IRQ_ID) ;

	while(1)
	{
		switch(state)
		{
		case UART_TX :          /* Send string : Hello Alinx! */
		{
			SendBufferPtr = TxString ;
			SendByteNum = sizeof(TxString) ;
			UartPsSend(&Uart_PS, SendBufferPtr, SendByteNum);
			state = UART_RXCHECK ;
			break ;
		}
		case UART_RXCHECK :    /* Check receiver flag, send received data */
		{
			if (ReceivedFlag)
			{
				/* Reset receiver pointer, flag, byte number */
				ReceivedBufferPtr = ReceivedBuffer ;
				SendBufferPtr = ReceivedBuffer ;
				SendByteNum = ReceivedByteNum ;
				ReceivedFlag = 0 ;
				ReceivedByteNum = 0 ;
				UartPsSend(&Uart_PS, SendBufferPtr, SendByteNum);
			}
			else
			{
				state = UART_WAIT ;
			}
			break ;
		}
		case UART_WAIT :		/* Wait for 1s */
		{
			sleep(1) ;
			state = UART_TX ;
			break ;
		}
		default : break ;
		}
	}
}

int SetupInterruptSystem(XScuGic *IntcInstancePtr,	XUartPs *UartInstancePtr, u16 UartIntrId)
{
	int Status;
	/* Configuration for interrupt controller */
	XScuGic_Config *IntcConfig;

	/* Initialize the interrupt controller driver */
	IntcConfig = XScuGic_LookupConfig(INTC_DEVICE_ID);
	if (NULL == IntcConfig) {
		return XST_FAILURE;
	}

	Status = XScuGic_CfgInitialize(IntcInstancePtr, IntcConfig,
			IntcConfig->CpuBaseAddress);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}

	/*
	 * Connect the interrupt controller interrupt handler to the
	 * hardware interrupt handling logic in the processor.
	 */
	Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
			(Xil_ExceptionHandler) XScuGic_InterruptHandler,
			IntcInstancePtr);


	Status = XScuGic_Connect(IntcInstancePtr, UartIntrId,
			(Xil_ExceptionHandler) Handler,
			(void *) UartInstancePtr);
	if (Status != XST_SUCCESS) {
		return XST_FAILURE;
	}

	XScuGic_Enable(IntcInstancePtr, UartIntrId);
	Xil_ExceptionEnable();

	return Status ;
}


void Handler(void *CallBackRef)
{
	XUartPs *UartInstancePtr = (XUartPs *) CallBackRef ;
	u32 ReceivedCount = 0 ;
	u32 UartSrValue ;

	UartSrValue = XUartPs_ReadReg(UartInstancePtr->Config.BaseAddress, XUARTPS_SR_OFFSET) & (XUARTPS_IXR_RXOVR|XUARTPS_IXR_RXEMPTY);
	ReceivedFlag = 0 ;

	if (UartSrValue & XUARTPS_IXR_RXOVR)   /* check if receiver FIFO trigger */
	{
		ReceivedCount = UartPsRev(&Uart_PS, ReceivedBufferPtr, MAX_LEN) ;
		ReceivedByteNum += ReceivedCount ;
		ReceivedBufferPtr += ReceivedCount ;
		/* clear trigger interrupt */
		XUartPs_WriteReg(UartInstancePtr->Config.BaseAddress, XUARTPS_ISR_OFFSET, XUARTPS_IXR_RXOVR) ;
	}
	else if (UartSrValue & XUARTPS_IXR_RXEMPTY)       /*check if receiver FIFO empty */
	{
		/* clear empty interrupt */
		XUartPs_WriteReg(UartInstancePtr->Config.BaseAddress, XUARTPS_ISR_OFFSET, XUARTPS_IXR_RXEMPTY) ;
		ReceivedFlag = 1 ;
	}

}


int UartPsSend(XUartPs *InstancePtr, u8 *BufferPtr, u32 NumBytes)
{

	u32 SentCount = 0U;

	/* Setup the buffer parameters */
	InstancePtr->SendBuffer.RequestedBytes = NumBytes;
	InstancePtr->SendBuffer.RemainingBytes = NumBytes;
	InstancePtr->SendBuffer.NextBytePtr = BufferPtr;


	while (InstancePtr->SendBuffer.RemainingBytes > SentCount)
	{
		/* Fill the FIFO from the buffer */
		if (!XUartPs_IsTransmitFull(InstancePtr->Config.BaseAddress))
		{
			XUartPs_WriteReg(InstancePtr->Config.BaseAddress,
					XUARTPS_FIFO_OFFSET,
					((u32)InstancePtr->SendBuffer.
							NextBytePtr[SentCount]));

			/* Increment the send count. */
			SentCount++;
		}
	}

	/* Update the buffer to reflect the bytes that were sent from it */
	InstancePtr->SendBuffer.NextBytePtr += SentCount;
	InstancePtr->SendBuffer.RemainingBytes -= SentCount;


	return SentCount;
}

int UartPsRev(XUartPs *InstancePtr, u8 *BufferPtr, u32 NumBytes)
{
	u32 ReceivedCount = 0;
	u32 CsrRegister;

	/* Setup the buffer parameters */
	InstancePtr->ReceiveBuffer.RequestedBytes = NumBytes;
	InstancePtr->ReceiveBuffer.RemainingBytes = NumBytes;
	InstancePtr->ReceiveBuffer.NextBytePtr = BufferPtr;

	/*
	 * Read the Channel Status Register to determine if there is any data in
	 * the RX FIFO
	 */
	CsrRegister = XUartPs_ReadReg(InstancePtr->Config.BaseAddress,
			XUARTPS_SR_OFFSET);

	/*
	 * Loop until there is no more data in RX FIFO or the specified
	 * number of bytes has been received
	 */
	while((ReceivedCount < InstancePtr->ReceiveBuffer.RemainingBytes)&&
			(((CsrRegister & XUARTPS_SR_RXEMPTY) == (u32)0)))
	{
		InstancePtr->ReceiveBuffer.NextBytePtr[ReceivedCount] =
				XUartPs_ReadReg(InstancePtr->Config.BaseAddress,XUARTPS_FIFO_OFFSET);

		ReceivedCount++;

		CsrRegister = XUartPs_ReadReg(InstancePtr->Config.BaseAddress,
				XUARTPS_SR_OFFSET);
	}
	InstancePtr->is_rxbs_error = 0;
	/*
	 * Update the receive buffer to reflect the number of bytes just
	 * received
	 */
	if(InstancePtr->ReceiveBuffer.NextBytePtr != NULL){
		InstancePtr->ReceiveBuffer.NextBytePtr += ReceivedCount;
	}
	InstancePtr->ReceiveBuffer.RemainingBytes -= ReceivedCount;

	return ReceivedCount;
}

```

```c
 * uart_parameter.h

#ifndef SRC_UART_PARAMETER_H_
#define SRC_UART_PARAMETER_H_

#include "xuartps.h"

u8 TxString[14] =
{
		"Hello ALINX!\r\n"
};

XUartPsFormat UartFormat =
{
		115200,
		XUARTPS_FORMAT_8_BITS,
		XUARTPS_FORMAT_NO_PARITY,
		XUARTPS_FORMAT_1_STOP_BIT
};

#endif /* SRC_UART_PARAMETER_H_ */
```

## 1.8. 07_ps_XADC

### 1.8.1. vivado

### 1.8.2. SDK

```c

#include "xparameters.h"
#include "xadcps.h"
#include "xstatus.h"
#include "stdio.h"
#include "xil_printf.h"

#define XADC_DEVICE_ID 		XPAR_XADCPS_0_DEVICE_ID
#define printf xil_printf /* Small foot-print printf function */

/************************** Function Prototypes *****************************/

static int XAdcPolledPrintfExample(u16 XAdcDeviceId);
static int XAdcFractionToInt(float FloatNum);

/************************** Variable Definitions ****************************/

static XAdcPs XAdcInst;      /* XADC driver instance */

int main(void)
{
	XAdcPolledPrintfExample(XADC_DEVICE_ID);
}


int XAdcPolledPrintfExample(u16 XAdcDeviceId)
{
	int Status;
	XAdcPs_Config *ConfigPtr;
	u32 TempRawData;
	u32 VccPintRawData;
	u32 VccPauxRawData;
	u32 VccPdroRawData;
	float TempData;
	float VccPintData;
	float VccPauxData;
	float MaxData;
	float MinData;
	XAdcPs *XAdcInstPtr = &XAdcInst;

	ConfigPtr = XAdcPs_LookupConfig(XAdcDeviceId);
	XAdcPs_CfgInitialize(XAdcInstPtr, ConfigPtr, ConfigPtr->BaseAddress);
	Status = XAdcPs_SelfTest(XAdcInstPtr);
	/*
	 * Disable the Channel Sequencer before configuring the Sequence
	 * registers.
	 */
	XAdcPs_SetSequencerMode(XAdcInstPtr, XADCPS_SEQ_MODE_SAFE);
	
	/*
	 * Read the on-chip Temperature Data (Current/Maximum/Minimum)
	 * from the ADC data registers.
	 */
	TempRawData = XAdcPs_GetAdcData(XAdcInstPtr, XADCPS_CH_TEMP);
	TempData = XAdcPs_RawToTemperature(TempRawData);
	printf("\r\nThe Current Temperature is %0d.%03d Centigrades.\r\n",
				(int)(TempData), XAdcFractionToInt(TempData));

	TempRawData = XAdcPs_GetMinMaxMeasurement(XAdcInstPtr, XADCPS_MAX_TEMP);
	MaxData = XAdcPs_RawToTemperature(TempRawData);
	printf("The Maximum Temperature is %0d.%03d Centigrades. \r\n",
				(int)(MaxData), XAdcFractionToInt(MaxData));

	TempRawData = XAdcPs_GetMinMaxMeasurement(XAdcInstPtr, XADCPS_MIN_TEMP);
	MinData = XAdcPs_RawToTemperature(TempRawData & 0xFFF0);
	printf("The Minimum Temperature is %0d.%03d Centigrades. \r\n",
				(int)(MinData), XAdcFractionToInt(MinData));

	/*
	 * Read the VccPint Votage Data (Current/Maximum/Minimum) from the
	 * ADC data registers.
	 */
	VccPintRawData = XAdcPs_GetAdcData(XAdcInstPtr, XADCPS_CH_VCCPINT);
	VccPintData = XAdcPs_RawToVoltage(VccPintRawData);
	printf("\r\nThe Current VCCPINT is %0d.%03d Volts. \r\n",
			(int)(VccPintData), XAdcFractionToInt(VccPintData));

	VccPintRawData = XAdcPs_GetMinMaxMeasurement(XAdcInstPtr, XADCPS_MAX_VCCPINT);
	MaxData = XAdcPs_RawToVoltage(VccPintRawData);
	printf("The Maximum VCCPINT is %0d.%03d Volts. \r\n",
			(int)(MaxData), XAdcFractionToInt(MaxData));

	VccPintRawData = XAdcPs_GetMinMaxMeasurement(XAdcInstPtr, XADCPS_MIN_VCCPINT);
	MinData = XAdcPs_RawToVoltage(VccPintRawData);
	printf("The Minimum VCCPINT is %0d.%03d Volts. \r\n",
			(int)(MinData), XAdcFractionToInt(MinData));
	return XST_SUCCESS;
}

int XAdcFractionToInt(float FloatNum)
{
	float Temp;

	Temp = FloatNum;
	if (FloatNum < 0) {
		Temp = -(FloatNum);
	}

	return( ((int)((Temp -(float)((int)Temp)) * (1000.0f))));
}
```

## 1.9. 08_DMA

- DMA可以产生中断
- DMA模块一端接交叉互联模块(AXI BUS)，另一端接设备(AXI Stream BUS)。
  - MM2S: memory map to slaver.
  - S2MM: slaver to memory map. 
- AXI DMA这个模块只是起着通过AXI-4 BUS，访问HP接口里的DDR

### 1.9.1. Vivado

- Data-stream-FIFO
- AXI-DMA



![Screenshot-2020-01-03PM1.45.56](https://gitee.com/AndrewChu/markdown/raw/master/1599546831_Screenshot-2020-01-03PM1.45.56.png)

![Screenshot-2020-01-03PM1.46.45](https://gitee.com/AndrewChu/markdown/raw/master/1599546832_Screenshot-2020-01-03PM1.46.45.png)



### 1.9.2. SDK

```c
/* ------------------------------------------------------------ */
/*				Include File Definitions						*/
/* ------------------------------------------------------------ */


#include "xaxidma.h"
#include "xparameters.h"
#include "xil_printf.h"
#include "xscugic.h"


#define DMA_DEV_ID		  XPAR_AXIDMA_0_DEVICE_ID
#define INT_DEVICE_ID     XPAR_SCUGIC_SINGLE_DEVICE_ID
#define INTR_ID           XPAR_FABRIC_AXI_DMA_0_S2MM_INTROUT_INTR

#define FIFO_DATABYTE   4
#define TEST_COUNT      80
#define MAX_PKT_LEN		TEST_COUNT*FIFO_DATABYTE

#define TEST_START_VALUE	0xC

#define NUMBER_OF_TRANSFERS	2

/*
 * Function declaration
 */
int XAxiDma_Setup(u16 DeviceId);
static int CheckData(void);
int SetInterruptInit(XScuGic *InstancePtr, u16 IntrID, XAxiDma *XAxiDmaPtr) ;

XScuGic INST ;

XAxiDma AxiDma;

u8 TxBufferPtr[MAX_PKT_LEN] ;
u8 RxBufferPtr[MAX_PKT_LEN] ;


int main()
{
	int Status;

	xil_printf("\r\n--- Entering main() --- \r\n");

	Status = XAxiDma_Setup(DMA_DEV_ID);

	if (Status != XST_SUCCESS) {
		xil_printf("XAxiDma Test Failed\r\n");
		return XST_FAILURE;
	}

	xil_printf("Successfully Ran XAxiDma Test\r\n");

	xil_printf("--- Exiting main() --- \r\n");

	return XST_SUCCESS;

}



int SetInterruptInit(XScuGic *InstancePtr, u16 IntrID, XAxiDma *XAxiDmaPtr)
{

	XScuGic_Config * Config ;
	int Status ;

	Config = XScuGic_LookupConfig(INT_DEVICE_ID) ;

	Status = XScuGic_CfgInitialize(&INST, Config, Config->CpuBaseAddress) ;
	if (Status != XST_SUCCESS)
		return XST_FAILURE ;

	Status = XScuGic_Connect(InstancePtr, IntrID,
			(Xil_ExceptionHandler)CheckData,
			XAxiDmaPtr) ;

	if (Status != XST_SUCCESS) {
			return Status;
		}

	XScuGic_Enable(InstancePtr, IntrID) ;

	Xil_ExceptionInit();
	Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
					(Xil_ExceptionHandler) XScuGic_InterruptHandler,
					InstancePtr);

	Xil_ExceptionEnable();


	return XST_SUCCESS ;

}


int XAxiDma_Setup(u16 DeviceId)
{
	XAxiDma_Config *CfgPtr;
	int Status;
	int Tries = NUMBER_OF_TRANSFERS;
	int Index;
	u8 Value;

	/* Initialize the XAxiDma device.
	 */
	CfgPtr = XAxiDma_LookupConfig(DeviceId);
	if (!CfgPtr) {
		xil_printf("No config found for %d\r\n", DeviceId);
		return XST_FAILURE;
	}

	Status = XAxiDma_CfgInitialize(&AxiDma, CfgPtr);
	if (Status != XST_SUCCESS) {
		xil_printf("Initialization failed %d\r\n", Status);
		return XST_FAILURE;
	}

	if(XAxiDma_HasSg(&AxiDma)){
		xil_printf("Device configured as SG mode \r\n");
		return XST_FAILURE;
	}

	Status = SetInterruptInit(&INST,INTR_ID, &AxiDma) ;
	if (Status != XST_SUCCESS)
		         return XST_FAILURE ;

	/* Disable MM2S interrupt, Enable S2MM interrupt */
	XAxiDma_IntrEnable(&AxiDma, XAXIDMA_IRQ_IOC_MASK,
						XAXIDMA_DEVICE_TO_DMA);
	XAxiDma_IntrDisable(&AxiDma, XAXIDMA_IRQ_ALL_MASK,
						XAXIDMA_DMA_TO_DEVICE);

	Value = TEST_START_VALUE;

	for(Index = 0; Index < MAX_PKT_LEN; Index ++) {
			TxBufferPtr[Index] = Value;

			Value = (Value + 1) & 0xFF;
	}
	/* Flush the SrcBuffer before the DMA transfer, in case the Data Cache
	 * is enabled
	 */
	Xil_DCacheFlushRange((UINTPTR)TxBufferPtr, MAX_PKT_LEN);
	Xil_DCacheFlushRange((UINTPTR)RxBufferPtr, MAX_PKT_LEN);

	for(Index = 0; Index < Tries; Index ++) {

			Status = XAxiDma_SimpleTransfer(&AxiDma,(UINTPTR) TxBufferPtr,
								MAX_PKT_LEN, XAXIDMA_DMA_TO_DEVICE);

			if (Status != XST_SUCCESS) {
				return XST_FAILURE;
			}

		    Status = XAxiDma_SimpleTransfer(&AxiDma,(UINTPTR) RxBufferPtr,
								MAX_PKT_LEN, XAXIDMA_DEVICE_TO_DMA);


			if (Status != XST_SUCCESS) {
				return XST_FAILURE;
			}


			while ((XAxiDma_Busy(&AxiDma,XAXIDMA_DEVICE_TO_DMA)) ||
				(XAxiDma_Busy(&AxiDma,XAXIDMA_DMA_TO_DEVICE)))
					{
					/* Wait */
			}


		}

		/* Test finishes successfully
		 */
		return XST_SUCCESS;
	}


static int CheckData(void)
{
	u8 *RxPacket;
	int Index = 0;
	u8 Value;

	RxPacket = RxBufferPtr;
	Value = TEST_START_VALUE;

	xil_printf("Enter Interrupt\r\n");
	/*Clear Interrupt*/
	XAxiDma_IntrAckIrq(&AxiDma, XAXIDMA_IRQ_IOC_MASK,
			XAXIDMA_DEVICE_TO_DMA) ;
	/* Invalidate the DestBuffer before receiving the data, in case the
		 * Data Cache is enabled
		 */
	Xil_DCacheInvalidateRange((UINTPTR)RxPacket, MAX_PKT_LEN);


	for(Index = 0; Index < MAX_PKT_LEN; Index++) {
		if (RxPacket[Index] != Value) {
			xil_printf("Data error %d: %x/%x\r\n",
			Index, (unsigned int)RxPacket[Index],
				(unsigned int)Value);

			return XST_FAILURE;
		}
		Value = (Value + 1) & 0xFF;
	}

	return XST_SUCCESS;
}

```

## 1.10. 98_IP core

主要研究了这么封装IP核，同时和DMA互动. 从底层记录起：

if：

1. ad_data_valid 是在8个通道转换好之后，给出一个脉冲信号
2. 8个通道转好好之后，马上开始继续转换。转换好之后再给出valid信号。
3. 转换速率收到os的数字滤波器的影响。如果默认是200k

sample：

1. sample_len使用AXI的第二个寄存器配置下来，决定的是单个通道的采样点数，采样的次数。
2. 存入dma的数据是sample_len multi 8 multi 2 bytes大小
3. sample module --- FIFO ----DMA。FIFO是用来跨时钟域的同步的。 
4. FIFO的写入：ADC处于采样模式，同时ADC的valid给出有效脉冲。FIFO的读出：只要AXIS从机准备好（DMA），同时FIFO不是empty的，FIFO就开始吐数据M_AXIS_tdata。FIFO读的比写的快，所以不用太深
5. FIFO吐给DMA的数据就是M_AXIS_tdata。其他的AXIS的同步信号，都是Verilog写的逻辑。
6. sample_start是AXI的第一个寄存器配置下来，当PS配置这个寄存器为高的时候，PL开始转换。当转换开始后，PL会马上把该寄存器配置为低，使得PL的转换只会持续一次。但是一次就可以转换sample_len multi 8 multi 2 bytes 到DMA
7. 完成sample_len 次采样之后，AXIS就会发送一个完成信号给DMA，DMA收到之后会触发s2mm中断给PS

DMA:

1. 深度是2^23
2. 地址宽度是32bit
3. stream data width是16 bit.因为fifo是16
4. Memory map width 是64bit？？？

clock：

1. ADC---50M    GP----100M    AXIS----142M

interconnection

1. DMA: 配置走的GP, AXIS走的HP。只需要连线就行
2. ADC：配置走的GP（靠生成IP核的时候自动产生的代码）, 和DMA用AXIS（自己写的逻辑）. 

## 1.11. AD7606LWIP

### 1.11.1. UDP Protocol

![Screenshot-2020-01-07AM10.14.05](https://gitee.com/AndrewChu/markdown/raw/master/1599546823_Screenshot-2020-01-07AM10.14.05.png)

![Screenshot-2020-01-07AM10.14.21](https://gitee.com/AndrewChu/markdown/raw/master/1599546824_Screenshot-2020-01-07AM10.14.21.png)

查询命令:

```python
data = '\x00\x00\x01\x00\x01'
```

Mac addr:  00 0a 35 00 01 02

IP: c0 a8 01 0b

有效数据长度：10---16位

采样率： 00 03 0d 40-----200k sample rate

缓存长度： 00 01 00 00-----16位 65536----单位是字节

```python
data = b'\x00\x00\x01\x00\x01'
data = b'\x00\x00\x01\x00\x02\x00\x0A\x35\x00\x01\x02\x00\x00\x00\x01\x00\x00\x80\x00'
```

### 1.11.2. 数据恢复：

$$Voltage=2bytes/(65536/2)*5$$

### 1.11.3. 数据的参数

| 序列 | 参数名             | 大小               | 二进制 | 是否可配 | 说明                                                         |
| ---- | ------------------ | ------------------ | ------ | -------- | ------------------------------------------------------------ |
| 1    | ADC_SAMPLE_NUM     | `1024*32` 个       |        | PS写死   | 配置ADC采样的次数，意味着8个通道都要采集ADC_SAMPLE_NUM次     |
| 2    | ADC占用空间        | `1024*32*8*2` byte |        |          | 采集完                                                       |
| 3    | DmaRxBuffer        | 非常大             |        |          | 关联到了DMA_BD里，就是DDR3里所有的数据。就是DMA的大小，除以2，存的数据的个数 |
| 4    | 上位机发的采样次数 |                    | 15     |          | 就和ADC_SAMPLE_NUM一样                                       |
| 5    | FrameLengthCurr    |                    | 16     |          | 就是要会给上位机的数据大小，`ADC_SAMPLE_NUM*2`               |

### 1.11.4. python

https://www.cnblogs.com/gala/archive/2011/09/22/2184801.html

https://blog.csdn.net/liuguanghui1988/article/details/53375269



## 1.12. FAQ

### 1.12.1. Debug into disassemble

> Try the following:
>
> \- Right-click on BSP from Project Explorer -> Board Support Package Settings
>
> \- Select the cortex under drivers section (ps7_cortexa9_0)
>
> \- Modify the extra_compiler_flags: on Value column add at the end " -g" -> Ok

### 1.12.2. AXI4 protocol

![Screenshot-2020-01-03PM3.43.51](https://gitee.com/AndrewChu/markdown/raw/master/1599546832_Screenshot-2020-01-03PM3.43.51.png)

![Screenshot-2020-01-03PM3.44.20](https://gitee.com/AndrewChu/markdown/raw/master/1599546833_Screenshot-2020-01-03PM3.44.20.png)

![Screenshot-2020-01-03PM3.44.31](https://gitee.com/AndrewChu/markdown/raw/master/1599546834_Screenshot-2020-01-03PM3.44.31.png)

![Screenshot-2020-01-03PM3.44.45](https://gitee.com/AndrewChu/markdown/raw/master/1599546835_Screenshot-2020-01-03PM3.44.45.png)

> ACLK为时钟线，所有信号都在ACLK上升沿被采样；
>
> ARESETn为复位线，低电平有效；
>
> TVALID为主机数据同步线，为高表示主机准备好发送数据；
>
> TREADY为从机数据同步线，为高表示从机准备好接收数据；这两根线完成了主机与从机的握手信号，一旦二者都变高有效，数据传输开始。
>
> TDATA为数据线，主机发送，从机接收。
>
> TKEEP为主机数据有效指示，为高代表对应的字节为有效字节，否则表示发送的为空字节。
>
> TLAST为主机最后一个字指示，下一clk数据将无效，TVALID将变低。
>
> https://blog.csdn.net/Real003/article/details/88976454

