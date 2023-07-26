# 基于Github的协作开发说明

**本次协作开发通过Github提供的协同开发完成**

## 步骤

- **在我们使用Github进行操作时，我们要确保在自己的分支内修改，一定要谨慎不得覆盖或者影响到其他分支或者主分支的内容（若修改了其他分支内容一定要事先告知）**
- 每一次在修改前，请切换到`main`分支执行指令`git pull`更新最新的主分支内容，然后再切换到个人分支，进行修改，`git commit`之后再执行`git rebase main`，确保分支挂在新的主分支版本上。

![](https://rockoss-1309912377.cos.ap-beijing.myqcloud.com/picgo/comiit.png?q-sign-algorithm=sha1&q-ak=AKIDqVTxW5OWTJyPemjcRMLAl7J1WoulZPDs&q-sign-time=1689161111;8999999999&q-key-time=1689161111;8999999999&q-header-list=host&q-url-param-list=&q-signature=fdd80a15d785766c4a791a45175a74ccd0cdf1f6)

- 此处我给每位成员都设置了管理权限，因此每位成员都可以自行审查或者审核他人的request，审核完毕没有错误即可合并分支到上游仓库。

此处附上参考文档链接：

[如何使用Github优雅地进行协同合作](https://blog.csdn.net/Jenny_WJN/article/details/104209062)

- **注**：项目开发日志我在前后端都已经给了对应的md文件，每位成员编写自己的技术报告的时候可以注明自己的个人身份标识（**不要透露姓名，学号等个人敏感信息**），例如昵称都可以，同时注明相关的开发日期和实践细节(尽可能详细，确保每一步操作都有迹可循)
- 为了保证项目开发的完整性和简便性，请各位组员一定要谨慎提交拉去请求和合并请求！！！在提交不同分支代码的过程中一定要慎重，切勿弄乱分支目录下的文件！！！
- 还有的后续再补充。。。。。。。。