"""
字符串处理工具类
"""
from pathlib import Path


# 秒数 转 hh:mm:ss 格式
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


# 字节数 转 网速
def byte2Speed(byte: int):
    """
    固定长度 12个字符的长度，不足的前补空格
    B   [   1023B/s]
    KB  [  1023KB/s]
    MB  [  5.60KB/s]
    """
    speed = byte
    # 小于1024Byte，网速单位为Byte/s
    if speed < 1024:
        speed = frontSpace(str(speed) + 'Byte/s')
        return speed
        pass

    # 以KB/s做单位
    speed /= 1024
    if speed < 1024:
        speed = frontSpace('%.2lfKB/s' % speed)
        pass
        return speed

    # 以MB/s做单位
    speed /= 1024
    speed = frontSpace('%.2lfMB/s' % speed)
    return speed
    pass


# 在string开头补齐空格，总长度补满num，默认12
def frontSpace(string: str, num: int = 10):
    while len(string) < num:
        string = ' ' + string
        pass
    return string
    pass


# 建议判断一个字符串是不是url
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
