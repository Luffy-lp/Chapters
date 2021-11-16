from time import sleep

from poco.agent import PocoAgent
from poco.drivers.std import StdPocoAgent
from poco.drivers.std.test.simple import TestStandardFunction
from poco.utils.simplerpc.simplerpc import RpcAgent

from common import COM_utilities
from common.COM_findobject import FindObject
from date.Chapters_data import MyData
from common.my_log import mylog
from airtest.core.api import *


class GameLoaded(FindObject):
    def __init__(self):
        self.GameLoaded_info = {}
        self.GameLoaded_info["loadtime"] = None
        self.GameLoaded_info["ErrorTxt"] = []

        COM_utilities.clock()  # 插入计时器
        self.mysleep(10)
        FindObject.__init__(self)

    def mainprocess(self):
        self.gameloading()
        # self.Popup_login(login)
        return True

    def gameloading(self):
        """游戏是否加载完成判断"""
        if self.find_try("DiscoverCanvas",description="大厅"):
            StdPocoAgent1 = StdPocoAgent()
            UserID = StdPocoAgent1.get_UserID()
            MyData.UserData_dir["uuid"] = UserID
            print("UserID:", UserID)
            self.GameLoaded_info["loadtime"]=0
            return
        while self.poco("Handle Slide Area").wait(1).exists():
            self.Popo_Errorinfo()
            # self.Popup_login(login=1)
            try:
                percentage= self.poco("Handle Slide Area").offspring("Progress").get_text()
                print("游戏加载进度：",percentage)
            except:
                print("未获取加载进度填充")
            if float(COM_utilities.clock("stop")) > 360:
                print("游戏加载失败。。。")
                log(Exception("游戏加载失败。。。"), snapshot=True)
                try:
                    raise Exception("游戏加载失败。。。")
                except Exception as e:
                    print("游戏加载失败。。。",e)
        if self.GameLoaded_info["loadtime"] is None:
            self.GameLoaded_info["loadtime"] = float(COM_utilities.clock("stop")) - 2
        # mylog.info("完成游戏加载，加载时间为{0}秒".format(self.GameLoaded_info["loadtime"]))
        print("已进入游戏界面")
        StdPocoAgent1 = StdPocoAgent()
        UserID = StdPocoAgent1.get_UserID()
        MyData.UserData_dir["uuid"] = UserID
        print("UserID:", UserID)
        try:
            MyData.getUsercurrency()
        except:
            print("虚拟币拉取失败")
        return True

    def Popup_login(self, login=1):
        """游戏进入界面弹框处理,0无弹框，1，有弹框跳过，2，有弹框点击登录"""
        login = int(login)
        if login == 0:
            return True
        if self.find_try("LoginGuide_LoginCtrl", description="游戏登陆弹框", waitTime=5):  # 登陆弹框
            self.GameLoaded_info["loadtime"] = float(COM_utilities.clock("stop")) - 2
            if login == 1:
                try:
                    # self.findClick_object("GuideViewBackBtn", "GuideViewBackBtn", description="点击返回箭头", waitTime=5,sleeptime=2)
                    self.notchfit__Click_try("GuideViewBackBtn", "GuideViewBackBtn", description="点击返回箭头",waitTime=5, sleeptime=2)
                finally:
                    self.findClick_object("StartGame", "StartGame", description="点击Play Now按钮", waitTime=2)
                    self.GameLoaded_info["游戏登陆弹框"] = "跳过登陆"
        return self.GameLoaded_info

    def Popo_Errorinfo(self):
        if self.android_tryfind("android:id/button1", description="android异常弹框"):
            self.android_findClick("android:id/button1", "android:id/button1", description="Google框架提示处理")
            mylog.error("检测到未安装谷歌框架，无法执行相关操作")
        if self.find_try("Title", description="unity异常弹框判断"):
        #     txtinfo=self.poco("Title").get_TMPtext()
        #     if txtinfo=="Info":
            try:
                TXT = self.poco("Context").get_TMPtext()
                self.GameLoaded_info["ErrorTxt"].append(TXT)
                self.findClick_try("CenterBtn","CenterBtn", description="Try again", waitTime=3)
                mylog.info("异常弹框，{0}".format(TXT))
            except:
                print("未发现弹框类型")
#
# GameLoaded1 = GameLoaded()
# GameLoaded1.gameloading()
# StdPocoAgent1 = StdPocoAgent()
# aa = StdPocoAgent1.get_sdk_version()
# print(aa)
# aa=self.call('GetSDKVersion')