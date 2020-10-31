import sys
import R
import argparse
import util.TextUrl as TextUrl
from util.DownloadUtil import M3u8Downloader
from m3u8.M3u8 import M3u8

parser = argparse.ArgumentParser(description=R.string.DESC)
parser.add_argument("url", nargs="*", help="url of m3u8 video, default argument, required")

parser.add_argument('-v', '--version', action='version', version=R.string.VERSION_NAME)

parser.add_argument('-u', '--url', metavar='', help='to specify m3u8 video url')
parser.add_argument('-n', '--name', metavar='', help='name of file', default='')
parser.add_argument('-t', '--thread', metavar='', type=int, help='threads of download progress')
parser.add_argument('-C', metavar='', help='download location')


def main():
    # 接收系统参数
    args = parser.parse_args()
    # 判断有没有传url
    if len(args.url) < 1:
        print('error: the following arguments are required: url')
        return

    url = args.url[0]

    # ------------------------
    # print(args)
    # print(url)
    # ------------------------

    # 简单判断一下url
    if not TextUrl.isUrl(url):
        print('error: "%s" is not a correct url' % url)
        return

    print()
    print('downloading with mdown...')
    print('url : ' + url)
    print()
    # 构造M3u8
    print('parsing m3u8...')
    m3u8 = M3u8(url)

    if not m3u8.isM3u8():
        print('error: "%s" is not a correct url' % url)
        pass

    print()
    print('parsing succeed')
    print('Length:\t\t%s' % m3u8.getTsLength())
    print('Duration:\t%s' % m3u8.getDuration())

    # 构造M3u8Downloader
    downloader = M3u8Downloader(m3u8.getList())
    downloader.download()

    pass


if __name__ == '__main__':
    main()
    pass
