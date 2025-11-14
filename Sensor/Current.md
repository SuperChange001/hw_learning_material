# 1. Current


## 1.1. 参考资料
1. [电流检测](https://training.ti.com/ti-precision-labs-current-sense-amplifiers-current-sensing-different-types-amplifiers?context=1139747-1139745-1138708-1139729-1138709)
## 1.2. 名词解释
- shunt：电流检测电阻
- OPA：operational amplifier
- DA：Difference amp
- INA：instrument amp
- CSA：current sencing amp

## 1.3. 总结：


# 2. 基础
1. Vcm需要关注：
	1. Vcm是否在运放的输入范围内
	2. Vcm是否是波动的，会影响输出的失真。因为Vcm很有可能是分档的
1. 高边检测还是低边检测：
	1. 看Shunt电阻的位置。不同的检测方式会影响被检测的电路。因为shunt电阻的是入侵式的检测
	2. 如果是低边，那么会检测不出来load短路。因为Vcm都是0
1. 单端还是差分：
	1. 单端信号，会把走线的分布电阻也计算进去。所以测试不准。
	2. 差分信号：可以抑制共模干扰，也可以把寄生参数消除。
1. CMRR是有两层意思的：DC CMRR和AC的


# 3. 检测的方式
## 3.1. 直接检测
1. 最简单的方式
	1. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379729_20200906155947437_649396228.jpg)

## 3.2. 4种运放的方式
1. 使用运放进行信号放大和信号调理是必要的。但是有很多种方式达成这个目标
2. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379730_20200906160147084_193658482.jpg)
3. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379737_20200906160822131_188894281.jpg)
### 3.2.1. 普通OPA
1. 最普通。但是要考虑很多非理想的参数
	1. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379732_20200906160211349_1476203973.jpg)
### 3.2.2. 差分OPA
1. 使用DA，可以解决Vcm的问题。但是阻抗的影响需要考虑
	1. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379733_20200906160247889_1383523063.jpg)

### 3.2.3. 仪放
1. INA和DA返过来，不用考虑阻抗，但是Vcm不能高于Vcc
2. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379734_20200906160514925_1680135916.jpg)



### 3.2.4. CSA电流检测OPA
1. CSA是专门用来做电流检测的。
2. 原理：
	1. 在DA的基础上，加入输入级，可以调节阻抗和Vcm。达到专门用来做电流检测的目的
	2. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379737_20200906160755173_301994788.jpg)
	3. 输入级的原理：
		1. ![Screenshot-2020-09-06 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599379739_20200906160841696_119838485.jpg)
	1. 输出电流和输出摆幅是有关系的
		1. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599381729_20200906163938183_357322081.jpg)



# 4. 误差
## 4.1. 误差的种类
1. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599381730_20200906164122435_303664411.jpg)
2. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599381731_20200906164155209_750242328.jpg)
## 4.2. offset error
1. 主要三个来源：
	1. Vos
	2. PSRR
	3. CMRR
	4. 注意，PSRR和CMRR会标识是参考输入端
	5. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599381730_20200906164139450_242279088.jpg)
1. 因为是个固定值，所以在输出低的时候，误差占比会很大。而且也会随着温度的漂移，变化很大
2. 避免：
	1. 选一个好的器件。或者把输出变大。
	2. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599381728_20200906163835301_149872146.jpg)

## 4.3. Gain error
1. 特点：
	1. 误差的值和输出的值是线性的，不会变的
	2. 增益误差的三个来源：初始的增益误差，增益误差的温漂，增益误差的非线性
	3. 一般来说，初始增益误差的值比较大
	3. 如果用了两点校准，那么初始的增益误差可以消除
	4. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599383070_20200906170326080_2089054479.jpg)
	5. 同时要注意，手册里给出的增益误差，不是在最严格的轨到轨测试的。所以我们的输出要留出余量
	6. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599383071_20200906170414681_1476979713.jpg)
1. 计算增益误差：
	1. ![Screenshot-2020-09-06 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599383074_20200906170426710_1969012092.jpg)

## 4.4. CMRR
1. CMRR有两层意思要理解：
	1. 直流的CMRR：就算CMRR不变也会引起Vos
	2. 交流的CMRR：如果有AC变化，CMRR会更加恶劣
	3. ![Screenshot-2020-09-06 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599437357_20200907080826748_1106594501.jpg)
	4. ![Screenshot-2020-09-06 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599437357_20200907080903538_1003641555.jpg)
	5. ![Screenshot-2020-09-06 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599437358_20200907080907598_1146969215.jpg)


## 4.5. PSRR
1. ![Screenshot-2020-09-07 AM11](https://gitee.com/AndrewChu/markdown/raw/master/1599450750_20200907115204648_1409284990.jpg)
## 4.6. 采样电阻误差
1. ![Screenshot-2020-09-07 AM11](https://gitee.com/AndrewChu/markdown/raw/master/1599450751_20200907115224443_1248196758.jpg)

## 4.7. 温漂
1. 温漂的影响是全方面的。会影响offset error也会影响Gain error。同时对采样电阻也会有影响。优化的方式，也就是选一个温漂小的各种器件。或者加入温度校准，单点或者双点校准可以改善一部分的温漂。
2. ![Screenshot-2020-09-07 AM8](https://gitee.com/AndrewChu/markdown/raw/master/1599447669_20200907105959632_1482199719.jpg)