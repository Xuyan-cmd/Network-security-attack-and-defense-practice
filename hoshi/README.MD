# 网络安全综合实验报告

## 实验目标

### 前置

- [x] 通过容器部署vulfocus平台搭建实验所需场景

### As Team Red

- 漏洞存在性验证

  - [x] struts2 代码执行 （CVE-2020-17530）

  - [x] weblogic 远程代码执行 (CVE-2019-2725)

  - [x] 不知名的Nginx命令执行漏洞

- 漏洞利用

  - [x] struts2 代码执行 （CVE-2020-17530）

  - [x] weblogic 远程代码执行 (CVE-2019-2725)

  - [x] 不知名的Nginx命令执行漏洞

### As Team Blue

## 实验环境

### 环境List

- 宿主机：Windows 11 23H2 22631.2050

- 虚拟机平台

  - Oracle VirtualBox 7.0.8 r156879 as "Attacker"

    - Kali GNU/Linux Rolling x86_64

      - Kernel：6.3.0-kali-amd64

  - WSL 1.3.14.0 as "Victim"

    - Kali GNU/Linux Rolling on Windows 10 x86_64

      - Kernel：5.15.90.3-microsoft-standard-WSL2

### 环境描述

因为存在攻防的背景设定，本次实验使用到了2台虚拟机，分别是作为被攻击主机的WSL平台Victim主机和作为攻击者主机是VirtualBox平台Attacker主机，其中Victim主机用于运行vulfocus平台的场景容器并负责攻击流量抓取，Attacker主机用于渗透攻入

## 试验记录

### 环境搭建

>由于实验是线上进行，无论红方还是蓝方都需要进行自己作为成员的环境搭建，这里记录个人的搭建过程

已经具备的条件是VirtualBox和WSL两个平台都有安装好的Kali Linux，前者是之前CTF用过的系统，后者是网络安全课程就有使用的Linux子系统，按照课程视频的模式，其实应该是两台VirtualBox虚拟机之间进行操作，这次选择创造一点多样性和不确定性，在一半VirtualBox一半WSL上进行环境搭建

最开始计划将VirtualBox的虚拟机Kali作为Victim主机，但是由于想要遵循课程视频中描述的好的工作习惯，在Attacker主机使用Metasploit时通过msfdb记录操作，但是WSL这边由于其他原因没有设置为通过systemd引导启动（chroot性质），基于systemctl的postgresql初始化操作自然会出现需要折腾的情况（用不同于systemd的方式启动数据库服务或者将WSL通过systemd作为PID 1完整启动），于是果断将WSL作为Victim主机，因为有预先配置过手动启动dockerd，单纯通过容器搭建vulfocus平台和抓包流量的话并不需要折腾

vulfocus平台的搭建直接使用了[ctf-games](https://github.com/c4pr1c3/ctf-games/tree/master/fofapro/vulfocus)中打包好的shell脚本，git clone的部分就不需要特别演示了，唯一的操作是用`chmod +x /fofapro/vulfocus/start.sh`给脚本添加了可执行权限，然后执行，剩下的就是等待docker拉取镜像

唯一可以说一下的点是，课程视频包括课件中描述的将docker换USTC源的操作应该被标记为**outdated**，以下是官网的描述：

>由于访问原始站点的网络带宽等条件的限制，导致 Docker Hub, Google Container Registry (gcr.io) 与 Quay Container Registry (quay.io) 的镜像缓存处于基本不可用的状态，因此科大镜像站的各容器镜像服务仅限校内使用。  
>对于从科大校外的访问：
>
>- Docker Hub 和 Google Container Registry 会返回 403；  
>
>- Quay 会被 302 重定向至源站。

作为颇为出名的开源镜像站，且不论格局问题，也许可能确实是被薅疼了，于是新的🐏的选择就出现了，那就是NJU的镜像😂

只需要进行一点点修改：

```bash
# 使用南京大学 Docker Hub 镜像源
cat <<EOF > /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.nju.edu.cn/"]
}
EOF
```

当然官方也有文档，详细内容可以看[这里](https://doc.nju.edu.cn/books/35f4a/page/docker-hub)

### 红方操作

假设要真实一点考虑攻防的话，其实整个红方操作部分在漏洞存在性检测这一环节都没有做很好，正确的思路应该是通过某种与服务的交互获取到信息，在确认POC可行之后再执行exploit，否则就是在白送0day🤔

而在接下来的内容当中，将记录最“不敬业”的红方操作😂

即

>“成功利用=漏洞存在”

的逻辑，无奈我们这是白盒渗透就是了，已然做好了挨骂的准备(。﹏。)

#### 外层

从模拟显示的角度来考虑，最外层的主机负责对外提供服务，于是直接得到了提供服务的端口号，也就是vulfocus平台上场景的入口端口

操作上，通过Metasploit工具的平台搜索struts2或者不演了直接搜索CVE-2020-17530，如果是前者的话需要进行一点肉眼筛选，这次的漏洞编号说明是2020年的漏洞，于是可用的exploit只有2020年9月14日的：

```metasploit
msf6 > search struts2

Matching Modules
================

   #  Name                                             Disclosure Date  Rank       Check  Description
   -  ----                                             ---------------  ----       -----  -----------
   0  exploit/multi/http/struts_dev_mode               2012-01-06       excellent  Yes    Apache Struts 2 Developer Mode OGNL Execution
   1  exploit/multi/http/struts2_multi_eval_ognl       2020-09-14       excellent  Yes    Apache Struts 2 Forced Multi OGNL Evaluation
   2  exploit/multi/http/struts2_namespace_ognl        2018-08-22       excellent  Yes    Apache Struts 2 Namespace Redirect OGNL Injection
   3  exploit/multi/http/struts2_rest_xstream          2017-09-05       excellent  Yes    Apache Struts 2 REST Plugin XStream RCE
   4  exploit/multi/http/struts2_code_exec_showcase    2017-07-07       excellent  Yes    Apache Struts 2 Struts 1 Plugin Showcase OGNL Code Execution
   5  exploit/multi/http/struts_code_exec_classloader  2014-03-06       manual     No     Apache Struts ClassLoader Manipulation Remote Code Execution
   6  exploit/multi/http/struts2_content_type_ognl     2017-03-07       excellent  Yes    Apache Struts Jakarta Multipart Parser OGNL Injection
   7  exploit/multi/http/struts_code_exec_parameters   2011-10-01       excellent  Yes    Apache Struts ParametersInterceptor Remote Code Execution


Interact with a module by name or index. For example info 7, use 7 or use exploit/multi/http/struts_code_exec_parameters
msf6 > search cve-2020-17530

Matching Modules
================

   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/multi/http/struts2_multi_eval_ognl  2020-09-14       excellent  Yes    Apache Struts 2 Forced Multi OGNL Evaluation


Interact with a module by name or index. For example info 0, use 0 or use exploit/multi/http/struts2_multi_eval_ognl

msf6 >
```

之后就是选用exploit，然后添加payload，这里选择和课件中一样的`cmd/unix/reverse_bash`，随后是options的设置阶段，设置rhosts为Victim主机的eth0网卡地址，rport则为平台上随机的端口，同时将payload中的lhost设置为Attacker主机的Host-Only网卡，之后就剩下输入run或者exploit执行了，不添加`-j`无非是将exploit过程放在前台进行，也确实没有太着急到需要在exploit的一点时间中再见缝插针做点什么操作

随后只需要等待exploit运行完成，payload中的反弹bash会自动开启，接下来就是`ls /tmp`查看flag了（早期摸索过程截图，比较啰嗦）：

![screenShot](./img/2023-07-15-224012.png)

#### 中层

#### 内层

### 蓝方操作

## 问题记录

### 解决的问题

#### vulfocus平台不再支持个人搭建的平台访问场景商店

最早是rock发现了这一问题，为了确认不是个人原因，我也快速进行了vulfocus平台的搭建，发现确实应该是平台官方不再开放场景商店给个人搭建平台的感觉，考虑到服务器成本或者攻击保护等等原因也是可以接受

rock那边甚至找到了vulfocus的在线平台，发现虽然可以在官方的在线平台上打开场景商店，场景却不开放打包下载的功能，rock愤然留言要求开放场景下载，甚至还加了开发者的微信群想要讨个说法😂最后也是没什么下文

于是我这边和rock尝试了手搓这个思路，课程视频中正好对整个DMZ环境的场景有讲解，于是就试着从创建网卡开始摸索，到参照镜像选择搭建了手搓的DMZ场景出来，并且“似乎”也没有遇到太多问题，就这么继续顺着手搓的DMZ场景做下去了（伏笔）

![screenShot](./img/2023-07-12-175824.png)

最后也是rock在讨论区发布了[唯一的一篇帖子](http://courses.cuc.edu.cn/course/109860/forum?show_sidebar=false#/topics/457749)（链接可能需要访问权限），我则是对其中“因为尝试而误对外开放了全部主机”的问题进行了修正，即要模拟仅最外层主机作为入口，内网主机对外“隐身”

#### 薛定谔的容器？

且说上一部分讨论手搓DMZ场景这件事，虽然说抄了个大概，不知道为什么我这边最内层的Nginx命令执行漏洞的容器会出现报错退出的情况，分析下来感觉像是vulfocus平台设计的网卡之间网段分配的问题？截图来看是下面的效果：

![screenShot](./img/2023-07-18-181813.png)

为了排这部分错，我甚至尝试了清除所有容器、镜像、网卡等：

```bash
docker system prune -a
```

然后是重新下载vulfocus平台的镜像，环境中用到的包含漏洞的镜像也尽数重新下载，然而并没有解决问题，没有变的是网段分配还是存在问题，即地址并没有按照在平台中定义的虚拟网卡那样分配网段

直到又隔了一阵子，开始肝报告了，尝试复现这部分内容，一切又正常了，之前运行就会退出的Nginx命令执行漏洞容器这次也正常运行了：

```bash
┌──(leaf㉿ZephyrusG15)-[~/Downloads/ctf-games/fofapro/vulfocus]
└─$ dk ps -a
CONTAINER ID   IMAGE                                    COMMAND                  CREATED         STATUS
   PORTS                                         NAMES
1f9e1717645c   vulfocus/struts2-cve_2020_17530:latest   "/usr/local/bin/mvn-…"   8 minutes ago   Up 8 minutes
   0.0.0.0:63469->8080/tcp, :::63469->8080/tcp   8f439cea-c7ac-4e71-a8b3-e4f96d9c2654_jslmf51ua1c_1
3384d7e6a302   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       8 minutes ago   Up 8 minutes
   5556/tcp, 7001/tcp                            8f439cea-c7ac-4e71-a8b3-e4f96d9c2654_12zwznv9dp68_1
a11c919b9c58   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       8 minutes ago   Up 8 minutes
   5556/tcp, 7001/tcp                            8f439cea-c7ac-4e71-a8b3-e4f96d9c2654_3ysq230jk8w0_1
61c7669ba129   vulshare/nginx-php-flag:latest           "/2.sh"                  8 minutes ago   Up 8 minutes
   80/tcp                                        8f439cea-c7ac-4e71-a8b3-e4f96d9c2654_5bmsr0nf7b00_1
996a93042bb9   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       8 minutes ago   Up 8 minutes
   5556/tcp, 7001/tcp                            8f439cea-c7ac-4e71-a8b3-e4f96d9c2654_3z99kgcz8km0_1
f1ea333cc299   vulfocus/vulfocus:latest                 "sh /vulfocus-api/ru…"   3 hours ago     Up 3 hours (healthy)      0.0.0.0:80->80/tcp, :::80->80/tcp             vulfocus_vul-focus_1
25a25352d04e   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       7 days ago      Exited (137) 6 days ago                                                 9c3103b1-30f6-4b88-ac91-f35e2c3ca060_12zwznv9dp68_1
70ce52c49a2b   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       7 days ago      Exited (137) 6 days ago                                                 9c3103b1-30f6-4b88-ac91-f35e2c3ca060_3z99kgcz8km0_1
0c67ad8c14fa   vulfocus/struts2-cve_2020_17530:latest   "/usr/local/bin/mvn-…"   7 days ago      Exited (143) 6 days ago                                                 9c3103b1-30f6-4b88-ac91-f35e2c3ca060_jslmf51ua1c_1
9b451976a7c3   vulshare/nginx-php-flag:latest           "/2.sh"                  7 days ago      Exited (1) 7 days ago                                                   9c3103b1-30f6-4b88-ac91-f35e2c3ca060_5bmsr0nf7b00_1
68b81f757d9c   vulfocus/weblogic-cve_2019_2725:latest   "startWebLogic.sh"       7 days ago      Exited (137) 6 days ago                                                 9c3103b1-30f6-4b88-ac91-f35e2c3ca060_3ysq230jk8w0_1

┌──(leaf㉿ZephyrusG15)-[~/Downloads/ctf-games/fofapro/vulfocus]
└─$
```

也导致写了一半的报告需要扔下再回过头去完成最后一台机器的flag提交😔

（小声：这部分原本是放在“未解决的问题”下的，事出突然甚至打乱了我的报告格式😡）

### 神秘的日记

[这是什么？](./diary.md)

## 参考链接
