# 1. TI-高精度实验室-ADC

## 1.1. 参考资料
1. [TI-precision-labs](https://training.ti.com/ti-precision-labs-data-converters?context=1139747-1140267)
2. [ADC噪声分析](https://www.ti.com/lit/wp/slyy192/slyy192.pdf?ts=1599364042567&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FADS124S08)
3. [TI在电机系统中的电压电流采样技术详解](https://training.ti.com/zh-tw/node/1146745)
3. [delta sigma ADC](https://training.ti.com/delta-sigma-adcs-overview)
## 1.2. 名词解释
- ENOB：effect number of bit
- SNR：signal noise ratio
- SINAD：signal to noise and distortion
- offset：偏差
- drift：漂移
- error：误差
- noise：噪声
- FSR：满量程
- NFS：负满量程
- PFS：正满量程
- LSB：least significant bit
- anti-aliasing :抗混叠
- CDAC：capacitive DAC
- EOS： electrical overstress
- SAR ADC: successive approximate ADC
- AFE: analog front end

## 1.3. 总结
1. 理解ADC的种类
	1. Pipeline：流水线
		1. 优点：非常快，带宽大。不常用
		2. 缺点：位数做不高，价格高
	2. SAR：successive approximate
		1. 优点：性价比高。延时比较小
		2. 缺点：有量化误差。采样频率比较低。
		3. 对Vref要求高，一个hold阶段，会不停地要给电容充电。
	3. Δ∑ ADC：
		1. 优点：可以减少量化误差。使用数字化的方式
		2. 缺点：cycle latency延时大。
		3. 利用了数字化级数，先过采样，然后再数字滤波把量化噪声也减少了,最后还要靠外部RC进行抗混叠。
	1. 双积分型：
		1. 输入给电容充电，然后在hold阶段判断多久放完电，就知道输入的电压值了。不过貌似不常见啊。
2. 理解ADC的非线性
	1. DNL
	2. INL
	3. NMC
	4. offset error
	5. Gain error
1. 理解ADC的原理：
	1. SAR ADC：采样和保持阶段。
	2. 因为Csh，CDAC
		1. 对Vref会有很高的动态范围。保持阶段，Csh在动作。
		3. 输入的管脚，如果直接接的Csh，会有稳定性的问题，要接Riso。最终的settling error 要小于1/2LSB
1. 理解码
	1. LSB
	2. FSR
	3. 计算SNR
	4. 理解量化误差导致的SNR公式的推导
1. 计算ADC的功耗：OPA两部分，ADC的保持阶段，ADC的数字通信部分
2. 计算ADC的噪声：OPA的噪声，电阻的噪声，ADC的量化噪声，Vref的噪声
3. 理解ADC的DC有效位数。理解噪声Vpp和RMS和∂的关系
3. 理解anti aliasing
4. 理解运放和ADC接口的Riso和C的作用
	1. 抗混叠
	2. 提供能量
	3. 减少稳态误差
	4. 提高环路稳定性
1. 理解ADC设计时候的容差：
	1. 蒙特卡洛分析：
	2. 因为之前说的非线性参数。选定关键参数，选一个好的器件
	2. 因为温度对这些非线性参数的影响。温漂很难校准
	3. 因为老化的影响。定时校准
	4. 因为器件本身的噪声。选一个好的器件最重要
	5. 电路的合理性。如果电路要求很多电阻都要匹配，那么这个电路实际价值就不高
	6. 尽量选用高容差的器件，电阻高精度，低PPM
	7. ADC带有自校准。注意，他是把输入短路了，然后校准自己，单纯做这个其实没多大意义



## 1.4. 关键参数
dnl和inl：![](https://gitee.com/AndrewChu/markdown/raw/master/1598284518_20200819090243858_69585225.png )

### 1.4.1. 电气参数
- 输入电容
	- 用于采样和转换
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284524_20200819090620744_529262572.png )
- 输入漏电流
	- 类似于运放，需要一个工作电流
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284525_20200819090637811_438781730.png )
- 输入阻抗
	- 一般的运放，接的是采样电容。因为大电流，所以运放的输出要接电容，引入了极点，要加Riso隔离
	- PGA内置了运放，所以有一定的输入阻抗
	- ![1598284517_20200818082851258_1767969462](https://gitee.com/AndrewChu/markdown/raw/master/1598285171_20200824235714572_1286540398.jpg)
- 输入电压：考虑这个参数要和运放输出的rail联合考虑
	- 工作输入电压：超过不正常工作
	- 绝对最大输入电压：超过可以会损坏ADC
	
- 参考电压端
	- 注意：Vref是有高频脉冲信号的管脚，要用宽带宽的buffer输出。需要小心对待。
	- 参考电压端的电压：不是随意地，要有一个范围
		- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284519_20200819090335817_1287772607.png )
	- 参考电压端的电流：要加一个电容续流
		- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284526_20200819090711799_145692312.png )


### 1.4.2. 纹波抑制  
- CMRR和 PSRR：都可以等效成输入端的误差，和Vos一样
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284524_20200819090558491_188880234.png )
- CMRR
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284523_20200819090543275_1344696066.png )
- SNR：signal noise rejection
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284527_20200819090727562_519330204.png )
- THD：total harmonic distortion
	- ADC采集运放输出的信号。输入的crossover distortion会影响THD。因为做成轨到轨，可能是两组NMOS在切换，他们的Vos不一样，导致输出波形失真。
		- 所以采用反向放大，可以稳定住Vcm
		- 采用0输入交越失真的OPA，可以用PMOS加电荷泵，显示单组MOS也可以输入到rail
	- ![](_v_images/20200815094405402_1163458812.png )
	- ![1598284521_20200819090525690_764802423](https://gitee.com/AndrewChu/markdown/raw/master/1598285171_20200824235833334_576260559.jpg)
### 1.4.3. 转换码参数
- 理想的码：LSB
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284528_20200819090742690_1009197220.png )
- DNL：differential no-linear 差分非线性：一个台阶的宽窄
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284530_20200819090812505_751832534.png )
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284531_20200819090829624_255619990.png )
- NMC：no missing code 丢码率
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284532_20200819090848887_1237877930.png )
- INL：integral no-linear：曲线弯
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284533_20200819090905260_192797374.png )
- offset and gain error
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284520_20200819090443107_1254011383.png )


# 2. ADC类型
- 按照采样原理：
	- ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940035_20200901132449751_1701446642.jpg)
- 按照输入端AINP和AINM的关系：4种
	- 单端：AINM接GND
	- 伪差分：AINM接Vref/2
	- 全差分:Vcm在Vref/2±0.1
	- 真差分：无限制
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284534_20200819090922590_1940125142.png )
- 按照输入电压范围：单极性和双极性
	- 单极性：只能输入正的电压。实际上Vdm也可以是负的
	- 双极性：正负电压都可以输入

## 2.1. Pipeline ADC
把flash ADC级联起来，
先用flash采集高5bit，然后用DAC输出，再采集下5bit
### 2.1.1. flash adc
内置了2N-1个比较器，和一系列的电阻分压。
只能做到5，6bits，快

## 2.2. SAR ADC
先放1/2 得到最高位的0还是1，然后再1/4 1/8
要关注的是SAR ADC的SH电容，在sample(acquisition)和hold(conversion)里都用了开关在切换，所以对Vin和Vref的影响都非常大。
所以这两个电压都要用宽带宽的驱动器，然后再接一个大电容。从而实现快速给Csh充电

- 简单原理：
	- 有一个CDAC，第一次输出最高那位比较，输出0/1；
	- 然后比较次高，输出0/1
	- ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940036_20200901133044756_270727580.jpg)
	- ![1598284537_20200819102406841_1458580013](https://gitee.com/AndrewChu/markdown/raw/master/1598285172_20200825000016052_1798947564.jpg)
- 复杂原理：
	- Csh分成1/2 1/4 1/8....并联
	- 判断MSB：
		- sample阶段：Csh都接Vin
		- conversion阶段：1/2Csh接了Vref，剩下的接了1/2Csh。用电容的电压分配原理，两个电容的中心点电压1/2Vref-Vin. 这样，后级的比较器就能输出MSB是 0还是1
	- 判断MSB-1：
		- 先把上个阶段的电放掉
		- sample阶段：Csh都接Vin
		- conversion阶段：1/2Csh的状态根据MSB，1/4接Vref。剩下的类似
	- 多少bit的ADC就要比较多少次。
	- 注意，MSB的电流最大，因为电容最大：
		- i=C*∂v/∂t 或者直接从容抗来考虑
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284548_20200820085954300_997885285.png )
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284548_20200820090010215_1758185572.png )
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284545_20200820083719514_2041224119.png )
	- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284546_20200820083820924_802507208.png )
- SAR分类：
	- 内置运放的PGA，可以调节增益
		- 因为输入阻抗比较高，可以用跟随器直驱
	- 低成本的SAR：
		- 里面有开关电阻40欧，采样电容40pf。
		- 如果用跟随器直接驱动，会增加了一个极点，环路稳定性会有问题。所以要有Riso
			- 组成的RC网络功能：改善极点；低通抗混叠；C给后端的采样电容提供大电流
			- 貌似，使用一个高带宽的就可以直接驱动电容？
### 2.2.1. SAR ADC 总结
- Vin
	- PSRR，对高频信号抵抗弱。
- Vref
	- 大的瞬态电流驱动能力，因为要驱动容性负载
	- 低噪声，因为直接使用了Vref作为比较基准
	- 可以很快的Settling down，不然电容采集到的电压不准
	- 使用参考IC
	- 如果使用Buffer：
		- 如果Buffer的带宽不够，就是动态响应不够，那就就会导致波形失真，就会有很高的谐波，THD就会很差
		- 可能参考IC自带Buffer，可能ADC自带Buffer。或者IC的带宽很大，输出阻抗很低，那就不用Buffer
		- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284549_20200820090247582_614411301.png )
- 误差校准：![](https://gitee.com/AndrewChu/markdown/raw/master/1598284547_20200820084918269_234650911.png )


### 2.2.2. 抗混叠
AFE前端的RC不是为了抗混叠的。可以从截止频率来分析。这个RC是为了提供大电容给后端采样的Csh使用。
- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948671_20200901141909813_461831493.jpg)
- 如果没有RC：
	- 运放可能会震荡，因为驱动了容性负载。同时运放的带宽也不够，输出会被拉低，采到的信号不准。
	- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948672_20200901142021308_146196891.jpg)
- 抗混叠，使用的Rf和Cf
- 


## 2.3. Δ∑ ADC
1. 原理：
	1. 使用了一位的CDAC，里面还有积分器就是∑，Δ是输入和最开始的CDAC的0/1的差。经过积分器的不断加权后，就变高位了。
	2. ![Screenshot-2020-09-01 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598949403_20200901163451635_456492895.jpg)
	2. 使用过采样：可以把白噪声的幅值变低，但是总量是不变的
	2. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940037_20200901133733100_672122940.jpg)
	3. 先把模拟信号调制为数字信号，增加数字滤波器，滤除不要的高频
		1. 对白噪声是个高通
		2. 对有效信号是个低通
		3. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940037_20200901133859401_1360158130.jpg)
		4. 调制阶段：
			1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940038_20200901134200926_117776356.jpg)
		1. 数字滤波阶段：
			1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940039_20200901134226640_906961661.jpg)
			2. 数字滤波器的选择：
			3. sinc：![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940039_20200901134305308_168464727.jpg)
			4. flat：![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940040_20200901134321160_694353003.jpg)
1. 制约参数
	1. ![Screenshot-2020-09-01 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598948675_20200901160921192_93048890.jpg)
### 2.3.1. 采样和保持
- 采样阶段：
	- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948673_20200901160633956_1438313291.jpg)
- 保持ref阶段：
	- [Screenshot-2020-09-01 PM3.54.19.jpg](file:///Users/andrew/Desktop/Screenshot-2020-09-01%20PM3.54.19.jpg)
- 同样也需要bulk cap	
	- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948674_20200901160821167_1894591323.jpg)
### 2.3.2. Vref设计
- 和SAR ADC类似。不过这个ADC的Vref在一个周期内，只会采样一次。但是也是对电容充电，还是比较恶略的。
- ![Screenshot-2020-09-01 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598948675_20200901161151883_1091652278.jpg)
- ![Screenshot-2020-09-01 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598948676_20200901161302179_522121957.jpg)


### 2.3.3. 噪声分析：
1. 噪声包括AFE的运放噪声+ADC本身的噪声+Vref的噪声
2. 貌似量化噪声被忽略了。
3. ![Screenshot-2020-09-01 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1598948676_20200901161403546_1168416398.jpg)
4. 时钟的jitter也会影响SNR
	1. ![Screenshot-2020-09-01 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1598948676_20200901162333588_1094223668.jpg)

### 2.3.4. 抗混叠设计
- 配合内置的数字滤波器，在外面增加RC低通配合。注意fc的关系
	- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948669_20200901141053026_1800570799.jpg)
- 加了RC。如果C不匹配，就会把共模信号变成差模信号。为了抑制这个，要使Cdm大于10*Ccm，那么差模的抑制能力，可以把共模产生的差模吸收了。
	- ![Screenshot-2020-09-01 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1598948670_20200901141344925_1531936261.jpg)


## 2.4. SAR和Δ∑比较
1. 什么时候采样
	1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940041_20200901135855075_1178762091.jpg)
1. 采样的延迟时间：
	1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940042_20200901135923773_1205481520.jpg)
1. SAR的优点：
	1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940043_20200901135950925_686675916.jpg)
1. Δ∑的优点：
	1. ![Screenshot-2020-09-01 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1598940043_20200901140028287_1616517396.jpg)


# 3. SNR THD
- SNR：是信噪比。服从高斯分布的
	- SNR优化：满量程输出，因为失真的量是固定的
	- 从SNR退出噪声均方电压
		- 信号RMS：满量程/2*0.707
		- 噪声RMS：容易得
- THD：是谐波失真。波特图上有明显的峰值，是基波的10次谐波


# 4. 容差分析：
- offset误差+Gain误差：
    - offset误差：
        - 每个器件都有误差，器件本身决定的
    - 增益误差：
        - 电阻的精度
        - Aol不是无穷大，导致Auf也有误差
    - 最大误差和统计误差
        - 最大误差：就是把误差直接相加
        - 统计误差：多个独立的高斯分布函数相加，新的函数也是一个高斯分布。新的∂是∂的均方根值。一般取3个∂
    - 把这两个误差，都当成是线性方程。最终拟合也用线性方程。
        - 测试两个点，可以得到斜率和截距
            - 0V校准：现实中成本，太大。可以简单地默认斜率不变，输入短接测试截距。
                - 注意，要用双极性的ADC或者差分输入的，只要能测到负电压就行
    - 自校准ADC：只是校准ADC本身的offset
    - 无法校准的误差：
        - 温漂
        - 积分非线性，差分非线性
        - 老化
        - 温度迟滞
    - 蒙特卡洛分析：
	    - 就是所有的参数都扫描一遍
    - 降低噪声
        - 低噪声的器件
        - 降低电阻
        - 降低带宽
        - 数字平均：针对多个独立的高斯分布
            - 噪声降低到原来的sqrt(N)
    - 例子：
        - 从SNR反推ADC的噪声RMS。
            - Vfsr_rms=满量程/2*0.707
        - 测试OPA的噪声的时候，输入信号不能为0，因为运放工作不起来
## 4.1. 误差校准：
基本原理：![](https://gitee.com/AndrewChu/markdown/raw/master/1598284547_20200820084918269_234650911.png )
## 4.2. ADC的SNR
- 三方面：ADC量化误差+OPA白噪声+Vref
	- ![1598284535_20200819092725122_1634314885](https://gitee.com/AndrewChu/markdown/raw/master/1598285175_20200825000516397_385174529.jpg)
	- ![1598284536_20200819095523068_1614427065](https://gitee.com/AndrewChu/markdown/raw/master/1598285176_20200825000605973_1916415387.jpg)
	
# 5. OPA和ADC接口
- 关键参数：
	- R
	- C
	- 运放的带宽：
		- 如果不接RC，就要用高带宽的
		- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284539_20200819102751911_1588817201.png )
		- ![1598284541_20200819103009443_823251549](https://gitee.com/AndrewChu/markdown/raw/master/1598285175_20200825000428706_603297964.jpg)
	- 最终目标：**在采样时间结束后，误差电压小于0.5LSB**
- ADC参数：
	- ![1598284540_20200819102923001_1439030409](https://gitee.com/AndrewChu/markdown/raw/master/1598285174_20200825000338910_1621431620.jpg)
- ![1598284538_20200819102515003_828447986](https://gitee.com/AndrewChu/markdown/raw/master/1598285173_20200825000253355_33748830.jpg)

# 6. ADC的功耗计算
- ADC的采样模式：
	- 固定的转换时间。固定的，内部决定，转换好了存起来。转换好CS才能拉低，同时采样时间不固定
	- 外部转换时钟。CS了之后，才开始转换，和SCLK同步
	- 其他。cs了之后，先采样，再转换
- 功耗组成：
	- 运放：
		- Iq和输出端
	- ADC的模拟
		- 采样0耗能
		- 转换100%耗能
	- ADC的数字
		- 只有MISO脚耗能。P=V*I=V*C*V*N/f
- 决定因素：
	- 采样率：采样率越高，OPA的带宽要更大，Iq就会很大。ADC的模拟和数字转换也耗能更多。

# 7. EOS
- 三种器件：
	- 二极管：钳制住一定的过电压。
		- 如果信号持续比VCC高，就不能用
	- TVS
	- SCR：只有断电才能恢复

## 7.1. OPA和ADC电平不匹配
- 加肖特基二极管，做电平钳制。
	- 但是需要限流电阻，太大了会导致settling time变长，误差超过半个LSB。最终就是SNR和THD很差
		- 解决方式：把限流电阻放到负反馈环路里，就相当于增加运放的Z0，但是对输出无影响
			- 问题：会改变环路稳定性，需要分析相位裕度。这个时候，不能简单的用1/ß去和Aol去相交了。不过也可以算出F把
			
# 8. FFT
- FFT：
    - 锯齿波是奇次谐波的叠加
    - ADC的误差
        - 最少有量化误差噪声：6.02N+1.76。这个服从高斯分布，所以类似白噪声的底噪
        - 还有其他的非线性，如积分非线性，会带来高次谐波。这个就不是底噪的样子了
    - FFT的公式：
    - 采样频率fs——频谱还原出一半的频率。奈奎斯特采样定理
    - 采样点数N——分辨率。fs/N
    - 频谱泄露：
        - FFT之后，10.1khz的信号，不在频率的点上，就会导致10khz左右的频率都有信号
        - 改善：时域无限就行，N足够多，就肯定在点上
            - 但是时域波形不一定连续，所以要加窗口
                - 窗口：对主频不衰减，对旁瓣衰减。ADC用7阶-blackman
    - 抗混叠：
        - fs=10k，f=1khz和11khz采样到的波形是一样的。所以要抗混叠滤波，把高于1/2fs的信号都衰减到0.5个LSB
        - 注意：运放输出的RC不是为了滤波，是为了提供ADC采样时候的电流。也可以做成是抗混叠的
            - 如果没有这个RC，那么运放就要有更加大的增益带宽积，让采样保持电容充满电



# 9. FAQ
## 9.1. 仿真的工作点
交流分析和噪声分析，都要运放工作在线性区。   
所以测试运放的开环增益的时候，使用双电源比较方便

## 9.2. Buffer的特性
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284542_20200819104205136_151646422.png )
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284543_20200819104254987_1805809212.png )



## 9.3. 复合运放
前级的DC特性好，后级的带宽输出特性好
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598284544_20200819104342966_1996526680.png )

## 9.4. 带宽和容性负载
只有宽带宽的器件，才能更好地驱动容性负载。
就是要求能更快地给电容充上电，就相当于，要在高频段的驱动能力很强。
这个就是宽带宽的意义


## 9.5. OPA的Iq和其他参数的关系
静态电流越大：
- BW越大
- slew rate越大
- 噪声越小
- 功耗越大

## 9.6. 二极管和肖特基二极管
- 肖特基二极管
	- Vf小 0.3v
	- 漏电流大，但是受温度影响小
	- 反向恢复时间快
- 普通二极管
- TVS
	- 快，功率大
	- Vr，漏电流很小的阶段，判断是否工作
	- Vbr，开始起保护的电压
	- 为什么使用单相TVS
	- 寄生二极管会随着电压变化，所以谐波会很大
	- 同时也会组成一个低通滤波，电容会变，截止频率也会变
- zener
	- 稳压二极管，作为参考电压
	- 功率很小，可以一直反向工作



























