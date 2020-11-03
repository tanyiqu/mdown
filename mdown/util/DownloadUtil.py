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
            downloader = TsDownloader(dit['url'], self.__tmpPath, dit['index'])
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


class TsDownloader:
    """
    下载ts文件的下载器
    """

    def __init__(self, url: str, path: str, num: int, timeout: int = 5, noSuffix: bool = True):
        self.url = url
        self.path = path
        self.num = num
        self.timeout = timeout
        self.noSuffix = noSuffix
        self.filename = str(num)
        if not self.noSuffix:
            self.filename += '.ts'
        pass

    def download(self):
        # 两种方式
        # 1.边下边写
        # resp = requests.get(url=self.url, timeout=self.timeout)
        # with open(self.path + '/' + self.filename, "wb") as f:
        #     for data in resp.iter_content(1024):
        #         f.write(data)
        #     pass

        # 2.下完再写
        # resp = requests.get(url=self.url, timeout=self.timeout)
        # with open(self.path + '/' + self.filename, "wb") as f:
        #     f.write(resp.content)
        #     pass

        i = 0
        # 如果请求失败就重新请求，直至请求成功
        while True:
            try:
                resp = requests.get(url=self.url, timeout=self.timeout)
                with open(self.path + '/' + self.filename, "wb") as f:
                    for data in resp.iter_content(1024):
                        f.write(data)
                    pass
                print('%s is ok' % self.num)
                break
                pass
            except requests.exceptions.RequestException:
                i += 1
                print('%s retry %d' % (self.num, i))
                pass
            pass
        pass
        pass

    pass


if __name__ == '__main__':
    ts = TsDownloader()
    ts.print()
    ts.set()
    ts.print()

    pass
