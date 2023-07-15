# 2023暑期网络安全攻防实践记录报告

## **负责工作**

- 制定分工计划
- 作为红队完成漏洞存在性验证和漏洞利用

- 作为蓝队对漏洞攻击行为进行持续检测和威胁识别，并进行修复

## 实践过程

### 环境搭建

> 万事开头难，只要肯攀登

**1.配置虚拟机，调节网络环境**

本次实践中，虚拟机配置两张网卡：`Host-only`网卡和`网络地址转换(NAT)`

<img src="img/virtualnetwork.png" alt="virtualnetwork" style="zoom:50%;" />

当然要完成红蓝攻防对抗，需要准备攻击者主机和靶机，直接使用多重加载镜像，能够有效简化整个实验过程：

<img src="img/windows.png" alt="windows" style="zoom: 67%;" />

同时为了使得挂载的两个虚拟机的ip地址不同，可以自行手动更新地址：
<img src="img/peizhi.png" alt="peizhi" style="zoom: 50%;" />

**2.从仓库中拉取到本机的虚拟机系统当中**：

在模拟红蓝网络攻防实践的整个过程之前，需要确保本地环境部署完毕，当然在黄药师录制好的[视频指导](https://www.bilibili.com/video/BV1p3411x7da/?p=22&spm_id_from=pageDriver&vd_source=61a1cf010feeebc60643481f16fc695e)下可以很快的部署完能够省略很多比较繁琐的操作：

```shell
git clone https://github.com/c4pr1c3/ctf-games.git
```

通过使用Docker Compose来构造docker环境，其中git下来的仓库老师已经配置好对应的.yml文件，直接执行即可构建对应的环境：

```shell
sudo apt update && sudo apt install -y docker.io docker-compose jq
```

构建好后，直接运行老师给出的bash脚本即可在本地的80端口开启容器：

<img src="img/container%20build.png" alt="container build" style="zoom:50%;" />

此处在运行`start.sh`脚本时，需要在root用户权限下执行，当然，也可以将当前用户添加到 docker 用户组，免 sudo 执行 docker 相关指令：

```shell
sudo usermod -a -G docker ${USER}
```

当然以上步骤都需要确保**网络能够正常进行访问**，如果访问或者拉取镜像时出现网络限制或者超时，可以更换docker镜像源和kali镜像源：

- **更换kali国内镜像源**：

  - 使用下列命令可以直接编辑`sources.list`

    ```css
    sudo vim /etc/apt/sources.list
    ```

  - 换源地址如下：

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

  - 保存成功后命令行输入 `sudo apt update`更新软件源

    ```shell
    sudo apt update
    ```

- **更换docker源：**

  - 创建或修改 /etc/docker/daemon.json 文件，修改：

    ```shell
    cd /etc/docker
    vim daemon.json
    ```

    加入如下配置：

    ```shell
    {
        "registry-mirrors" : [
        "https://registry.docker-cn.com",
        "http://hub-mirror.c.163.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://cr.console.aliyun.com",
        "https://mirror.ccs.tencentyun.com"
      ]
    }
    ```

    重启docker服务使配置生效：

    ```shell
    systemctl daemon-reload
    systemctl restart docker.service
    ```

    查看配置是否成功：

    ```shell
    docker info
    ```

    <img src="img/dockerpeizhi.png" alt="dockerpeizhi" style="zoom:50%;" />

**3.测试部署本地的Vulfocus**

进入部署好的地址，能够看到对应的镜像列表等信息：

<img src="img/vulfocus-platform.png" alt="vulfocus-platform" style="zoom:50%;" />

在镜像列表同步上游镜像，能够得到Vulfocus已经提供的镜像：

![cvetest](img/cvetest.png)

<img src="img/mirror%20list.png" alt="mirror list" style="zoom:50%;" />

尝试下载镜像，并在容器中启动环境进行一定测试：

![start image test](img/start%20image%20test.png)

**4.如何去自定义一个场景拓扑镜像**、

我们在搭建整个网络攻防的模拟环境的过程中，需要去构建跨网段渗透的场景镜像，而由于官网（[在线平台](https://vulfocus.cn/#/scene/list)）已经不再提供下载和资源镜像分享，因此需要自己去设计构建相应的拓扑场景和镜像：

![Download function off](img/Download%20function%20off.png)

我们直接手动设计场景，首先，要达成跨网段和识别，进入办公区和核心区的任务，简单模拟其环境供使用这一漏洞攻防环境，我们需要准备两张网卡实现二层网络的搭建：

![Gateway configuration](img/Gateway%20configuration.png)

攻击者主机通过暴露在“外网”的靶机漏洞从而渗透攻击DMZ区域，并将其作为跳板访问，依次利用漏洞访问到核心网内的靶机：
![Scene Topology](img/Scene%20Topology.png)

在容器中启动场景，查看相应的镜像信息：

![The scene started successfully](img/The%20scene%20started%20successfully.png)

完成上述步骤即构建了一个双层网段的渗透测试环境的模拟。

### 漏洞验证和利用

> 雄关漫道真如铁，而今迈步从头越。

#### CVE-2020-17530 Struts2

我们启动场景后，查看当前运行的镜像：

![dockerps](img/dockerps.png)

能够看到在Host-only网卡的本地地址的58841端口开启了`CVE-2020-17530 Struts2`的靶场环境，

![attackcore](img/attackcore.png)

切换到攻击者主机并执行：

```shell
# metasploit 基础配置
# 更新 metasploit
sudo apt install -y metasploit-framework
# 初始化 metasploit 本地工作数据库
sudo msfdb init
```

![datalab](img/datalab.png)

```shell
# 启动 msfconsole
msfconsole
# 确认已连接 pgsql
db_status
# 建立工作区
workspace -a demo
```

![metasploit](img/metasploit.png)







#### weblogic-cve-2019-2725







#### nginx-php-flag

















### 漏洞威胁监测和缓解修复

> 欲穷千里目，更上一层楼

#### 









