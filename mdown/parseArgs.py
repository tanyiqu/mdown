"""
专门处理命令行参数
将命令行参数构造成Configuration对象
"""

import R
import argparse
from config.Configuration import Configuration
import util.TextUtil as TextUtil
import util.OSUtil as OSUtil


# 准备
def initParser(parser):
    # 必须参数
    parser.add_argument("url", nargs="?", help="下载视频的URL，必须在首位")

    # 版本信息
    parser.add_argument('-v', '--version', action='version', version=R.string.VERSION_NAME, help='显示程序的版本号')

    # 需要跟值的参数
    parser.add_argument('-n', '--name', metavar='', help='指定下载文件名称', default=None)
    parser.add_argument('-t', '--thread', metavar='', type=int, help='指定下载的线程数', default=32)
    parser.add_argument('-o', '--outpath', metavar='', help='输出路径', default=None)
    parser.add_argument('-s', '--slice', metavar='', type=int, help='指定要下载第几个视频片段', default=-1)
    parser.add_argument('--begin', metavar='', type=int, help='指定从第几个视频片段开始', default=0)
    parser.add_argument('--end', metavar='', type=int, help='指定从第几个视频片段结束', default=-1)
    parser.add_argument('--timeout', metavar='', type=int, help='指定请求资源时，超时几秒后重试，默认5s', default=5)

    # 不需要跟值的参数
    parser.add_argument('--temp', action='store_true', help='保留下载时的临时文件，默认不保留')
    pass


# 检验参数
def analyseArgs(args):
    """
    检测传入的参数，返回字典形式的参数列表，如果有检测失败的则返回None
    :param args: 参数
    :return: 无
    """
    if args.url is None:
        print('error: the following arguments are required: URL')
        return None

    Configuration.url = args.url
    Configuration.name = args.name
    Configuration.thread = args.thread
    Configuration.outPath = args.outpath
    Configuration.begin = args.begin
    Configuration.end = args.end
    Configuration.slice = args.slice
    Configuration.timeout = args.timeout
    Configuration.temp = args.temp

    # 简单判断一下url
    if not TextUtil.isUrl(Configuration.url):
        print('error: "%s" is not a correct URL' % Configuration.url)
        print('please check the link for incorrect input')
        return None

    # 名字
    if Configuration.name is None:
        Configuration.name = 'index.ts'
        pass

    # 路径
    if Configuration.outPath is None:
        Configuration.outPath = OSUtil.getPath()
        pass
    elif not TextUtil.isPath(Configuration.outPath):
        print('error: "%s" is not a correct path' % Configuration.outPath)
        return None
        pass

    # 线程数
    if not 0 < Configuration.thread < 256:
        print('error: the number of threads must be greater than 0 and less than or equal to 256')
        return None

    pass


# 处理
def parseArgs():
    """
    处理命令行参数
    :return: 无
    """
    # 创建parser
    parser = argparse.ArgumentParser(description=R.string.DESC)

    # 初始化parser
    initParser(parser)

    # 接收args
    args = parser.parse_args()

    # 分析处理args
    analyseArgs(args)

    pass
