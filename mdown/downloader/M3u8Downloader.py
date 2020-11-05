import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import util.TextUtil as TextUtil
from downloader.Downloader import Downloader
from downloader.TsDownloader import TsDownloader


class M3u8Downloader(Downloader):
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
    def __getDuration(self):
        return TextUtil.formatTime(time.time() - self.startTime)
        pass

    # 获取当前下载百分比  12.34%
    def __getPercentage(self):
        return '%.2lf%%' % (100.00 * (self.completeNum / self.tsLength))

    # 获取 上一个时间间隔的 平均网速 1.25MB/s
    def __getSpeed(self):
        return TextUtil.byte2Speed(int(self.dataPerInterval / self.interval))
        pass

    # 获取当前完成任务数进度 [28 / 251]
    def __getProgress(self):
        return '[%d / %d]' % (self.completeNum, self.tsLength)
        pass

    # 进度条
    def __getProgressBar(self, fill='=', halfFill='>'):
        # [=========>                                        ]
        # 满进度为100，换算当前进度
        progress = int((self.completeNum / self.tsLength) * 100)
        # 计算 = 的个数 ，> 的个数 和 空格的个数
        # 如果progress为偶数，= 为 progress/2，> 为 0，空格为 50减 =的个数
        # 如果progress为奇数，= 为 (progress-1)/2，> 为 1，空格为 50减(=的个数)-1
        if progress % 2 == 0:
            num_fill = progress // 2
            num_half_fill = 0
            num_space = 50 - num_fill
            pass
        else:
            num_fill = (progress - 1) // 2
            num_half_fill = 1
            num_space = 50 - num_fill - num_half_fill
            pass
        bar = '[' + fill * num_fill + halfFill * num_half_fill + ' ' * num_space + ']'
        return bar
        pass

    def showProgress(self):
        print('note: speed display may not be accurate.')
        while not self.isFinished():
            # print('\r' + ' ' * 120, end='')
            print('\r%s %s %s %s %s' % (
                self.__getProgress(), self.__getProgressBar(halfFill='-'), self.__getPercentage(),
                self.__getSpeed(),
                self.__getDuration()
            ), end='')
            # 当前时间间隔内的流量清零
            self.lock.acquire()
            self.dataPerInterval = 0
            self.lock.release()
            time.sleep(self.interval)
            pass
        else:
            print('\r%s %s %s %s %s' % (
                self.__getProgress(), self.__getProgressBar(), self.__getPercentage(), self.__getSpeed(),
                self.__getDuration()
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
