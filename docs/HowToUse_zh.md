# mdown使用说明

- [简体中文](https://gitee.com/Tanyiqu/mdown/blob/main/docs/HowToUse_zh.md)
- [English](https://gitee.com/Tanyiqu/mdown/blob/main/docs/HowToUse_en.md)
- [日本語](https://gitee.com/Tanyiqu/mdown/blob/main/docs/HowToUse_ja.md)

## 0x01 下载exe可执行文件

[点击进入下载](https://github.com/tanyiqu/mdown/releases)

## 0x02 配置环境变量并在终端调用

- 将下载的“mdown.exe“放进一个你认为合适的文件夹，如：**D:/softwate/mdown**（注意：D:/softwate/mdown 是文件夹全路径）

- 然后将 **D:/softwate/mdown** 这个目录添加进系统环境变量（不会添加系统环境变量可以网上搜一下）
- 之后在任意路径下打开终端 或 cmd 或 Windows Terminal 或 PowerShell...
- 输入命令即可下载视频

## 0x03 参数说明

1.0.0-release 版本的参数有

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



## 0x04 详细说明

假如你想下载的链接为 https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8

你在桌面打开了一个cmd

这时候你输入 ```mdown https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8``` 命令就可以将视频下载到桌面



如果你想下载更快速一点，你可以在后面追加 ```-t 128``` 来指定下载使用的线程为128，当然也可以更快，这取决于你的电脑性能和网络带宽



如果你想要给下载好的文件命名，你可以再追加 ```-n xxx.ts``` 来指定下载视频的名称



如果你想要下载到 D:/video 这个文件夹下，你可以再追加  ```-o D:/video``` 来指定下载的位置



以上需要追加的参数没有顺序限制，但是url链接一定要在第一位

