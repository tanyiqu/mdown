"""
文件下载模块
"""

import requests
import time


class M3u8Downloader:
    __list = []

    def __init__(self, __list: list):
        self.__list = __list
        pass

    def download(self):
        print('下载 + %s' % len(self.__list))
        pass

    pass


class Downloader:
    """
    下载小文件的 工具类
    """
    __filename = ''
    __url = ''
    __path = ''

    # 构造
    def __init__(self, __url: str, __path: str, __filename: str):
        self.__url = __url
        self.__path = __path
        self.__filename = __filename
        pass

    def download(self):
        duration = time.time()
        resp = requests.get(self.__url)
        duration = time.time() - duration

        with open(self.__path + '/' + self.__filename, "wb") as code:
            code.write(resp.content)
            pass
        length = int(resp.headers['Content-Length']) / (1024 ** 2)
        speed = length / duration
        return {
            'length': length,
            'duration': duration,
            'speed': speed
        }
        pass

    pass


if __name__ == '__main__':
    d = Download('https://yuledy.helanzuida.com/20200402/1745_5f787176/1000k/hls/964e77c2ad0000033.ts',
                 # d = Download('https://mirrors.tuna.tsinghua.edu.cn/qt/archive/qt/5.12/5.12.8/qt-opensource-linux-x64-5.12.8.run',
                 'C:/Users/Tanyiqu/Desktop/测试打包',
                 '4555.ts')
    print(d.download())
    pass
