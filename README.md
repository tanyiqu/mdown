# mdown
Fast and simple m3u8 video downloader built with Python

## 版本

1.0.0 发布版

## 安装

### windows

下载打包的exe程序

[点击跳转下载](https://github.com/tanyiqu/mdown/releases)

### macos

暂无

### linux

暂无

## 使用

添加环境变量，在控制台调用

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



## 第三方库

requests

...