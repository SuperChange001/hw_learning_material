# 1. 前言

[所有笔记的链接](https://github.com/SuperChange001/hw_learning_material)    
所有的文字都是作者一个一个码出来的，花了很多的时间和精力。创作不易，大家要是有Gitee的账号，那就给我点个Star把。    

一个优秀的工程师，不是**业务驱动型**，而是**技术驱动型**。这个也是为什么真正优秀的公司都是**面试造火箭，实际拧螺丝**的原因。很多人只会描述自己的业务，自己的项目，但是对于电路深层次的原理则是一无所知。**理论和实践是两条腿走路的**，甚至于理论是远高于实践的。不要只做一个**if else coder**！     

# 2. Content
**偏差和噪声**的区别？什么是**容差**？**RS485和CAN收发器**的区别，以及产生的效果？    

因为篇幅限制，外加我更想记录自己对一些理论知识的见解，所以有些内容不适合0基础学习。希望大家**少接触快餐知识**，**少被贩卖焦虑**，多沉下心来自己去消化吸收理论知识，最后再和别人的经验进行参照对比。   
内容已经分门别类，请直接点击链接：     
1. 基本元件：
	- 说明：基本元件简单，但是都是基于直流低频的模式下。随着现在电路的工作频率越来越高，元件的寄生参数的作用会越来越明显。
	- [Electronic Basics](https://github.com/SuperChange001/hw_learning_material/blob/master/R-C-L-D_notes.md)
	- [BJT-MOSFET_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/BJT-MOSFET_notes.md)
2. 电源：
	- 说明：一个好的电源是模数电路的基础。但是现在的DCDC IC已经内置了非常多的功能，导致电子工程师对于DCDC的底层原理理解不够，从而把握不住DCDC的设计关键参数，尤其是出现功能性问题和EMC整改的时候是一头雾水。
	- [DC-DC-Basics](https://github.com/SuperChange001/hw_learning_material/blob/master/DC-DC-Basics.md)
	- [Isolation and EMC tricks](https://github.com/SuperChange001/hw_learning_material/blob/master/Isolation_Power.md)
	- [ACDC DCDC-Common-mistakes](https://github.com/SuperChange001/hw_learning_material/blob/master/DC-DC-Common-mistake.md)
	- [DCDC环路补偿](https://github.com/SuperChange001/hw_learning_material/blob/master/Loop_compensation.md)
	- [Motor_Driver](https://github.com/SuperChange001/hw_learning_material/blob/master/Power_Electronics/Motor_Driver.md)
2. 模拟：
	- 说明：纯模拟越来越少，模数混合是趋势。搞不懂OPA和ADC，是做不好模拟信号采集的。基本上所有的参数，都有DC模式和AC模式。
	- [Analog-Engineer's-Pocket-Reference-TI](https://github.com/SuperChange001/hw_learning_material/blob/master/Analog-Engineer's-Pocket-Reference-TI.md)
	- [ADC-PrecisionLABS-TI](https://github.com/SuperChange001/hw_learning_material/blob/master/ADC-PrecisionLABS-TI..md)
	- [OPA-PrecisionLABS-TI](https://github.com/SuperChange001/hw_learning_material/blob/master/OPA-PrecisionLABS-TI.md)
	- [新概念模拟电路](https://github.com/SuperChange001/hw_learning_material/blob/master/Analog-Circuit-compilation-yang_notes.md)
3. EMC：
	- [EMC_Brief_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/EMC_Brief_notes.md)
	- [产品EMC设计](https://github.com/SuperChange001/hw_learning_material/blob/master/Product_EMC_Evaluation.md)	
3. 信号完整性：
	- 说明：我们在设计低速电路的时候已经有了部分考虑
	- [SI](https://github.com/SuperChange001/hw_learning_material/blob/master/SI_notes.md)
3. 仿真：
	- 说明：暂时只有用SPICE模型对模拟电路的仿真，如瞬态响应，环路稳定性，噪声分析等。后续会加入HyperLynx的传输线信号完整性仿真的内容。
	- [LTspice_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/LTspice_notes.md)


3. 总线：
	- 说明：各种总线的原理，是做嵌入式控制板的底层。会用和搞懂搞清楚是两码事。跑通和稳定可靠也是两码事。
	- [RS485_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/RS485_notes.md)
	- [CAN_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/CAN_notes.md)
	- [SPI_IIC_UART_notes](https://github.com/SuperChange001/hw_learning_material/blob/master/SPI_IIC_UART_notes.md)
	- [Ethernet PHY](https://github.com/SuperChange001/hw_learning_material/blob/master/Ethernet.md)
	- `无线总线`

4. 传感器：
	- 说明：单纯研究传感器是没有前途的。关键是Sensor+OPA+ADC整个信号链路要了解。不然就会是一头雾水。
	- [温度-惠更斯电桥](https://github.com/SuperChange001/hw_learning_material/blob/master/Sensor/Temp.md)
	- [Hall Effect](https://github.com/SuperChange001/hw_learning_material/blob/master/Sensor/Hall_Effect.md)
	- [压力](https://github.com/SuperChange001/hw_learning_material/blob/master/Sensor/Pressure_Sensor.md)
	- [基于CSA的电流检测](https://github.com/SuperChange001/hw_learning_material/blob/master/Sensor/Current.md)
	- [环境光检测(暂不包含微弱信号检测)](https://github.com/SuperChange001/hw_learning_material/blob/master/Sensor/Optical.md)

2. 数字：
	- `STM32最小系统设计`
	- `Xilinx ZYNQ-7000series design`
4. 软件：
	- [C](https://github.com/SuperChange001/hw_learning_material/blob/master/Software/C_notes.md)
	- [ZYNQ Notes1](https://github.com/SuperChange001/hw_learning_material/blob/master/FPGA/ZYNQ_notes.md)
	- [ZYNQ Notes2](https://github.com/SuperChange001/hw_learning_material/blob/master/FPGA/ZYNQ_notes2.md)
	- [ZYNQ_PS](https://github.com/SuperChange001/hw_learning_material/blob/master/FPGA/ZYNQ_PS_notes2.md)
	- [Matlab入门](https://github.com/SuperChange001/hw_learning_material/raw/master/PDF/Matlab入门.pdf)
	- `Raspberry_notes`
	- `Python_notes`
	- `Linux_notes`
4. 数学：
	- [线性代数](https://github.com/SuperChange001/hw_learning_material/blob/master/Math/Linear_Algebra_notes.md)
	- `高等数学`
	- `概率论`
	- [三角级数，傅里叶变换和拉普拉斯变换](https://github.com/SuperChange001/hw_learning_material/blob/master/Math/Fourier_Laplace.md)
4. 英语：[IELTS Preparation](https://github.com/SuperChange001/hw_learning_material/blob/master/IELTS_arrangement.md)
3. 其他书籍：[总结](https://github.com/SuperChange001/hw_learning_material/blob/master/Books/Books_Summary.md)
4. Python实用脚本：[总结](https://github.com/SuperChange001/hw_learning_material/blob/master/Script/readme.md)
	
# 3. 说明
1. **硬件工程师不是抄抄抄，抄以前的设计，抄Datasheet里的Typical Application**。要对硬件的底层，硬件背后的原理有认识。**深入每一个元件的选型和参数**，都要有个specification。
2. 很多电路，我们不得不承认，随便搞搞也能凑合使用。不分析电源的环路稳定性，运放的稳定性，运放和ADC的采样精度，在95%的时候，不会出问题。硬件就会越做越low，陷入内卷。
3. 硬件工程师的吃饭家伙其实很多。叠加定理，KCL，戴维南定理，时间常数，傅里叶变换，波特图，微积分，线性代数，概率论，电磁场和电磁波，C和操作系统。多搞搞吧。和广大苦逼的同胞互勉把。 
6. 硬件可以做的不好，但是英语一定要好。**学好英语，是世界上性价比最高的技能**。不得不说，国内的好教材真的太少了。建议大家都去看英文的教材，这个语言转换的时间肯定是值的。就算同样是TI，国内的E2E论坛和培训教材，也是差了英文版的一个档次。
7. 做好硬件，是一门多学科交融的事，只是现在大家都没时间去好好学习一门技能了。现在的硬件，集成度已经越来越高，芯片原厂也越来越简化电子工程师的设计难度。再加上大量的典型设计，参考设计。所以跑通一种芯片门槛很低了。难的是理解芯片原厂为你做了什么，芯片的底层结构是怎么样的，以及怎么样根据我们的应用去优化一些参数，无论是出于特殊场景的稳定性考虑还是降成本的功能裁剪。   

# 4. 基本功
1. 基本元件：
	1. R C L的类型，容差，非理想参数，非理想的效应。
	2. BJT。先把电路用对。工作点分析，小信号分析。损耗分析
	3. MOSFET。先把参数理解对。米勒效应，开关损耗，导通损耗。
2. 电源：
	1. 电源的基本拓扑，BUCK BOOST FLYBACK
	2. 电源的输入电容，输出电容，电感，MOSFET的选型
	3. 电源layout的关键点，电压突变和电流突变的环路
	4. 电源的环路稳定性分析，补偿的方式。环路稳定性的测试
	5. 纹波测量，噪声测量，line regulation 和 load regulation
1. 运放：
	1. 容差分析和非理想参数的理解
	2. 噪声分析和计算
	2. 环路稳定性分析，补偿的方式。环路稳定性测试
	2. 放大电路
	2. 滤波电路
		1. SK和MFB设计高阶滤波器
		2. 巴特沃斯，切比雪夫，贝塞尔的区别
	1. 电流检测
1. ADC：
	1. 理解ADC的采样和保持，对Vin和Vref的影响  
	2. ADC的类型和原理
	2. 理解容差分析和非理想参数
	2. 量化噪声，和前端OPA引入的噪声
	3. OPA和ADC接口电路的设计
	4. Vref的需求，和对应的设计。
	5. 带宽限制和抗混叠
1. EMC：
	1. 理解麦克斯韦方程组
	2. 理解偶极子天线和环形天线的辐射模式
	3. 理解电场辐射和磁场辐射。了解远场和近场
	2. 理解测试项和测试标准
	2. 理解LISN或者AN的测试原理
	3. 理解共模电流的环路
	4. 理解常见的干扰源
	5. 理解常用的整改方式
1. 信号完整性：
	1. 对自己，对别人，对空间
2. 总线和原理：
	1. 不是简单的一个发数据一个接受到数据就万事大吉了。要理解PHY的底层。
	2. RS485
	2. CAN：
	3. SPI
	4. IIC
	3. USB
	4. Ethernet
2. 操作系统
	1. Linux是未来。先会使用Linux，然后再看看内核，自己做驱动吧。


# 5. 声明
- 欢迎阅读我关于硬件系统的一些理解。有问题可以留言。
- 也欢迎大家转载，但是转载请注明来源和作者。
- 如果有任何无意侵犯他人权益的行为，请联系我。