from airtest.core.api import log
from airtest.core.api import assert_equal, wake
from time import sleep
from scenes.scenes_login.SCN_gamestart import GameStart
from scenes.scenes_login.SCN_gameloaded import GameLoaded
from scenes.scenes_login.SCN_newuser import NewUserGuide
from scenes.scenes_discover.SCN_discover import Discover
from scenes.scenes_visualbook.SCN_bookdetail import BookNewDetail
from scenes.scenes_login.SCN_signin import SignIn
from scenes.SCN_pageTurn import PageTurn
from scenes.scenes_SidePanel.SCN_LanguagePanel import LanguagePanel

def pageTurn(type="Bottom",index=None,index1=None):
    """界面切换 Bottom，Upper"""
    PageTurn1 = PageTurn()
    if type=="Bottom":
        if index == None:
            PageTurn1.click_close()
            return True
        else:
            PageTurn1.Bottom_click(index)
    elif type=="Upper":
        PageTurn1.Upper_click(index)
    elif type == "POS":
        PageTurn1.click_pos(index,index1)
    sleep(2)

def test_uninstallGame():
    """卸载游戏"""
    myGameStart = GameStart()
    myGameStart.uninstallGame()
    sleep(1)


def test_installGame():
    """安装卸载游戏"""
    myGameStart = GameStart()
    myGameStart._instance = myGameStart
    actualValue = myGameStart.installGame()
    assert_equal(actualValue, True, "安装游戏")

def test_startgame():
    """启动游戏"""
    myGameStart = GameStart()
    myGameStart.stopGame()
    sleep(1)
    myGameStart.starGame()
    # assert_equal(myGameStart.isStarGame, True, "启动游戏{0}".format(myGameStart.GameStart_info))

def test_signin(login="Google", email="15019423971", password="yo5161381"):
    """用户绑定"""
    SignIn1 = SignIn()
    actualValuSignIne = SignIn1.process_profilelogin()
    SignIn1.issign()  # 判断用户登陆情况
    assert_equal(True, actualValuSignIne, "用户绑定{0}".format(SignIn1.SignIn_info))
    sleep(3)


