"""
字符串处理工具类
"""


# 判断一个字符串是不是url
def isUrl(url: str):
    """
    判断一个字符串是不是url
    :param url: 字符串
    :return:
    """
    return url.startswith('http')
    pass


if __name__ == '__main__':
    print(isUrl('https://xxx'))
    print(isUrl(''))

    pass
