from time import sleep
from common.COM_path import *
from airtest.core.api import assert_equal, wake
from airtest.report.report import simple_report

from scenes.scenes_community.SCN_creation import Creation
from scenes.scenes_login.SCN_gamestart import GameStart
from scenes.scenes_login.SCN_gameloaded import GameLoaded
from scenes.scenes_login.SCN_newuser import NewUserGuide
from scenes.scenes_discover.SCN_discover import Discover
from scenes.scenes_visualbook.SCN_bookread import VisualBook
from scenes.scenes_visualbook.SCN_bookdetail import BookNewDetail
from scenes.scenes_login.SCN_signin import SignIn
from scenes.SCN_pageTurn import PageTurn
from scenes.scenes_community.SCN_chapteredit import ChapterEdit
from scenes.scenes_community.SCN_community import Community
from scenes.scenes_community.SCN_readUGCbook import ReadUGCBook
from scenes.scenes_shop.SCN_shop import Shopmodule
from scenes.scenes_profile.SCN_profilemodule import Profilemodule
from scenes.scenes_profile.SCN_achievementmodule import Achievementmodule
from common.COM_data import MyData
from common.COM_findobject import CommonPoco
# import allure
__author__ = "lipeng"
__title__ = "Chapters"
__desc__ = "脚本描述"


# __file__ = "D:\ChaptersApp_Auto\common"


# Airtest提供了assert_exists和assert_not_exists两个接口，来断言一张图片存在或不存在于当前画面中。
#
# 同时，还提供了assert_equal和assert_not_equal两个语句，来断言传入的两个值相等或者不相等。

def test_uninstallGame():
    """卸载游戏"""
    myGameStart = GameStart()
    myGameStart.uninstallGame()
    sleep(1)


def test_installGame():
    """安装卸载游戏"""
    myGameStart = GameStart()
    myGameStart._instance = myGameStart
    myGameStart.installGame()
    assert_equal(myGameStart.GameStart_info["安装apk"], True, "安装游戏")


def test_startgame(login):
    """启动游戏"""
    myGameStart = GameStart()
    stopGame = myGameStart.stopGame()
    sleep(1)
    myGameStart.starGame()
    assert_equal(myGameStart.isStarGame, True, "启动游戏{0}".format(myGameStart.GameStart_info))
    myGameLoaded = GameLoaded()
    actualValue = myGameLoaded.mainprocess(login=login)
    assert_equal(actualValue, True, "加载游戏详情{0}".format(myGameLoaded.GameLoaded_info))
    sleep(3)


def test_discoverPopup():
    """大厅弹框"""
    myDiscover = Discover()
    discoverPopup = myDiscover.discoverPopup()
    assert_equal(True, discoverPopup[0], "大厅弹框列表{0}".format(discoverPopup[1]))
    sleep(3)


def test_signin(login="Google",email="15019423971",password="yo5161381"):
    """用户绑定"""
    SignIn1 = SignIn()
    actualValuSignIne = SignIn1.process_profilelogin()
    SignIn1.issign()  # 判断用户登陆情况
    assert_equal(True, actualValuSignIne, "登陆详情{0}".format(SignIn1.SignIn_info))
    sleep(3)


def test_newUserGuide():
    """新手引导"""
    myNewUserGuide = NewUserGuide()
    isNewUserGuide = myNewUserGuide.newUserPopUp()
    assert_equal(True, True, "新手引导弹出情况：{0}".format(isNewUserGuide[1]))

def test_bookchoose(bookShelf, index):
    """找书"""
    bookdetail = BookNewDetail()
    bookdetail.bookChoose(bookShelf=bookShelf, index=index)
    # actualValue = bookdetail.getBookNewDetail_info()
    assert_equal(True, True, "书籍选择{0}".format(bookdetail.BookNewDetail_info))


def test_bookPlay():
    """Play书籍"""
    bookdetail = BookNewDetail()
    actualValue = bookdetail.book_Play()
    assert_equal(True, actualValue, "Play书籍")


def test_bookread(BookID=None):
    """读书"""
    if BookID == None:
        BookID == MyData.UserData_dir["bookDetailInfo"]["BookID"]
    else:
        MyData.UserData_dir["bookDetailInfo"]["BookID"]=BookID
        print(MyData.UserData_dir["bookDetailInfo"])
        print(MyData.UserData_dir["bookDetailInfo"]["BookID"])
    myVisual = VisualBook()
    myVisual.bookLoad()
    # actualValue = myVisual.getReadBook_info(BookID)
    myVisual.bookRead()
    assert_equal(True, True, "阅读详情{0}".format(myVisual.ReadBook_info))
    sleep(5)


def pageTurn(index=None):
    """界面切换"""
    PageTurn1 = PageTurn()
    if index == None:
        PageTurn1.click_close()
        return True
    else:
        PageTurn1.Bottom_click(index)
    sleep(2)


def test_Creation():
    """创建书籍"""
    Community1 = Community()
    actualValueinto_workshop = Community1.into_workshop()
    assert_equal(actualValueinto_workshop, True, "进入工作室{0}")
    Creation1 = Creation()
    isCreation = Creation1.process_createNewBook()
    assert_equal(isCreation, True, "创建书籍")


def test_ChapterEdit(storyName):
    """编写小说"""
    myChapterEdit = ChapterEdit()
    actualValue = myChapterEdit.process_creationStoryFlow(storyName)
    assert_equal(actualValue, True, "创作小说{0}".format(myChapterEdit.ChapterEdit_info))
    sleep(5)


def test_chooseUGCBook(index_x=0, index_y=0):
    """选择UGC书籍"""
    myReadUGCBook = ReadUGCBook()
    myReadUGCBook.choosebook()


def test_ReadUGCBook(time=2):
    """短信小说阅读"""
    myReadUGCBook = ReadUGCBook()
    actualValue = myReadUGCBook.click_Read()
    myReadUGCBook.bookRead(time)
    assert_equal(True, True, "短信小说阅读".format(myReadUGCBook.ReadUGCBook_info))


def test_ChangeUseravatar():
    """更换个人信息背景角色"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.ChangeUseravatar()
    assert_equal(actualValue, True, "更换背景角色情况：{0}".format(myProfilemodule.Profilemodule_info))


def test_operationAchievement():
    """对成就进行操作"""
    myAchievementmodule = Achievementmodule()
    actualValue = myAchievementmodule.operationAchievememt()
    assert_equal(True, True, "进行操作的成就名字：{0}".format(myAchievementmodule.Achievementmodule_info["name"]))


def test_ChangeUseremoticons(expression):
    """更换背景角色表情"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.ChangeUseremoticons(expression)
    assert_equal(actualValue, True, "更换角色的表情：{0}".format((myProfilemodule.Profilemodule_info["emoticons"])))


def test_nameedit(name):
    """编辑名字"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.nameedit(name=name)
    assert_equal(actualValue, True, "编辑名字:{0}".format((myProfilemodule.Profilemodule_info["name"])))


def test_showAchievement():
    """成就展示"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.Change_showAchievement()
    assert_equal(actualValue, True, "成就展示变更的名字：{0}".format(myProfilemodule.Profilemodule_info["name"]))


def test_shop_buy_member():
    """订阅会员"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_member()
    assert_equal(actualValue, True, "用户的会员状态信息：{0}".format(myShopmodule.Shopmodule_info))


def test_shop_buy_ticket(num):
    """购买票卷"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_ticket(num)
    assert_equal(actualValue, True, "购买非双倍奖励的5票{0}".format(myShopmodule.Shopmodule_info))


def test_shop_buy_diamond(num):
    """购买钻石"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_diamond(num)
    assert_equal(actualValue, True, "购买非双倍奖励的20钻石{0}".format(myShopmodule.Shopmodule_info))
