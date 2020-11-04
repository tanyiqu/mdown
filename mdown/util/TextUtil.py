"""
字符串处理工具类
"""
from pathlib import Path


# 秒数转 hh:mm:ss 格式
def formatTime(sec: int):
    d = sec
    # 计算秒数
    s = d % 60
    # 持续时长 - 秒数
    d -= s
    # 计算分钟数
    minute = d / 60
    # 计算小时数
    h = minute / 60
    # 计算小于60的分钟数
    minute %= 60
    return "%02d:%02d:%02d" % (h, minute, s)
    pass


# 判断一个字符串是不是url
def isUrl(url: str):
    """
    判断一个字符串是不是url
    :param url: 字符串
    :return:
    """
    return url.startswith('http')
    pass


# 判断给定路径的目录是否存在
def isPath(path: str):
    my_file = Path(path)
    return my_file.is_dir()


if __name__ == '__main__':
    print(isUrl('https://xxx'))
    print(isUrl(''))

    pass
