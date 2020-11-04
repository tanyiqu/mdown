"""
文件下载模块
"""

import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor


class M3u8Downloader:
    """
    m3u8视频下载器
    """

    def __init__(self, tsList: list, path: str, filename: str, maxWorkers: int):
        self.tsList = tsList
        self.path = path
        self.filename = filename
        self.tmpPath = self.path + '\\.' + self.filename
        self.maxWorkers = maxWorkers
        self.tsLength = len(self.tsList)
        pass

    def download(self):
        print('output: [%s\\%s]' % (self.path, self.filename))

        # 在路径里创建临时文件夹
        os.mkdir(self.tmpPath)

        # 开启线程池进行下载
        executor = ThreadPoolExecutor(max_workers=self.maxWorkers)
        for tmp in self.tsList:
            executor.submit(self._download, tmp)
            pass

        # 显示进度

        executor.shutdown(wait=True)
        print('download finished')
        pass

        pass

    # 在线程中被调用的任务
    def _download(self, arg):
        """
        arg:{
            index
            name
            duration
            url
        }
        """
        downloader = TsDownloader(arg['url'], self.tmpPath, arg['index'])
        downloader.download()
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
