import winreg
import os

"""
OS操作工具类
"""


# 获取当前用户桌面路径，仅windows
def getDesktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
    pass


# 获取当前工作路径
def getPath():
    return os.path.abspath('.')
    pass


# 删除指定文件夹及其文件
def deleteDir(path: str):
    pass
