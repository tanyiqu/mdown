import sys
import R
import argparse
import util.TextUtil as TextUtil
import util.OSUtil as OSUtil
from downloader.M3u8Downloader import M3u8Downloader
from m3u8.M3u8 import M3u8
import threading
import time

parser = argparse.ArgumentParser(description=R.string.DESC)
parser.add_argument("url", nargs="*", help="url of m3u8 video, default argument, required")

parser.add_argument('-v', '--version', action='version', version=R.string.VERSION_NAME)

parser.add_argument('-u', '--url', metavar='', help='to specify m3u8 video URL')
parser.add_argument('-n', '--name', metavar='', help='name of file')
parser.add_argument('-t', '--thread', metavar='', type=int, help='threads of download progress', default=32)
parser.add_argument('-o', '--output', metavar='', help='output path of file')


# 检测传入的参数，返回字典形式的参数列表，如果有检测失败的则返回None
def analyseArgs(args):
    dit = {
        'url': args.url[0],
        'name': args.name,
        'thread': args.thread,
        'path': args.output
    }

    # 简单判断一下url
    if not TextUtil.isUrl(dit['url']):
        print('error: "%s" is not a correct URL' % dit['url'])
        print('please check the link for incorrect input')
        return None

    # 名字
    if dit['name'] is None:
        dit['name'] = 'index.ts'
        pass

    # 路径
    if dit['path'] is None:
        dit['path'] = OSUtil.getPath()
        pass
    elif not TextUtil.isPath(dit['path']):
        print('error: "%s" is not a correct path' % dit['path'])
        return None
        pass

    # 线程数
    if not 0 < dit['thread'] < 129:
        print('error: the number of threads must be greater than 0 and less than or equal to 128')
        return None

    return dit


def main():
    # 接收系统参数
    args = parser.parse_args()

    # 判断有没有传url
    if len(args.url) < 1:
        print('error: the following arguments are required: URL')
        return

    # 检测参数
    args = analyseArgs(args)
    if args is None:
        return

    # 开始
    print()
    print('downloading with mdown...')
    print('%s%-16s%s' % ('    ', 'Url:', args['url']))
    print('%s%-16s%s' % ('    ', 'Thread:', args['thread']))
    print('%s%-16s%s' % ('    ', 'Name:', args['name']))
    print('%s%-16s%s' % ('    ', 'Path:', args['path']))
    print()

    # 构造M3u8
    print('parsing m3u8...')
    m3u8 = M3u8(args['url'])
    if not m3u8.isM3u8():
        print()
        print('error: "%s" is not a correct URL' % args['url'])
        print('please check your URL through your browser')
        return
        pass
    print('parsing succeed')
    print()
    print('%s%-16s%s' % ('    ', 'Length:', m3u8.getTsLength()))
    print('%s%-16s%s' % ('    ', 'Duration:', m3u8.getDuration()))
    print()

    # 构造M3u8Downloader
    downloader = M3u8Downloader(m3u8.getList(), args['path'], args['name'], args['thread'], interval=0.2)
    print('downloading...')
    downloader.download()

    pass


if __name__ == '__main__':
    main()
    pass
