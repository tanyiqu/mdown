"""
配置
静态类
"""


class Configuration:
    # 下载的url
    url = None
    # 下载输出文件的名字
    name = None
    # 下载文件的最大线程数
    thread = None
    # 下载文件输出路径
    outPath = None

    # 从第几个分段开始下载,0表示第一个
    begin = None
    # 从第几个分段结束下载,包含此分段,-1表示最后一个
    end = None

    # 要下载那个分段,只下载这个分段
    slice = None
    # 请求资源时，超时几秒后重试
    wait = None
    # 是否保留临时文件
    temp = False

    @staticmethod
    def showConfig():
        print('===============================')
        print('url', Configuration.url)
        print('name', Configuration.name)
        print('thread', Configuration.thread)
        print('outPath', Configuration.outPath)

        print('begin', Configuration.begin)
        print('end', Configuration.end)

        print('slice', Configuration.slice)
        print('wait', Configuration.wait)
        print('temp', Configuration.temp)
        print('===============================')

        pass

    pass
