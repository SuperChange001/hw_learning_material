# 1. Motor_Driver
水平有限，电机没搞懂。不要误人子弟

## 1.1. 参考资料
- [TI precision LAB](https://training.ti.com/ti-precision-labs-motor-drivers-motor-types?context=1139747-1138777-1139739-1138097)
## 1.2. 名词解释
1. BLDC： brushless DC Motor Driver

## 1.3. 总结
1. 有刷无刷指的是电刷，没有电刷作为换向器件，马达的寿命会提高，同时EMC会降低。但是控制的复杂度会上去
2. 有没有霍尔
3. 电流环
4. 电压环


# 2. 电机
市面上主要有：直流有刷，直流无刷，步进电机
- ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599460399_20200907135458831_2028181436.jpg)
## 2.1. 直流有刷
1. 有电刷。只要给一个方向的电，就会沿着一个方向转。
	1. ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599457809_20200907134957123_258875779.jpg)

2. 换向，就会需要H电桥。就要注意死区
3. 优点：简单，容易使用
	1. ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599457809_20200907135002686_408313312.jpg)
## 2.2. 直流无刷
1. 就是BLDC。和有刷的区别
	1. ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599457808_20200907134902466_2075010025.jpg)

2. 有转子和定子。一般都是线圈是转子
3. Y和△接线：驱动方式是一样的
	1. Y：效率高，转速低
	2. ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599457809_20200907134915326_1521985663.jpg)

## 2.3. 步进电机
1. ![Screenshot-2020-09-07 PM1](https://gitee.com/AndrewChu/markdown/raw/master/1599460399_20200907135448150_890992058.jpg)
# 3. 驱动器
## 3.1. 直流有刷
1. H桥
	1. 注意死区，这个是设计的关键。
	2. 一般都使用4个NMOS，因为便宜。所以要使用自举电路
	2. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460400_20200907140840327_399626987.jpg)
	3. 死区时间的时候。是从体二极管续流的。会发热
	4. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460400_20200907141013529_660824856.jpg)
1. 快速泄放：
	1. 因为从体二极管走，功耗太大。
	2. 所以可以把另外一对MOS开关打开。MOS导通之后，就像个电阻，不想BJT是有电流流向的。
	3. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460400_20200907141130405_821829919.jpg)

## 3.2. Step
1. 步进电机的优点
	1. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460400_20200907142719892_1649240902.jpg)
1. 步进电机的种类 
	1. 第二种用的多。第一种和第二种，看到的就是转子上有没有尺的区别
	2. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460401_20200907142938845_592380137.jpg)
1. 分为双极性和单极性的电机。我们主要讲双极性的
	1. 双极性的电路和有刷电机的很像
	2. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460401_20200907143019938_2112868277.jpg)
1. 控制方式分为电压型和电流型的
	1. 电流型的，因为可以控制电流变化率在额定范围内，让线圈的工作电压很大，所以可以更快地驱动。效果也更好
	2. 可以看到，驱动器和电机之间是4线的，2组线圈。每次一组线圈上电。
	3. 电压模式和电流模式的区别，也在于有没有检测电流的电阻
	3. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460401_20200907143210672_2110806755.jpg)
	4. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599460401_20200907143311816_1386539778.jpg)

2. 细分：
	1. 检测电流，就可以知道电机转动的角度了。从而实现了细分
	2. 细分让控制更加准确，运动更加平稳，噪声小。但是可能会出现丢步
	3. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464735_20200907153818051_207898080.jpg)
	4. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464738_20200907153829336_1757998433.jpg)

3. Control和Driver的接口
	1. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464738_20200907153902850_465289103.jpg)
	2. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464739_20200907153914897_1016819298.jpg)
	3. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464739_20200907153928436_365091749.jpg)
	4. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464740_20200907153935996_1810356276.jpg)
## 3.3. BLDC
1. 原理：
	1. 三个线圈，依次绕过去，吸引磁铁
	2. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468455_20200907164034534_332004925.jpg)
1. 保护机制：
	1. OCP：过流保护
	2. 过热
	3. 欠压
	4. 死区
	5. stall lock
	6. 反向发电保护
	2. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468456_20200907164211911_1396905656.jpg)

### 3.3.1. 有sensor
1. 可以使用编码器，或者hall
	1. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468457_20200907164532121_1400574554.jpg)
2. 使用hall
	1. 注意，这张图的波形，不是Hall的。是ABC三项流过的电流。所以可以是正的，负的，没有电流。
	1. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468457_20200907164421797_878347587.jpg)

3. 使用场景
	1. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468459_20200907164710039_1394519019.jpg)
	2. 各自的特点：
		1. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468460_20200907164721487_73248698.jpg)
		2. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468460_20200907164727522_1977609.jpg)
### 3.3.2. BEMF
1. 原理：其实就是法拉第
	1. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468457_20200907164545384_2063143691.jpg)
1. 测量方式：
	1. 测量浮空的端子：
		1. 处于Z状态的端子。是有上升或者下降沿的。也叫做window。就是下图标了Z的。
		2. 一般就是用在高速运行的应用，那就可以侧得到足够的BEMF
		2. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473382_20200907180501596_1259384104.jpg)
	2. 使用电流反推，我们知道线圈的电阻和电感的。
		3. ![Screenshot-2020-09-07 PM4](https://gitee.com/AndrewChu/markdown/raw/master/1599468458_20200907164635572_116355156.jpg)

### 3.3.3. 换向方式
1. 换向和很多参数有关系；
	1. 因为正弦和梯形电机的BEMF是不一样的，所以要区分
	2. ![Screenshot-2020-09-07 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599473386_20200907180741340_948962237.jpg)
	3. 换向角度：
		1. ![Screenshot-2020-09-07 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599473390_20200907180830362_408927161.jpg)
	1. 120°换向
		1. ![Screenshot-2020-09-07 PM5](https://gitee.com/AndrewChu/markdown/raw/master/1599473394_20200907180845360_729568026.jpg)
		2. 可以使用有传感器方案，也可以使用没有传感器
			1. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473400_20200907180912274_798929371.jpg)
			2. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473382_20200907180501596_1259384104.jpg)
	1. 150°
		1. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473913_20200907181809265_873313651.jpg)
	2. 180°
		1. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473914_20200907181815531_519044971.jpg)
	3. FOC
		1. ![Screenshot-2020-09-07 PM6](https://gitee.com/AndrewChu/markdown/raw/master/1599473915_20200907181824238_909143450.jpg)
	




# 4. BEMF--没搞懂
1. 就是线圈，可以感应到磁极的位置。这个感应电压就叫做BEMF
2. 没有搞懂BEMF的变化原理。
	1. ![Screenshot-2020-09-07 PM2](https://gitee.com/AndrewChu/markdown/raw/master/1599464741_20200907154040941_1752012440.jpg)
	2. ![Screenshot-2020-09-07 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599464742_20200907154334238_1583821328.jpg)
	3. ![Screenshot-2020-09-07 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599464742_20200907154425214_65224757.jpg)
	4. ![Screenshot-2020-09-07 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599464743_20200907154436913_864845185.jpg)
	5. ![Screenshot-2020-09-07 PM3](https://gitee.com/AndrewChu/markdown/raw/master/1599464743_20200907154526175_415774104.jpg)


# 5. 算法