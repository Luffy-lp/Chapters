# from asyncio import sleep
from time import sleep
from scenes.scenes_login.SCN_signin import SignIn
from common import COM_utilities
from common.COM_findobject import FindObject
from scenes.scenes_login.SCN_newuser import NewUserGuide
from scenes.SCN_pageTurn import PageTurn
from common.my_log import mylog
from airtest.core.api import *


class GameLoaded(FindObject):
    GameLoaded_info = {}
    __instance = None
    ErrorTxt = []
    GameLoaded_info["ErrorTxt"] = ErrorTxt

    def __init__(self):
        COM_utilities.clock()  # 插入计时器
        self.mysleep(10)
        FindObject.__init__(self)
    def mainprocess(self, login=0):
        self.gameloading()
        self.Popup_login(login)
        return True

    def gameloading(self):  # 游戏是否加载完成判断
        NewUserGuide1 = NewUserGuide()
        # self.find_object("LoadingPanel", description="游戏加载界面", sleeptime=1)
        while self.poco("Slider").wait(1).exists():
            self.Popo_Errorinfo()
            self.Popup_login(login=1)
            mytime = float(COM_utilities.clock("stop"))
            if mytime > 360:
                print("游戏加载失败。。。")
                log(Exception("游戏加载失败。。。"))
                raise Exception
        loadtime = COM_utilities.clock("stop")
        self.GameLoaded_info["loadtime"] = loadtime
        mylog.info("完成游戏加载，加载时间为{0}秒".format(loadtime))
        print("完成游戏加载，加载时间为{0}秒".format(loadtime))
        return True

    def Popup_login(self, login=1):
        """游戏进入界面弹框处理,0无弹框，1，有弹框跳过，2，有弹框点击登录"""
        login=int(login)
        if login==0:
            return True
        if self.find_try("LoginGuide_LoginCtrl", description="游戏登陆弹框", waitTime=5):  # 登陆弹框
            if login == 1:
                try:
                    self.findClick_object("GuideViewBackBtn", "GuideViewBackBtn", description="点击返回箭头", waitTime=5,sleeptime=2)
                finally:
                    self.findClick_object("StartGame", "StartGame", description="点击Play Now按钮", waitTime=2)
                    self.GameLoaded_info["游戏登陆弹框"] = "跳过登陆"
            elif login == 2:
                SignIn1 = SignIn()
                SignIn1.loginGuide_login_process()
                sleep(3)
                self.GameLoaded_info["游戏登陆弹框"] = "登陆"
                self.GameLoaded_info["登陆状态"] = SignIn1.SignIn_info["用户登陆状态"]
                self.PageTurn.Bottom_click(0)
        return self.GameLoaded_info

    def Popo_Errorinfo(self):
        if self.android_tryfind("android:id/button1",description="Google框架弹框"):
            self.android_findClick("android:id/button1","android:id/button1",description="Google框架提示处理")
            mylog.error("检测到未安装谷歌框架，无法执行相关操作")
        if self.find_try("Context", description="异常弹框"):
            TXT = self.poco("Context").get_TMPtext()
            self.GameLoaded_info["ErrorTxt"].append(TXT)
            self.click_object("CenterBtn", description="Try again",waitTime=5)
            mylog.info("异常弹框，{0}".format(TXT))