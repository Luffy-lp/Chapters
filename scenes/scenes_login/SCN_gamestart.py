import sys

from airtest.core.api import *
from pathlib import Path
from common.COM_data import MyData
from common.my_log import mylog

class GameStart():
    isStarGame = False
    GameStart_info = {}
    _instance = None

    def installGame(self):  # 安装应用
        packageName = MyData.ConfData_dir["packageName"]
        print(MyData.ConfData_dir["packagepath"])
        mypath = MyData.ConfData_dir["packagepath"]
        my_file = Path(mypath)
        if my_file.is_file():
            list = G.DEVICE.list_app(third_only=True)
            for i in list:
                if i == packageName:
                    print("{0}包已经安装".format(packageName))
                    self.GameStart_info["安装apk"] = True
                    return True
            print("正在安装apk这时间可能有点长", packageName)  # 需要解决安装很慢。。。。。。。。。。。。。。
            mylog.info("正在安装【{}】--apk包".format(packageName))
            G.DEVICE.install_app(mypath)
            mylog.info("已经安装【{}】--apk包".format(packageName))
            self.GameStart_info["安装apk"] = True
        else:
            print("未找到对应的安装包")
            return False

    def uninstallGame(self, package=MyData.ConfData_dir["packageName"], **kwargs):  # 卸载应用
        packageName = MyData.ConfData_dir["packageName"]
        mypath = MyData.ConfData_dir["packagepath"]
        my_file = Path(mypath)
        if my_file.is_file():
            list = G.DEVICE.list_app(third_only=True)
            for i in list:
                if i == packageName:
                    uninstall(package, **kwargs)
                    mylog.info("已经卸载【{}】--apk包".format(packageName))
                    return True
        else:
            mylog.info("未找到【{}】--apk包".format(packageName))

    def processCount(self):
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % MyData.ConfData_dir["packageName"])
        a = os.popen("tasklist")
        return p.read().count(MyData.ConfData_dir["packageName"])

    def starGame(self):  # 启动游戏
        wake()
        print("尝试启动游戏")
        mylog.info("启动游戏")
        start_app(MyData.ConfData_dir["packageName"])
        print("等待加载")
        self.isStarGame = True

    def stopGame(self):
        stop_app(MyData.ConfData_dir["packageName"])
        print("停止游戏")
        mylog.info("停止游戏")
        return True

    def clearGame(self):
        clear_app(MyData.ConfData_dir["packageName"])
        print("清理设备上的游戏数据")

