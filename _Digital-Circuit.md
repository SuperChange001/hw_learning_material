# 1. Digital-Circuit




# 2. FAQ
## 2.1. NAND NOR EMMC flash的区别
1. EMMC是集成了NAND 和NAND的控制器，使得控制变得简单和统一
2. NOR 容量小，但是代码可以直接运行。
	1. 擦的慢，但是可以随机读取
	2. 成本高
	3. 擦写次数小，10w次吧
3. NAND一般是带一块小的NOR作为bootloader运行代码
	1. 只能一块一块读
	2. 每bit的价格便宜
	3. 是个大块文件的存储
2. DRAM SDRAM SRAM DDR
	1. DRAM：动态随机访问内存
		1. 需要不断刷新才能保持住数据
	2. SDRAM：同步动态随机访问内存
	      1. 需要时钟同步，但是方便数据读取
	      2. 比DRAM快
	3. SRAM： 静态RAM
	      1. 不需要不停刷电。容量小，但是速度很快。贵。CPU里的cache