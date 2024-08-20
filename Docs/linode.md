# Linode 资源平台可视化

可基于Linode平台上的各个资源情况，可进行统一界面展示、亦可根据自身关注项做针对性的监控告警。

展示项包含Linode服务器实例数、Linode服务器Region分布情况、NodeBalancers个数、流量总量及使用情况、每小时成本(估算)等数据可视化展示。

主要Metric信息如下：

![image-20240820154613956](C:\Users\zhin\AppData\Roaming\Typora\typora-user-images\image-20240820154613956.png)



## 1. 环境准备

运行这套Linode资源可视化展示所需环境，主要通过将Prometheus作为数据源添加到Grafana中进行可视化展示。

### 1.1 所需工具

2个工具自行安装：

+ Prometheus 
+ grafana

### 1.2 **Python 环境**

- 确保你已经安装了 Python 3.x。

### 1.3 **依赖项安装**

- 需要安装以下 Python 库：
  - `requests`: 用于发送 HTTP 请求。
  - `prometheus_client`: 用于暴露 Prometheus 指标。

你可以通过以下命令安装这些库：

```shell
$ pip install requests prometheus-client
```

### 1.4 代码仓库地址

### 1.5  API Tokens

Linode云平台生成一份 Personal Access Tokens：

![image-20240820154920132](C:\Users\zhin\AppData\Roaming\Typora\typora-user-images\image-20240820154920132.png)

生成结果类似：

```shell
06c5ed628d863c24ce39e292280dbbc6a6a098a63579cbc71c3157bc14d1f832
```



## 2. 代码运行

### 2.1 克隆仓库

### 2.2 代码配置

把生成的API Tokens填入到linode_token处，如：

```shell
$ cp config.py.template config.py
$ xx@xx:~/linode-resource-tracking$ cat config.py
# Personal Access Token
linode_token = '06c5ed628d863c24ce39e292280dbbc6a6a098a63579cbc71c3157bc14d1f832'

# Refresh Invertal, seconds
interval = 30
pagesize = 200


#  Exporter Port      
hostPort = 9001
hostAddr = "0.0.0.0"
```

+ 确保在你的机器上没有其他服务占用 `hostPort` 端口。

### 2.3 Prometheus 配置

- 如果你要将这些指标导入 Prometheus，请在你的 Prometheus 配置文件中添加一个 scrape job：

```shell
scrape_configs:
  - job_name: 'linode_exporter'
    static_configs:
      - targets: ['<hostAddr>:<hostPort>']
```

例如：

```shell
  - job_name: "linode-monitor"
    static_configs:
      - targets: ["localhost:9001"]
```

### 2.4 代码运行

准备好这些环境后，成功运行脚本并导出 Linode 的相关指标给 Prometheus。

```shell
$ python3 linode.py
```

 在 Linux 系统中，您可以使用以下方法来让脚本在后台运行：

+ 使用 `nohup` 命令

```shell
$ nohup  python3  linode.py &
```

+ 使用 `systemd` 服务

```shell
$ sudo vim  /etc/systemd/system/linode.service
[Unit]
Description=Linode monitor

[Service]
ExecStart=/usr/bin/python3 /path/to/linode-resource-tracking/linode.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动并启用服务：

```shell
$ sudo systemctl start linode.service
$ sudo systemctl enable linode.service
```



## 3. 图表展示

进入Grafana进行图表设置

![image-20240820154142302](C:\Users\zhin\AppData\Roaming\Typora\typora-user-images\image-20240820154142302.png)