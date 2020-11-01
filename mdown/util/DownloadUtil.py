"""
文件下载模块
"""

import requests
import time
import os
import threading
import threadpool


class M3u8Downloader:
    __list = []
    __filename = ''
    __path = ''
    __tmpPath = ''
    __length = 0
    __downloader = None
    __workers = 0

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
            downloader = Downloader(dit['url'], self.__tmpPath, dit['name'])
            downloader.download()
            pass

        pool = threadpool.ThreadPool(128)

        reqs = threadpool.makeRequests(_download, self.__list)

        for req in reqs:
            pool.putRequest(req)
            pass

        pool.wait()

        # for i in range(30):
        # downloader = Downloader(self.__list[i]['url'], self.__tmpPath, self.__list[i]['name'])
        # thread = threading.Thread(target=downloader.download)
        # thread.start()
        # pass

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
        resp = requests.get(self.__url, stream=True)
        duration = time.time() - duration

        with open(self.__path + '/' + self.__filename, "wb") as f:
            for data in resp.iter_content(1024):
                f.write(data)
            pass

        # length = int(resp.headers['Content-Length']) / (1024 ** 2)
        # speed = length / duration
        # return {
        #     'length': length,
        #     'duration': duration,
        #     'speed': speed
        # }

        pass

    pass


if __name__ == '__main__':
    d = Download('https://yuledy.helanzuida.com/20200402/1745_5f787176/1000k/hls/964e77c2ad0000033.ts',
                 # d = Download('https://mirrors.tuna.tsinghua.edu.cn/qt/archive/qt/5.12/5.12.8/qt-opensource-linux-x64-5.12.8.run',
                 'C:/Users/Tanyiqu/Desktop/测试打包',
                 '4555.ts')
    print(d.download())
    pass
