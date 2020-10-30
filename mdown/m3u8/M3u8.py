import util.WebUtil as WebUtil
import re

"""
思路：
获取m3u8文件序列，然后组成单个的下载直链
使用多线程下载这些文件
然后再合并成完整的ts文件

一般m3u8文件有两层，但也有些例外
需要判断url链接是直链还是重定向的链接
"""


# 获取链接的前缀
def getPre(url: str):
    return url[0:url.rfind('/') + 1]


class M3u8:
    __url__ = ''  # m3u8链接
    __urlPre__ = ''  # m3u8链接前缀
    __innerUrl__ = ''  # 内层m3u8链接
    __innerUrlPre__ = ''  # 内层m3u8链接前缀
    __indexContent__ = ''  # 外层文件内容
    __content__ = ''  # 内层文件内容
    __tsList__ = []  # ts文件集合
    __tsLength = 0
    __isM3u8__ = False  # 是否是m3u8链接

    # 构造
    def __init__(self, url):
        self.__url__ = url
        self.detectUrl()
        if self.__isM3u8__:
            self.__getList__()
        pass

    # 判断链接是否为m3u8文件，如果是则获取内层文件内容
    def detectUrl(self):
        """
        思路：获取链接内容，然后正则匹配是否包含 #EXTM3U
        如果包含则匹配 #EXTINF
        """
        txt = WebUtil.getText(self.__url__)
        if txt == '':
            self.__isM3u8__ = False
            return
        reg = r'^#EXTM3U'
        if re.search(reg, txt):
            # 匹配成功，是m3u8链接
            self.__isM3u8__ = True
            reg = r'#EXTINF'

            # 判断是内层还是外层
            if re.search(reg, txt):
                # 是内层链接
                self.__innerUrl__ = self.__url__
                self.__content__ = txt
                self.__innerUrlPre__ = getPre(self.__innerUrl__)
                pass
            else:
                # 是外层链接
                # 取内层
                self.__indexContent__ = txt
                self.__urlPre__ = getPre(self.__url__)
                self.__getInnerContent__()
                pass
            pass
        else:
            # 不是m3u8链接
            self.__isM3u8__ = False
            pass
        pass

    def isM3u8(self):
        return self.__isM3u8__

    # 获取内层文件内容
    def __getInnerContent__(self):
        # 获取 xxk/hls/index.m3u8 ，一般在文件最后一行
        lk = self.__indexContent__.split('\n')[-1:][0]
        # 拼接inner url
        self.__innerUrl__ = self.__urlPre__ + lk

        # 获取链接内容
        txt = WebUtil.getText(self.__innerUrl__)
        if txt == '':
            self.__isM3u8__ = False
        else:
            self.__content__ = txt
            self.__isM3u8__ = True
        pass

    # 获取视频直链列表
    def __getList__(self):
        """
        匹配类似下面的序列
        #EXTINF:1.000000,
        xxxxxxxxx.ts
        """
        self.__innerUrlPre__ = getPre(self.__innerUrl__)

        reg = r'#EXTINF:.*?\n(.*?\.ts)'
        res = re.findall(reg, self.__content__)
        self.__tsList__ = []
        i = 0
        for item in res:
            self.__tsList__.append({
                'index': i,
                'name': item,
                'url': self.__innerUrlPre__ + item
            })
            i += 1
            pass
        return self.__tsList__

    def getList(self):
        return self.__tsList__
        pass

    def getTsLength(self):
        return len(self.__tsList__)
        pass

    pass


if __name__ == '__main__':
    # m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/index.m3u8')
    # m = M3u8('https://douban.donghongzuida.com/20200918/9893_7cec614e/index.m3u8')
    # m = M3u8('https://xigua-cdn.haima-zuida.com/20200625/8575_d71b372e/index.m3u8')
    m = M3u8('https://yuledy.helanzuida.com/20200402/1745_5f787176/index.m3u8')
    # m = M3u8('https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8')
    # m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/1000k/hls/index.m3u8')

    print(m.getTsLength())
    print(m.getList())
    pass
