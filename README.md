<<<<<<< HEAD
<div align="center">
<img src="https://rockoss-1309912377.cos.ap-beijing.myqcloud.com/picgo/logo1.png?q-sign-algorithm=sha1&q-ak=AKIDqVTxW5OWTJyPemjcRMLAl7J1WoulZPDs&q-sign-time=1689064042;9000000000&q-key-time=1689064042;9000000000&q-header-list=host&q-url-param-list=&q-signature=aad9fa8c543509e08d98b24f6f5ef5b2a158f79e" >
<h1 align="center">
    CUC网络安全攻防实践（Network-security-attack-and-defense-practice）
    <h4>
        2023年CUC网络安全攻防实践仓库
    </h4>
</h1>
</div>

## 📜仓库说明

本仓库基于[基础团队实践训练](https://c4pr1c3.github.io/cuc-wiki/cp/2023/index.html#_12)跟练复现完成的 [网络安全(2021) 综合实验](https://www.bilibili.com/video/BV1p3411x7da/) 。其中以红蓝队角色完成相应的网络攻防场景在线，其中主要是基于Vulfocus平台提供的靶场环境进行实验

以下按本次实践训练所涉及到的人员能力集合划分了以下团队角色。一人至少承担一种团队角色。

- 红队：需完成漏洞存在性验证和漏洞利用。

- 蓝队威胁监测：漏洞利用的持续检测和威胁识别与报告。

- 蓝队威胁处置：漏洞利用的缓解和漏洞修复（源代码级别和二进制级别两种）。

上述能力的基本评分原则参考“道术器”原则：最基础要求是能够跟练并复现 [网络安全(2021) 综合实验](https://www.bilibili.com/video/BV1p3411x7da/) 中演示实验使用到的工具；进阶标准是能够使用课程视频中 **未使用** 的工具或使用编程自动化、甚至是智能化的方式完成漏洞攻击或漏洞利用行为识别与处置。

## 📝实践达成指标

- [ ] 完成基础环境配置
- [ ] 红队实现对环境漏洞的挖掘，并利用漏洞实现攻击
- [ ] 蓝队对模拟场景下的出现的攻击进行检测和识别处理
- [ ] 蓝队完成对漏洞的缓解或修复
- [ ] 实现自动化脚本编写和检测工具

## 📒项目日志

👨‍💻：[记录日志](https://www.baichuanweb.cn/article/example-68)
=======
# **2023暑期网络安全攻防实践记录报告**

## **负责工作**

- 制定分工计划
- 作为红队完成漏洞存在性验证和漏洞利用

- 作为蓝队对漏洞攻击行为进行持续检测和威胁识别，并进行修复

## 实践过程

### 环境搭建

> **万事开头难，只要肯攀登**

在模拟红蓝网络攻防实践的整个过程之前，需要确保本地环境部署完毕，当然在黄药师录制好的[视频指导](https://www.bilibili.com/video/BV1p3411x7da/?p=22&spm_id_from=pageDriver&vd_source=61a1cf010feeebc60643481f16fc695e)下可以很快的部署完能够省略很多比较繁琐的操作：

**1.从仓库中拉取到本机的虚拟机系统当中**：

```shell
git clone https://github.com/c4pr1c3/ctf-games.git
```

通过使用Docker Compose来构造docker环境，其中git下来的仓库老师已经配置好对应的.yml文件，直接执行即可构建对应的环境：

```shell
sudo apt update && sudo apt install -y docker.io docker-compose jq
```

构建好后，直接运行老师给出的bash脚本即可在本地的80端口开启容器：

![container build](img/container%20build.png)

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

    ![dockerpeizhi](img/dockerpeizhi.png)

**2.测试部署本地的Vulfocus**

进入部署好的地址，能够看到对应的镜像列表等信息：

![vulfocus-platform](img/vulfocus-platform.png)

在镜像列表同步上游镜像，能够得到Vulfocus已经提供的镜像：

![mirror list](img/mirror%20list.png)

尝试下载镜像，并在容器中启动环境进行一定测试：

>>>>>>> 4cb2a77 (7.11 攥写实验报告)
