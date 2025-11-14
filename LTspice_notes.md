# 1. LTspice记录
## 1.1. 参考资料
1. [所有笔记的链接](https://github.com/SuperChange001/hw_learning_material)    
2. 内置的help文档。这里面基本上把所有问题都讲了。
2. ADI的官网，貌似是这个软件的作者会写一些常用的指导。
## 1.2. 缩写
spice：Simulation Program with Integrated Circuit Emphasis
## 1.3. 总结
要掌握spice的网表接口：name nodeA，nodeB。有些时候，还是要看一下LTspice生成的网标的。也要看一下第三方提供的网表到底是什么东西。  
LTspice的使用，第一阶段是会用这个软件。就像画schematic的软件一样，用软件只是一个手段，不是目的。目的是仿真好软件。这个软件我们会设置就行。花个两三天，把help文档都读完，基本就上手了。难的是怎么去建模我们的电路。包括怎样才能正确测得Aol，环路增益，闭环增益，**蒙特卡洛分析**。所以，后续打算把常用的一些LTspice的电路也放上来。虽然我手上已经绘制了一些了，但现在还比较杂乱。  
常用命令：
1. 时域分析： `.tran 1ms`：暂态仿真
2. 交流仿真：`.ac oct 25 .01 1g`
	1. oct是2倍频，有25个点
	2. 常用的还有dec
3. 参数扫描：`.step oct param R 1k 2k 4`
	1. 有个电阻的值要写成`{R}`
4. 直流扫描：`.dc V2 0 1 0.1 V1 5 10 1`
	1. 这个是看两个参数之间的关系的。
	2. 这个例子是输出关于V1 V2的两个变量的曲线
2. 噪声分析：`.noise V(out) V3 dec 100 100m 1Meg`
5. 定义参数：`.param switch_on 10`
6.  定义模型：`.model SW SW(Ron=1 Roff=1Meg Vt=.5 Vh=-.4)`



# 2. 基本操作
LTspice的tricks：
- **you first select the action and then the object**
- Right click once to cancel the current wire
- You can draw wires through components such as resistors. The wire will automatically be cut such that the resistor is now in series with the wire.
- If you give a node a name starting with the characters "$G_"; as in for example, "$G_VDD"; then that node is global no matter where the name occurs in the circuit hierarchy
- For most users, this is the only method you should ever consider for adding third-party models defined as subcircuits since all the details are handled for you
- 右键器件，就可以打开datasheet或者仿真fixture
- 有些时候，按住command键或者ctl键，再单击，出现的效果会不一样。
- If you click the same voltage or current twice, then all other traces will be erased and the double clicked trace will be plotted by itself
- You can also probe the current in a wire. To do this, hold down the Alt key and click on the wire.
- V(n001,n002)是这两个网络的电压差
- ![](https://gitee.com/AndrewChu/markdown/raw/master/1598264208_20200815164504201_1311068592.png )
- You can measure differences in this manner without performing the zoom by either pressing the Esc key 
- Whenever a waveform plotting window is the active window, the menu commands File=>Save and File=>Open allows you to read and write plot configurations to disk
- If you want to use something other than the default values, you will have to write a .option statement specifying the values you want to use and place it on the schematic or keep the settings in a file and .inc that file
- 修改数据库 ` ~/Library/Application Support/LTspice/lib/cmp/standard.ind`在里面添加信息



# 3. 仿真命令
仿真模式：![](https://gitee.com/AndrewChu/markdown/raw/master/1598264208_20200815152206067_300472727.png)
命令：![20200824183717848_1823840452](https://gitee.com/AndrewChu/markdown/raw/master/1598265738_20200824184144590_1747854157.jpg)
- 新建directive：
	1. 按下s
	2. 输入.
	3. 然后输入命令
	4. 可选择是文本还是命令。
	5. 可以使用`#`或者	`;`注释一行命令
1. **常用命令：**
	1. 时域分析： `.tran 1ms`：暂态仿真
	2. 交流仿真：`.ac oct 25 .01 1g`
		1. oct是2倍频，有25个点
		2. 常用的还有dec
	3. 参数扫描：`.step oct param R 1k 2k 4`
		1. 有个电阻的值要写成`{R}`
	4. 直流扫描：`.dc V2 0 1 0.1 V1 5 10 1`
		1. 这个是看两个参数之间的关系的。
		2. 这个例子是输出关于V1 V2的两个变量的曲线
	2. 噪声分析：`.noise V(out) V3 dec 100 100m 1Meg`
	5. 定义参数：`.param switch_on 10`
	6.  定义模型：`.model SW SW(Ron=1 Roff=1Meg Vt=.5 Vh=-.4)`
	7. func函数：
		1. `.func Pythag(x,y) {sqrt(x*x+y*y)}` 
		1. `.param u=100 v=600`
		2. `R1 a b {myfunc(u,v/3)}`
	1. 变压器：` k l1 l2 1` 
		1. 变压器的耦合。电感量是圈数的平方
	3. 测量：`.meas VoutAvg avg V(out)`
		1. 数据会保存到errorlog里
		2. 配合step还能画图
	3. FFT参数不压缩: ` .OPTIONS plotwinsize=0 numdgt=15`
	4.  参数扫描：
		1. `.step param; A parameter sweep of a user-defined variable`
		1. `.step param R1 list 22.5k*(1-.01) 22.5k*(1+.01) 22.5k`
		2. `gauss(x); A random number from Gaussian distribution with a sigma of x`
		3. `flat(x); A random number between -x and x with uniform distribution`
		4. `mc(x,y); A random number between x*(1+y) and x*(1-y) with uniform distribution.`
	2. 导入Pspice模型
		1. 从网站上下载有.subckt的模型，文件名应该是.LIB的
		2. 在SCH里添加`.include ~/Desktop/OPA192.LIB`
		3. 找一个通用的运放opamp2，把value改成OPA192
			1. 这样就把这个通用的模块变成了OPA192，注意，他用的是管脚顺序匹配，所以IO的名字不一样没关系，只要顺序一样就行
			2. 如果找不到一样的管脚的元件，那就可以用LTspice打开这个.LIB，然后在.subckt这一行generate symbol。
			3. 可以用失调电压或者增益带宽积来验证

# 4. MAC 快捷键
部分MAC的快捷键也和Windows不一样，不如RCL都没有
快捷键：![20200824183717848_1823840452](https://gitee.com/AndrewChu/markdown/raw/master/1598265739_20200824184213753_1340600800.jpg)

MAC的directive没有UI，只能按照Help里的说明和Example里的例子来编写。考验你理解能力的时候到了

# 5. 单位
单位不区分大小写
m：是mili
meg：是M
![](https://gitee.com/AndrewChu/markdown/raw/master/1598264205_20200815141923169_24550794.png )


# 6. 波形显示
把鼠标放在波形的名字上，会出现提示
- 按住波形，拖到下个网络，就会显示V1-V2
- 可以显示电流探头
- 多窗口
	- 右键+ add plot panel
	- 双击窗口，就会激活一个窗口	
- 反向交叉探头：显示原理图的网络
	- cmd+单击
- 数学运算
	- 查看可用的数学运算：查看Help
	- FFT：右键---view里选择

- 波形测量：点击波形名字
	- 均值和RMS值：
	- 波形的数学计算：
	- 使用curve测量波形


# 7. 导入第三方spice文件
使用.LIB文件，里面会有`.subclk`这一行，右键可以自动生成模型。  
但是生成的模型，电路符号都会变，很丑而且不方便使用。自己画个类似的也很累。  
可以使用`.include path`把.LIB文件包含进来，再指定模型的名字。  

# 8. 利用errorlog
使用`.meas`命令，可以把指定的参数保存到errorlog里。同时errorlog也可以直接画图。

# 9. 蒙特卡洛分析
这个一般是在容差分析的时候使用的，在LTspice里使用这个需要一定的技巧。可以在网上查找一下软件作者推荐的方式

# 10. FAQ

## 10.1. 仿真很慢怎么办
一般都是不收敛了，我也不知道怎么办。
可以看看是不是运放没有一个合适的直流工作点