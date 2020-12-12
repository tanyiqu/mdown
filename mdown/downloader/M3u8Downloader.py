import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import util.TextUtil as TextUtil
import util.OSUtil as OSUtil
from downloader.Downloader import Downloader
from downloader.TsDownloader import TsDownloader


class M3u8Downloader(Downloader):
    """
    m3u8视频下载器
    """

    # 构造器
    def __init__(self,
                 tsList: list,
                 path: str,
                 filename: str,
                 maxWorkers: int,
                 timeout: int,
                 interval: float = 0.5,
                 temp: bool = False):
        """
        构造器
        :param tsList: 下载链接的list
        :param path: 下载的路径（是路径）
        :param filename: 下载文件的名字
        :param maxWorkers: 最大的线程数
        :param timeout: 等待几秒
        :param interval: 时间间隔，用于记录网速等
        :param temp: 是否保留临时文件 为True时保留
        """

        self.tsList = tsList
        self.path = path
        self.filename = filename
        self.maxWorkers = maxWorkers
        self.timeout = timeout
        self.interval = interval  # 计时器停顿时间间隔
        self.temp = temp
        self.dataPerInterval = 0  # 每一个时间间隔所下载的流量
        # 文件输出路径
        self.outPath = ('%s\\%s' % (self.path, self.filename)).replace('\\', '/')
        # 临时文件存放路径
        self.tmpPath = (self.path + '\\__' + self.filename).replace('\\', '/')
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

    # 下载成功回调
    def __onFinished(self):
        # 清除临时文件
        if not self.temp:
            OSUtil.rmDir(self.tmpPath)
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
    def __getProgress(self, compact=False):
        if compact:
            return '[%d/%d]' % (self.completeNum, self.tsLength)
        else:
            return '[%d / %d]' % (self.completeNum, self.tsLength)
        pass

    # 进度条
    def __getProgressBar(self, fill='=', halfFill='>', space=' '):
        warnings.warn("此方法已过时，请考虑 __getCompatibleProgressBar", DeprecationWarning)
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
        bar = '[' + fill * num_fill + halfFill * num_half_fill + space * num_space + ']'
        return bar
        pass

    # 进度条
    def __getCompatibleProgressBar(self, fill: str = '=', halfFill: str = '-', space=' ', width: int = 33):
        """
        [==========-                      ]
        :param width: 进度条宽度
        :return:
        """

        if not 10 < width <= 100:
            width = 33

        # 满进度为100
        progress = int((self.completeNum / self.tsLength) * 100)

        calcProgress = progress * width / 100
        # 计算=的个数
        num_fill = int(calcProgress)
        # 计算-的个数
        if (calcProgress - int(calcProgress)) >= 0.5:
            num_half_fill = 1
        else:
            num_half_fill = 0
        # 计算空格的个数
        num_space = width - num_fill - num_half_fill
        return '[%s%s%s]' % (fill * num_fill, halfFill * num_half_fill, space * num_space)
        pass

    def showProgress(self):
        print('note: speed display may not be accurate.')
        while not self.isFinished():
            # print('\r' + ' ' * 120, end='')
            print('\r%s %s %s %s %s' % (
                self.__getProgress(compact=True), self.__getCompatibleProgressBar(halfFill='>', space='-'),
                self.__getPercentage(),
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
                self.__getProgress(compact=True), self.__getCompatibleProgressBar(halfFill='>', space='-'),
                self.__getPercentage(),
                self.__getSpeed(),
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
        downloader = TsDownloader(arg['url'], self.tmpPath, arg['index'], timeout=self.timeout,
                                  parentDownloader=self)
        downloader.download()
        pass

    # 合并成ts文件
    def merge(self):
        # 目录： self.tmpPath
        # 目标路径： self.outPath
        print('merging...')

        file = open(self.outPath, 'wb+')
        for i in range(self.tsLength):
            tsPath = '%s/%s' % (self.tmpPath, i)
            with open(tsPath, 'rb') as f:
                file.write(f.read())
                pass
            pass
        file.close()

        self.__onFinished()
        print('merging finished')

        pass

    pass
