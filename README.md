# mdown

Fast and simple m3u8 video downloader built with Python

[注：如果下面有图片加载不出来，点这个进行查阅文档](https://gitee.com/tanyiqu/mdown/blob/main/README.md)

## 当前版本

1.1.0-release

## 安装

### windows

下载打包的exe程序

[点击进入下载](https://github.com/tanyiqu/mdown/releases)

### macos

暂无

### linux

暂无

## 使用

添加环境变量，在控制台调用

[具体使用说明点这里](https://gitee.com/Tanyiqu/mdown/blob/main/docs/HowToUse_zh.md)

### 参数

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



--timeout：指定获取资源无响应时，等待几秒重试，默认（不加时这个参数）为5s

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8 --timeout 10
```



--temp：添加这个参数，指定下载后保留临时文件，默认（不加时这个参数）不保留临时文件

```shell
mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8 --temp
```



软件预览

[![预览图加载不出来的话，点文档上面的链接跳转查阅](https://s1.ax1x.com/2020/11/05/BW1SgO.png)](https://imgchr.com/i/BW1SgO)

## 更新日志

- 下载后可以选择是否删除临时生成的文件夹
- 添加--timeout参数，指定无形应是几秒后重试
- 修复win7进度条显示问题
- ...

## Bug & 不足

- 下载失败不能续传
- ...

## 未来计划

- 实现中断继续下载
- ...

## 第三方库

requests

...

## 更新日志

1.1.0-release

1.0.0-release