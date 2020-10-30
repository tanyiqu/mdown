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


class M3u8:
    __url__ = ''  # m3u8链接
    __innerUrl__ = ''
    __index_content__ = ''  # 外层文件内容
    __content__ = ''  # 内层文件内容
    __tsList__ = ''  # ts文件集合
    __isM3u8__ = False  # 是否是m3u8链接

    # 构造
    def __init__(self, url):
        self.__url__ = url
        self.detectUrl()
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
            return self.__isM3u8__
        reg = r'^#EXTM3U'
        if re.search(reg, txt):
            # 匹配成功，是m3u8链接
            self.__isM3u8__ = True
            # 判断是内层还是外层
            reg = r'#EXTINF'
            if re.search(reg, txt):
                # 成功，是内层链接
                self.__content__ = txt
                pass
            else:
                # 获取内层内容
                self.__index_content__ = txt
                self.__getInnerContent__()
                pass
            pass
        pass

    def isM3u8(self):
        return self.__isM3u8__

    # 获取内层文件内容
    def __getInnerContent__(self):
        """
        内层链接为 自己的链接 拼接 xxk/hls/index.m3u8
        """
        self.__content__ = ''
        # 获取自己的链接
        reg = '^(.*?)index.m3u8'
        u = re.findall(reg, self.__url__)[0]
        # 获取 xxk/hls/index.m3u8 ，一般在文件最后一行
        lk = self.__index_content__.split('\n')[-1:][0]
        url = u + lk

        # 获取链接内容
        txt = WebUtil.getText(url)
        if txt == '':
            self.__isM3u8__ = False
        else:
            self.__content__ = txt
            self.__isM3u8__ = True
        pass

    # 获取视频直链列表
    def getList(self):

        """
        匹配下面的序列
        #EXTINF:7.960000,
        d2af79ce06c000000.ts
        """
        reg = r'#EXTINF:.*?\n(.*?\.ts)'
        res = re.findall(reg, self.__content__)
        print(res)
        pass

    pass


if __name__ == '__main__':
    # m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/index.m3u8')
    m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/1000k/hls/index.m3u8')
    # print(m.__content__)
    m.getList()
    pass
