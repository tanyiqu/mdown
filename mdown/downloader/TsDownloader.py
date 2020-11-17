import requests
from downloader.Downloader import Downloader


class TsDownloader(Downloader):
    """
    下载ts文件的下载器
    真正实现下载功能的下载器
    """

    # 构造器
    def __init__(self,
                 url: str,
                 path: str,
                 num: int,
                 timeout: int,
                 parentDownloader: Downloader,
                 noSuffix: bool = True):
        """
        构造器
        :param url: 要下载的那一分段的url
        :param path: 被下载的路径（只是路径）
        :param num: 这是第几个分段，从0开始
        :param timeout: 等待几秒
        :param parentDownloader: 指定一个父下载器，M3u8Downloader
        :param noSuffix: 指定下载的文件，带不带【.ts】后缀
        """

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
                self.parentDownloader.lock.acquire()
                self.parentDownloader.completeNum += 1
                self.__onFinished()
                self.parentDownloader.lock.release()
                break
                pass
            except requests.exceptions.RequestException:
                i += 1
                pass
            pass
        pass
        pass

    def __onFinished(self):
        pass

    pass
