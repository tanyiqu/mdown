import util.WebUtil as WebUtil
import util.TextUtil as TextUrl
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
    __url = ''                  # m3u8链接
    __urlPre = ''               # m3u8链接前缀
    __innerUrl = ''             # 内层m3u8链接
    __innerUrlPre = ''          # 内层m3u8链接前缀
    __indexContent = ''         # 外层文件内容
    __content = ''              # 内层文件内容
    __tsList = []               # ts文件集合
    __tsLength = 0              # ts文件个数
    __durationSec = 0.0         # 视频的时长(秒)
    __duration = '00:00:00'     # 视频的时长(hh:mm:ss)
    __isM3u8 = False            # 是否是m3u8链接

    # 构造
    def __init__(self, url):
        self.__url = url
        self.__detectUrl()
        if self.__isM3u8:
            self.__getList()
        pass

    # 判断链接是否为m3u8文件，如果是则获取内层文件内容
    def __detectUrl(self):
        """
        思路：获取链接内容，然后正则匹配是否包含 #EXTM3U
        如果包含则匹配 #EXTINF
        """
        txt = WebUtil.getText(self.__url)
        if txt == '':
            self.__isM3u8 = False
            return
        reg = r'^#EXTM3U'
        if re.search(reg, txt):
            # 匹配成功，是m3u8链接
            self.__isM3u8 = True
            reg = r'#EXTINF'

            # 判断是内层还是外层
            if re.search(reg, txt):
                # 是内层链接
                self.__innerUrl = self.__url
                self.__content = txt
                self.__innerUrlPre = getPre(self.__innerUrl)
                pass
            else:
                # 是外层链接
                # 取内层
                self.__indexContent = txt
                self.__urlPre = getPre(self.__url)
                self.__getInnerContent()
                pass
            pass
        else:
            # 不是m3u8链接
            self.__isM3u8 = False
            pass
        pass

    # 获取内层文件内容
    def __getInnerContent(self):
        # 获取 xxk/hls/index.m3u8 ，一般在文件最后一行
        lk = self.__indexContent.split('\n')[-1:][0]
        # 拼接inner url
        self.__innerUrl = self.__urlPre + lk

        # 获取链接内容
        txt = WebUtil.getText(self.__innerUrl)
        if txt == '':
            self.__isM3u8 = False
        else:
            self.__content = txt
            self.__isM3u8 = True
        pass

    # 获取视频直链列表
    def __getList(self):
        """
        匹配类似下面的序列
        #EXTINF:1.000000,
        xxxxxxxxx.ts
        """
        self.__innerUrlPre = getPre(self.__innerUrl)

        reg = r'#EXTINF:(.*?),\n(.*?\.ts)'
        res = re.findall(reg, self.__content)
        self.__tsList = []
        i = 0
        for item in res:
            duration = float(item[0])
            self.__tsList.append({
                'index': i,
                'name': item[1],
                'duration': duration,
                'url': self.__innerUrlPre + item[1]
            })
            # 依次相加时长
            self.__durationSec += duration
            i += 1
            pass
        # 计算时长
        self.__duration = TextUrl.formatTime(self.getDurationSecond())
        return self.__tsList

    def isM3u8(self):
        return self.__isM3u8

    def getList(self):
        return self.__tsList
        pass

    def getTsLength(self):
        return len(self.__tsList)
        pass

    def getDurationSecond(self):
        return int(self.__durationSec)

    def getDuration(self):
        return self.__duration

    pass


if __name__ == '__main__':
    # m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/index.m3u8')
    m = M3u8('https://leshi.cdn-zuyida.com/20170604/L9pBumBj/index.m3u8')
    # m = M3u8('https://douban.donghongzuida.com/20200918/9893_7cec614e/index.m3u8')
    # m = M3u8('https://xigua-cdn.haima-zuida.com/20200625/8575_d71b372e/index.m3u8')
    # m = M3u8('https://yuledy.helanzuida.com/20200402/1745_5f787176/index.m3u8')
    # m = M3u8('https://mei.huazuida.com/20191220/19588_51b84e32/index.m3u8')
    # m = M3u8('https://meng.wuyou-zuida.com/20200227/26199_992e4909/1000k/hls/index.m3u8')

    print(m.getTsLength())
    print(m.getList())
    print(m.getDuration())
    pass
