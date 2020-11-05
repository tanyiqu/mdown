from abc import abstractmethod


class Downloader:
    """
    下载器接口类
    """

    @abstractmethod
    def download(self):
        pass

    pass
