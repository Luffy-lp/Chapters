from airtest.core.api import log
from airtest.core.api import assert_equal, wake
from time import sleep
from common.COM_findobject import FindObject
from scenes.scenes_login.SCN_gameloaded import GameLoaded
from scenes.scenes_login.SCN_newuser import NewUserGuide
from scenes.scenes_discover.SCN_discover import Discover
from scenes.SCN_pageTurn import PageTurn
from scenes.scenes_SidePanel.SCN_LanguagePanel import LanguagePanel

def test_click(findName,clickName,description):
    """点击按钮"""
    MYclikObject=FindObject()
    MYclikObject.findClick_object(findName=findName,ClickName=clickName,description=description)

def test_sleep(sleeptime):
    """睡眠时间"""
    sleep(float(sleeptime))

def pageTurn(type="Bottom",index=None,index1=None):
    """界面切换 Bottom，Upper"""
    PageTurn1 = PageTurn()
    if type == "Bottom":
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
def test_GameLoaded(login):
    myGameLoaded = GameLoaded()
    actualValue = myGameLoaded.mainprocess(login=login)
    if float(myGameLoaded.GameLoaded_info["loadtime"])>50:
        log(Exception("load游戏时间大于30s！加载时间为：{0}".format(myGameLoaded.GameLoaded_info["loadtime"])),snapshot=True)
    assert_equal(actualValue, True, "启动游戏{0}".format(myGameLoaded.GameLoaded_info))
    sleep(3)

def test_discoverPopup():
    """大厅弹框"""
    myDiscover = Discover()
    actualValue = myDiscover.discoverPopup()
    assert_equal(True, actualValue, "大厅弹框列表{0}".format(myDiscover.Popuplist))
    sleep(3)

def test_discoverPopup_noassert():
    """大厅弹框"""
    myDiscover = Discover()
    myDiscover.discoverPopup()
    sleep(3)

def test_LanguageChoose(language):
    """切换语言"""
    myLanguagePanel=LanguagePanel()
    myLanguagePanel.click_language()  # 进入选择语言界面
    actualValue= myLanguagePanel.chooseLanguage(language)
    if myLanguagePanel.LanguagePanel_info["switch"]:
        test_GameLoaded(1)
    else:
        myLanguagePanel.click_back()
    assert_equal(actualValue, True, "切换语言{0}".format(myLanguagePanel.LanguagePanel_info))

def test_checkLanguageChoose(language):
    """检查语言"""
    myLanguagePanel=LanguagePanel()
    myLanguagePanel.click_language()  # 进入选择语言界面
    myLanguagePanel.checkLanguageChoose(language) #检查语言是设置语言
    myLanguagePanel.click_back()
    actualValue = (myLanguagePanel.LanguagePanel_info["当前语言"] == language and True or False)
    assert_equal(actualValue, True, "语言检查{0}".format(myLanguagePanel.LanguagePanel_info))

def test_newUserGuide():
    """新手引导"""
    myNewUserGuide = NewUserGuide()
    actualValue = myNewUserGuide.newUserPopUp()
    assert_equal(actualValue, True, "新手引导{0}".format(myNewUserGuide.NewUserGuide_info))

