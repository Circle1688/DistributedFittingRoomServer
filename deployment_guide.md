# 部署指南

## 安装依赖

- Python 3.12
- Cuda
- Cudnn
- TensorRT
- Topaz Video AI
- SyncTrayzor



## 同步目录

1. 打开主机的SyncTrayzor
2. 添加远程设备
3. 编辑FittingRoom的共享 共享到新机器
4. 新机器接受邀请



## 添加开机启动项

1. win+R 输入 shell:startup 打开开机启动目录
2. 将"D:\FittingRoom\DistributedSystemManager\run_node.bat.lnk"复制到开机启动目录



## 配置UE style3d账号

1. 打开"D:\FittingRoom\FittingRoomUE\FittingRoom\Saved\account.json"
2. 输入style3d账号 一台机器一个



## 添加节点

1. 打开cmd，输入ipconfig，查看IPv4地址
2. 打开主机的run_manager.bat
3. 点击add node，添加子机器ip地址



## 运行系统

1. 运行子机器的run_node.bat
2. 管理程序 run server 按钮
3. 点击start all nodes按钮
4. 等待facefusion预热结束









