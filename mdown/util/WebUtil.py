import requests


# 获取链接的文本内容，下载失败返回None
def getText(url: str, timeout: int = 5, retries: int = 3):
    """
    获取链接的文本内容，下载失败返回"null"
    :param url:     链接
    :param timeout: 每次请求的等待时长，默认5秒
    :param retries: 超时重试次数，不是总请求次数，总共请求次数为retries+1
    :return: 文本内容
    """
    # 检查参数
    if timeout < 1:
        timeout = 5
    if retries < 1:
        retries = 3
    print('getting resource...')
    i = 0
    while i <= retries:
        try:
            if i >= 1:
                print('retry getting resource...', i)
            text = requests.get(url, timeout=timeout).text
            print('getting resource finished.')
            return text
        except requests.exceptions.RequestException:
            i += 1
            pass
        pass
    return None
    pass


if __name__ == '__main__':
    txt = getText('https://meng.wuyou-zuida.com/20200227/26199_992e4909/index.m3u8')
    print(txt)
