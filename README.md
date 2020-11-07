# mdown

Fast and simple m3u8 video downloader built with Python

[注：如果下面有图片加载不出来，点这个进行查阅文档](https://gitee.com/tanyiqu/mdown/blob/main/README.md)

## 版本

1.0.0 发布版

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

[具体使用说明点这里](https://gitee.com/Tanyiqu/mdown/blob/main/docs/HowToUse.md)

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



软件预览

![预览图加载不出来的话，点文档上面的链接跳转查阅](https://tanyiqu.gitee.io/mdown/res/preview.png)

## Bug & 不足

- 如果已存在同名的文件/文件夹则不能正常下载
- 下载过后不能删除临时生成的文件夹
- 下载失败不能续传
- ...

## 未来计划

- 实现中断继续下载
- ...

## 第三方库

requests

...

## 更新日志

1.0.0 release