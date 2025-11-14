# 1. Linux_阿尔法
# 2. 阿尔法-Linux

1. 怎么整理ubuntu的磁盘空间，占用太大了

## 2.1. 初学

### 2.1.1. 环境配置

- vmware
    - 区分windows：vmware workstation
    - MAC：vmware fusion
- 安装ubuntu 16.0版本
- 分配磁盘空间给vmware，注意要很大的空间。配了一个固态硬盘给虚拟机
    - 扩容要分两步，参考其他教程
- 注意网络要选择桥接
    - 使用`ifconfig`查看ipv4的ip
    - 在Mac使用ping测试ip
    - 使用 `ps -e |grep ssh` 确认ssh服务是否开启
        - 没开启的要用  `sudo apt-get install openssh-server`
    - 最后在mac使用`ssh name@ip`
        - 可以使用 `ssh-copy-id` command 来避免每次输入密码
    - 更换语言
        - 直接在系统设置里更换
        - 如果出现软件包损坏
            - `sudo apt-get install update`
            - `sudo apt-get install upgrade`
            - sudo apt-get install  language-pack-zh-han*

### 2.1.2. 虚拟机连接USB设备

注意选择的系统就可以了，同时要注意选择usb3.0

### 2.1.3. shell命令

常用的shell命令如下

1. ls
2. cd
3. pwd
4. clear
5. cat
6. sudo
7. su
8. cp
9. mv
10. mkdir
11. touch
12. rm
13. ifconfig
14. reboot
15. poweroff
16. shutdown
17. man
18. sync
19. find
20. grep
21. mount：把dev下的盘挂载到mnt下
22. umount：卸载的是mnt路径下的名字
23. du -sh path：这个path所有文件的信息
24. df： disk file 所有磁盘的信息
25. fdisk：磁盘分区
26. mkfs：`mkfs -t vfat /dev/sd*` 给分好区的磁盘格式化
27. Ps -e
28. top
29. File

### 2.1.4. 软件安装

- deb软件安装包
    - `sudo dpkg -I xxxx.deb`
- 源码安装
    - `make` 		`make install`
    - 

### 2.1.5. 文件体统结构

- /: 根目录
    - .  当前目录
    - .. 上级目录
    - ~   家目录
- /bin: 二进制文件
- /boot: 内核和启动文件
- /etc: environment configuration 系统配置文件
- /home: 家目录，用户都在这里面
- /lib: library 库文件
- /media:
- /mnt: mount
- /opt:
- /root:
- /sbin: root使用的二进制文件
- /srv: server 服务文件
- /sys: system 内核信息，虚拟文件
- /tmp: temporary
- /var: variable
- /usr: unix software repository 
- /proc: process

### 2.1.6. 磁盘管理

- 挂载的u盘

    - 首先出现在`/dev/sd*`里面

    - 然后需要mnt，unix会自动挂载

    - sdb：这是一个u盘

    - Sdb1：这个是u盘的第一个分区

        

### 2.1.7. 压缩和解压缩

- tar
    - ``tar -czf xxx.tar.gz xxx`` 压缩归档
    - ``tar -xzf xxx.tar.gz`` 解压缩
- rar
    - Mac不支持，就不试了
- zip
    - ``zip -r xxx.zip xxx`` 创建压缩的zip
    - ``unzip xxx.zip`` 解压缩

### 2.1.8. 用户与用户组

- 查询用户记录：``/etc/passwd``
- 查询密码：``/etc/shadow``
- 区分UID和GID
- 查询用户组：``/etc/group``
- 用户管理：
    - 添加：``adduser username``
    - 修改密码：``passwd username``
    - 删除用户：``deluser username``
    - 把用户归到指定组里：``usermod -a -G examplegroup exampleusername``
- 用户组管理：
    - 添加用户组：``addgroup groupname``
    - 显示系统所有组：``groups``
    - 显示成员在什么组：``id``
    - 删除用户组：``delgroup groupname``

### 2.1.9. 文件权限管理

文件的权限：

- 查看使用**ls -l**
- 分为read，write，execute。对应的4，2，1
- 权限分为：文件类型+所属用户的权限+所属组的权限+其他人的权限
- 修改文件权限：
    - chmod：
        - ``chmod 777 filename``
        - ``chmod a-w filename``
    - Chown:
        - ``sudo chown root:root filename``

### 2.1.10. 链接文件

链接：

- ``ln target newName``
- 硬链接：
    - 指向同一个inode
    - 具有同一个inode的文件互为硬链接
    - 改了一个文件，所有硬链接的文件都改了。
- 软链接：
    - 新建一个inode，指向之前的文件。类似于指针
    - cp命令对于一个软连接，会改变他原先的属性，要加上-d
        - Cp命令的软链接，如果不适用绝对位置，那么他就会路径错乱
    - 所以软连接都要使用绝对位置
- 不同点：
    - 软链接大小很小，硬链接文件很大
    - 软链接删除了原先的文件，所有链接都失效了。硬链接不会。硬链接用来防止误删
    - 硬链接不能跨文件系统，不能链接到目录。硬链接不常用。
- inode：文件存储的唯一位置。
    - 当文件的被引用位置为0，那么这个文件就会被删除

### 2.1.11. vim编辑器

详细的使用参见其他教程，这边只是强调几个常用的快捷键：

- dd：删除一行
- /abc：搜索。n，b上下
- U: 撤销
- .：重复上个动作
- yy：复制一行
- P：复制到下一行

### 2.1.12. Linux C编程

源码：

```c
#include <stdio.h>

int main(){
	printf("hello world!\r\n");
}
```

编译 ``gcc name.c -o main``

运行``./main``

### 2.1.13. Make工具和MakeFile

了解的不多。只知道Make可以调用makefile，一次性生成所有的编译文件，不用每改动一次问题，就把所有文件都编译一遍。

等具体用到这个工具的时候再仔细研究吧

### 2.1.14. shell脚本

太复杂，实现的功能和python差不多。自己不太可能会写，但是要会看别人写的shell script

## 2.2. 第二章



