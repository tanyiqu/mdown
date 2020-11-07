**1.为什么要自己编写《mdown》**
最近迷上了日剧，配合我之前写的[《看番神器Pro》](https://www.52pojie.cn/thread-1159920-1-1.html )确实拿到了资源，但是大多都是m3u8的链接。
在线解析又非常麻烦，所以我就自己写了mdown来下载m3u8的视频

**2.《mdown》有什么用**

mdown是用来高速（尽量，但也很快速）下载m3u8视频的工具

它使用python构建，下载速度由给定的线程数和你自己的网络带宽决定

**3.《mdown》的工作原理**

mdown解析传入的url链接，然后根据用户给定的线程数来分配下载任务

目前1.0.0为第一个版本，做稳定性测试

**4.从哪里获取《mdown》**

（1）从[开源项目](https://github.com/tanyiqu/mdown)里下载源码，然后自己打包

（2）从[github](https://github.com/tanyiqu/mdown/releases)下载打包好的exe程序

（3）从[网盘](https://tanyiqu.lanzoui.com/b0cqn2a3c)下载打包好的exe程序

**5.如何使用《mdown》**

添加环境变量，在控制台调用，参数为：

-u --url：指定url链接，默认为第一个参数（如有其他参数，则url一定要在第一个位置）

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8
```



-n --name：指定下载视频的名字，默认为index.ts

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8 -n 01.ts
```



-o --output：指定视频下载位置，默认为当前路径

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8 -o D:\video
```



-t --thread：指定下载视频使用多少线程数，默认线程数为16（如果你的计算机性能差不多的话，开64或128可以有很棒的下载体验）

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8 -t 128
```

**6.《mdown》怎么更新**

star我的[github项目](https://github.com/tanyiqu/mdown)，或者[关注他](https://space.bilibili.com/42337616)获取更新详情

**7.Bug & 不足**

- 如果已存在同名的文件/文件夹则不能正常下载
- 下载过后不能删除临时生成的文件夹
- 下载失败不能续传
- ...

**8.关于《mdown》的一些声明**

《mdown》只是为了大家提供一个m3u8视频下载的途径，请不要用于非法用途。

感谢大家的支持！