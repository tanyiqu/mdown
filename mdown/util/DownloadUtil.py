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

    def __init__(self, tsList: list, path: str, filename: str, maxWorkers: int, interval: float = 0.5):
        self.tsList = tsList
        self.path = path
        self.filename = filename
        self.maxWorkers = maxWorkers
        self.interval = interval  # 计时器停顿时间间隔

        self.dataPerInterval = 0  # 每一个时间间隔所下载的流量

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

        executor.shutdown()
        self.endTime = time.time()
        print('download complete, took %s' % TextUtil.formatTime(self.endTime - self.startTime))
        self.merge()
        pass

    def isFinished(self):
        return self.completeNum == self.tsLength
        pass

    # 获取当前下载持续时长  00:01:23
    def __getCurrDuration(self):
        return TextUtil.formatTime(time.time() - self.startTime)
        pass

    # 获取当前下载百分比  12.34%
    def __getCurrPercentage(self):
        return '%.2lf%%' % (100.00 * (self.completeNum / self.tsLength))

    # 获取 上一个时间间隔的 平均网速 1.25MB/s
    def __getCurrSpeed(self):
        return TextUtil.byte2MB(int(self.dataPerInterval / self.interval)) + 'MB/s'
        pass

    # 获取当前完成任务数进度 [28 / 251]
    def __getCurrProgress(self):
        return '[%d / %d]' % (self.completeNum, self.tsLength)
        pass

    # 进度条
    def __getProgress(self):
        # [=========>                                        ]
        # 满进度为100，换算当前进度
        progress = int((self.completeNum / self.tsLength) * 100)
        num_1 = 0
        num_2 = 0
        num_3 = 0
        # 计算 = 的个数 ，> 的个数 和 空格的个数
        # 如果progress为偶数，= 为 progress/2，> 为 0，空格为 50减 =的个数
        # 如果progress为奇数，= 为 (progress-1)/2，> 为 1，空格为 50减(=的个数)-1
        if progress % 2 == 0:
            num_1 = progress // 2
            num_2 = 0
            num_3 = 50 - num_1
            pass
        else:
            num_1 = (progress - 1) // 2
            num_2 = 1
            num_3 = 50 - num_1 - num_2
            pass
        bar = '[' + '=' * num_1 + '>' * num_2 + ' ' * num_3 + ']'
        return bar
        pass

    def showProgress(self):
        print('note: speed display may not be accurate.')
        while not self.isFinished():
            print('\r' + ' ' * 120, end='')
            print('\r%s %s %s %s %s' % (
                self.__getCurrProgress(), self.__getProgress(), self.__getCurrPercentage(), self.__getCurrSpeed(),
                self.__getCurrDuration()
            ), end='')
            # 当前时间间隔内的流量清零
            self.lock.acquire()
            self.dataPerInterval = 0
            self.lock.release()
            time.sleep(self.interval)
            pass
        else:
            print('\r%s %s %s %s %s' % (
                self.__getCurrProgress(), self.__getProgress(), self.__getCurrPercentage(), self.__getCurrSpeed(),
                self.__getCurrDuration()
            ))
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
                        self.parentDownloader.lock.acquire()
                        self.parentDownloader.dataPerInterval += len(data)
                        self.parentDownloader.lock.release()
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
