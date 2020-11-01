"""
字符串处理工具类
"""
from pathlib import Path


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
