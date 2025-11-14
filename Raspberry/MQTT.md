# 1. MQTT

## 1.1. 参考资料
- [树莓派安装Mosquitto](https://blog.gtwang.org/iot/raspberry-pi/raspberry-pi-mosquitto-mqtt-broker-iot-integration/)

# 2. Raspberry Client
`sudo pip3 install paho-mqtt`
## 2.1. VS code 远程开发Python
使用ssh的remote interpreter

# 3. MAC OS Client

`sudo pip3 install paho-mqtt`
## 3.1. VS code 开发Python
注意，使用右键的：在终端运行。不要选成在python终端运行

# 4. ALI Cloud Broker
搜索一下，在Centos上按照mosquito，设计用户名和密码。
```
apt-get install mosquitto mosquitto-clients
service mosquitto status
```

## 4.1. Broker的开启
在CentOS下使用：`netstat -ntlp`。可以查看1883端口是否开启，来判断mosquito是否运行。