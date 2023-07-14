## 小学期攻防学习记录

视频配套课件地址:[网络安全 (c4pr1c3.github.io)](https://c4pr1c3.github.io/cuc-ns-ppt/vuls-awd.md.v4.html#/漏洞原理详解)

### 7.10

网络安全综合实验：开源信息系统搭建、加固与漏洞攻防

- 内容提纲

  - 基础运行环境准备
  - 漏洞攻防环境现状
  - 漏洞攻防环境搭建
  - 漏洞攻击
  - 漏洞利用检测
  - 漏洞利用防御与加固

- 基础虚拟机环境搭建必知必会

  - 安装后虚拟机网卡没有分配到IP?

    - 修改配置文件：![image-20230710173343531](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230710173343531.png)

    - ![image-20230710173436296](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230710173436296.png)

    - ```
      再
      sudo ifdown eth0 && sudo ifup eth0
      sudo ifdown eth1 && sudo ifup eth1
      ```

  - SSH服务启用与SSH免密登录

    - ![image-20230710173916276](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230710173916276.png)
    - [可选]vscode remote on win10

  - 克隆出来的虚拟机IP地址—样?

  - **多重加载镜像**制作与使用

  - 备份与还原

    - 虚拟机快照与还原
    - 默认配置文件编辑前备份

- 网络：

  - Host-only
  - 希望用终端，不用图形界面
  - 网卡1：NAT
  - 网卡2：![image-20230710172921152](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230710172921152.png)

#### [本课程第 7 章课件中推荐过的训练学习资源](https://c4pr1c3.github.io/cuc-ns-ppt/chap0x07.md)

- https://github.com/c4pr1c3/ctf-games 获得本课程定制的 Web 漏洞攻防训练环境※
- [upload-labs 一个使用 PHP 语言编写的，专门收集渗透测试和 CTF 中遇到的各种上传漏洞的靶场](https://github.com/c0ny1/upload-labs)
- [PHP XXE 漏洞与利用源代码分析示例](https://github.com/vulnspy/phpaudit-XXE)
- [vulhub 提供的 XXE 漏洞学习训练环境](https://github.com/vulhub/vulhub/tree/master/php/php_xxe)
- [python-xxe](https://github.com/c4pr1c3/python-xxe)
- [sqli-labs](https://github.com/c4pr1c3/sqli-labs) | [sqli-labs 国内 gitee 镜像](https://gitee.com/c4pr1c3/sqli-labs)
- [一个包含php,java,python,C#等各种语言版本的XXE漏洞Demo](https://github.com/c0ny1/xxe-lab)
- [upload-labs 一个使用 PHP 语言编写的，专门收集渗透测试和 CTF 中遇到的各种上传漏洞的靶场](https://github.com/c0ny1/upload-labs)

#### [vulhub](https://github.com/topics/vulhub)

- [vulhub/vulhub](https://github.com/vulhub/vulhub)
- [fofapro/vulfocus](https://github.com/fofapro/vulfocus)
- [sqlsec/ssrf-vuls](https://github.com/sqlsec/ssrf-vuls)

#### 快速上手 vulfocus

[c4pr1c3/ctf-games - fofapro/vulfocus](https://github.com/c4pr1c3/ctf-games/tree/master/fofapro/vulfocus)

![image-20230710193006713](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230710193006713.png)

## 7.11

#### 从单个漏洞靶标开始

> 一切来自于 **用户输入** 的数据都是不可信的。

1. 找到靶标的【访问入口】
2. 收集【威胁暴露面】信息
3. 检测漏洞存在性
4. 验证漏洞可利用性
5. 评估漏洞利用效果

进入容器：![image-20230711102419958](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230711102419958.png)

![image-20230711102510727](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230711102510727.png)

容器拷贝：![image-20230711102547023](C:\Users\17124\AppData\Roaming\Typora\typora-user-images\image-20230711102547023.png)

对jar包反编译

6.3.4有DNSlog使用指南

## 7.13

学习一点漏洞防护技术原理与应用：

 [(100条消息) 信息安全-网络安全漏洞防护技术原理与应用_虚拟补丁_learning-striving的博客-CSDN博客](https://blog.csdn.net/qq_43874317/article/details/126689320)
