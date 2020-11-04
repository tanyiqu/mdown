"""
文件下载模块
"""

import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import util.TextUtil as TextUtil


class M3u8Downloader:
    """
    m3u8视频下载器
    """

    def __init__(self, tsList: list, path: str, filename: str, maxWorkers: int):
        self.tsList = tsList
        self.path = path
        self.filename = filename
        self.maxWorkers = maxWorkers

        # 文件输出路径
        self.outPath = ('%s\\%s' % (self.path, self.filename)).replace('\\', '/')

        # 临时文件存放路径
        self.tmpPath = (self.path + '\\.' + self.filename).replace('\\', '/')

        # ts序列长度
        self.tsLength = len(self.tsList)

        # 下载开始、结束时间
        self.startTime = 0
        self.endTime = 0

        # 锁
        self.lock = threading.Lock()

        # ts完成数
        self.completeNum = 0

        pass

    def isFinished(self):
        return self.completeNum == self.tsLength
        pass

    def download(self):
        print('output: [' + self.outPath + ']')
        self.startTime = time.time()

        # 在路径里创建临时文件夹
        os.mkdir(self.tmpPath)

        # 开启线程池进行下载
        executor = ThreadPoolExecutor(max_workers=self.maxWorkers)
        for tmp in self.tsList:
            executor.submit(self._download, tmp)
            pass

        # 显示进度
        self.showProgress()
        #

        executor.shutdown()
        self.endTime = time.time()
        print('download complete, took %s' % TextUtil.formatTime(self.endTime - self.startTime))
        self.merge()
        pass

    def _calcProgress(self):
        p = '%d / %d\r' % (self.completeNum, self.tsLength)
        print(p)
        pass

    def showProgress(self):
        while not self.isFinished():
            self._calcProgress()
            time.sleep(1)
            pass
        else:
            self._calcProgress()
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
        downloader = TsDownloader(arg['url'], self.tmpPath, arg['index'], self)
        downloader.download()
        pass

    # 合并成ts文件
    def merge(self):
        # 目录： self.tmpPath
        # 目标路径： self.outPath
        print('merging...')

        file = open(self.outPath, 'wb+')
        for i in range(self.tsLength):
            tsPath = '%s\\%s' % (self.tmpPath, i)
            with open(tsPath, 'rb') as f:
                file.write(f.read())
                pass
            pass
        file.close()

        print('merging finished')
        pass

    pass


class TsDownloader:
    """
    下载ts文件的下载器
    """

    def __init__(self, url: str, path: str, num: int, parentDownloader: M3u8Downloader, timeout: int = 5,
                 noSuffix: bool = True):
        self.url = url
        self.path = path
        self.num = num
        self.parentDownloader = parentDownloader
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
                # print('%s is ok' % self.num)
                self.parentDownloader.lock.acquire()
                self.parentDownloader.completeNum += 1
                self.parentDownloader.lock.release()
                break
                pass
            except requests.exceptions.RequestException:
                i += 1
                # print('%s retry %d' % (self.num, i))
                pass
            pass
        pass
        pass

    pass

# if __name__ == '__main__':
#     f = open('C:/Users/Tanyiqu/Desktop/tmp/index.ts', 'wb+')
#
#     f.close()
#     pass
