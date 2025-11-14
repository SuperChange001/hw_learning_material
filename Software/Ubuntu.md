
# 1. Ubuntu in VMware

这篇文章主要记录了在Vmware Fusion里安装和使用Vivado。

主要涉及的内容：

1. 安装vivado
2. 安装Jtag驱动
3. 安装putty获取USART log

## 1.1. General

```
# install vmware tools
sudo apt-get update
sudo apt-get install open-vm-tools
sudo apt-get install open-vm-tools-desktop
# 显示share file
sudo /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other
# mount the nfs shared folder
sudo mount -t nfs  -o resvport 172.16.31.134:/home/andrew/work ~/mnt/new_disk

#查看所有硬盘
ls /dev/sd*
#查看磁盘信息
sudo fdisk -l
#查看磁盘使用量
df -lh
#查看文件使用量
du -sh [name]

# 挂载硬盘
sudo mount /dev/sdb1 /mnt/disk
# 卸载硬盘
sudo umount -l /mnt/disk 
```

## 1.2. Expand root disk

1. setting in the Vmware, expand the file size
2. install the `gparted`
3. Run the `gparted`
4. Draw the bar of /dev/sdb1 to expand the root size
5. Only the unformated disk can be used to expand the root, so maybe need to delete some partial firstly



## 1.3. Auto mount

```
# check the UUID
sudo blkid
# auto mount
sudo vim /etc/fstab
# add line in the end of  the file
UUID=087AA7CC7AA7B4BA   /home/andrew/mystorage  ntfs    defaults    0   0
```

## 1.4. Serial-port authorization

https://www.jianshu.com/p/4b861297b6b3

```
sudo vim /etc/udev/rules.d/70-ttyusb.rules
KERNEL=="ttyUSB[0-9]*", MODE="0666"

sudo chmod a+rw /dev/ttyUSB0
or
sudo usermod -a -G dialout andrew

```

## 1.5. Etch SD card  

```
# show the list of all disk
diskutil list
# remove the disk of SD to etch Img file 
diskutil unmountDisk /dev/disk5
# etch Img
sudo dd if=~/rpi2.img of=/dev/rdisk5 bs=1m

# eject SD card
diskutil eject /dev/disk5
```

```
# options
# show progress bar
sudo pkill -INFO dd   # mac系统
# or Ctrl+T
```



## 1.6. Root authorization 

```
# root passwd is not configured
sudo -s
# passwd exist
su
```

## 1.7. Vivado enviroment

```
source /opt/Xilinx/Vivado/2017.4/settings64.sh
source /opt/pkg/petalinux/settings.sh

# SDK
xsdk
```

