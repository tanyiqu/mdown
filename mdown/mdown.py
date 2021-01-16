import R
import argparse
import util.TextUtil as TextUtil
import util.OSUtil as OSUtil
from downloader.M3u8Downloader import M3u8Downloader
from m3u8.M3u8 import M3u8
import parseArgs

from config.Configuration import Configuration


def main():
    # 处理命令行参数
    parseArgs.parseArgs()

    # 开始
    print()
    print('downloading with mdown...')
    print('%s%-16s%s' % ('    ', 'Url:', Configuration.url))
    print('%s%-16s%s' % ('    ', 'Thread:', Configuration.thread))
    print('%s%-16s%s' % ('    ', 'Name:', Configuration.name))
    print('%s%-16s%s' % ('    ', 'OutPath:', Configuration.outPath))
    print()

    # 构造M3u8
    print('parsing m3u8...')
    m3u8 = M3u8(url=Configuration.url, timeout=Configuration.timeout)
    if not m3u8.isM3u8():
        print()
        print('error: "%s" is not a correct URL' % Configuration.url)
        print('please check your URL through your browser')
        return
        pass
    print('parsing succeed')
    print()
    print('%s%-16s%s' % ('    ', 'Length:', m3u8.getTsLength()))
    print('%s%-16s%s' % ('    ', 'Duration:', m3u8.getDuration()))
    print()

    # 构造M3u8Downloader
    downloader = M3u8Downloader(tsList=m3u8.getList(),
                                path=Configuration.outPath,
                                filename=Configuration.name,
                                maxWorkers=Configuration.thread,
                                timeout=Configuration.timeout,
                                interval=0.2,
                                temp=Configuration.temp)

    # 下载视频
    print('downloading...')
    downloader.download()

    # 打印项目信息
    print()
    print('项目地址：https://github.com/tanyiqu/mdown，觉得好用就给个star吧！')

    pass


# 执行主函数
if __name__ == '__main__':
    main()
    pass
