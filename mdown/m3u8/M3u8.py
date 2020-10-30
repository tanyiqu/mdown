import m3u8.decode as decode


class M3u8:
    __url__ = ''

    # 构造
    def __init__(self, url):
        self.__url__ = url
        pass

    def hello(self):
        print(self.__url__)
        decode.decode()
        pass

    pass
