import sys
import R
import argparse

parser = argparse.ArgumentParser(description=R.string.DESC)
parser.add_argument("url", nargs="*", help="url of m3u8 video, default argument")

parser.add_argument('-v', '--version', action='version', version=R.string.VERSION_NAME)

parser.add_argument('-u', '--url', metavar='', help='to specify m3u8 video url')
parser.add_argument('-n', '--name', metavar='', help='name of file', default='')
parser.add_argument('-t', '--thread', metavar='', type=int, help='threads of download progress')

if __name__ == '__main__':
    # 接收系统参数
    args = parser.parse_args()
    print(args)
    pass
