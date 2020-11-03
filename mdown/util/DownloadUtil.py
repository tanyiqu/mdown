"""
文件下载模块
"""

import requests
import time
import os
import threading
import threadpool


# class M3u8Downloader:
#     pass


class TsDownloader:
    """
    下载ts文件的下载器
    """

    path = 'path'
    __path = '__path'

    def __init__(self):
        pass

    def print(self):
        print(self.path)
        print(self.__path)
        print(TsDownloader.path)
        print(TsDownloader.__path)
        pass

    def set(self):
        self.path = 'p'
        self.__path = '__p'
        pass

    # def __init__(self, url, path, name):
    #     # self.__url = url
    #     # self.__path = path
    #     # self.__name = name
    #     pass

    pass


if __name__ == '__main__':
    ts = TsDownloader()
    ts.print()
    ts.set()
    ts.print()

    pass


class M3u8Downloader:
    __list = []
    __filename = ''
    __path = ''
    __tmpPath = ''
    __length = 0
    __downloader = None
    __workers = 0
    __flag = []

    def __init__(self, __list: list, __path: str, __filename: str, __workers: int):
        self.__list = __list
        self.__path = __path
        self.__filename = __filename
        self.__workers = __workers
        self.__length = len(self.__list)
        pass

    def download(self):
        print('path: [%s] name: [%s]' % (self.__filename, self.__path))
        # 在路径里创建临时文件夹
        self.__tmpPath = self.__path + '\\.' + self.__filename
        os.mkdir(self.__tmpPath)

        def _download(dit):
            """
            dit:{
                index
                name
                duration
                url
            }
            """
            downloader = Downloader(dit['url'], self.__tmpPath, dit['name'], dit['index'])
            downloader.download()
            pass

        # 线程池
        pool = threadpool.ThreadPool(self.__workers)
        reqs = threadpool.makeRequests(_download, self.__list)
        for req in reqs:
            pool.putRequest(req)
            pass
        pool.wait()

        pass

    pass


class Downloader:
    """
    下载ts文件的 工具类
    """
    __filename = ''
    __url = ''
    __path = ''
    __num = 0

    # 构造
    def __init__(self, __url: str, __path: str, __filename: str, __num: int):
        self.__url = __url
        self.__path = __path
        self.__filename = __filename
        self.__num = __num
        pass

    def download(self):
        # 边写边下方式
        # duration = time.time()
        # resp = requests.get(self.__url, stream=True)
        # duration = time.time() - duration
        #
        # with open(self.__path + '/' + self.__filename, "wb") as f:
        #     for data in resp.iter_content(1024):
        #         f.write(data)
        #     pass

        # 下完再写方式
        # resp = requests.get(self.__url)
        # with open(self.__path + '/' + self.__filename, "wb") as f:
        #     f.write(resp.content)
        #     pass
        # #
        # print('%s is ok' % self.__num)
        #
        i = 0
        # 如果请求失败就重新请求，直至请求成功
        while True:
            try:
                resp = requests.get(url=self.__url, timeout=5)
                with open(self.__path + '/' + self.__filename, "wb") as f:
                    f.write(resp.content)
                    pass
                print('%s is ok' % self.__num)
                break
                pass
            except requests.exceptions.RequestException:
                i += 1
                print('%s retry %d' % (self.__num, i))
                pass
            pass
        pass

    pass

# if __name__ == '__main__':
#     d = Download('https://yuledy.helanzuida.com/20200402/1745_5f787176/1000k/hls/964e77c2ad0000033.ts',
#                  # d = Download('https://mirrors.tuna.tsinghua.edu.cn/qt/archive/qt/5.12/5.12.8/qt-opensource-linux-x64-5.12.8.run',
#                  'C:/Users/Tanyiqu/Desktop/测试打包',
#                  '4555.ts')
#     print(d.download())
#     pass
