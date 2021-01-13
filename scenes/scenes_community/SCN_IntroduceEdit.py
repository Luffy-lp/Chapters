from airtest.core.api import *
from common.COM_findobject import CommonPoco
from common import COM_utilities
from common.COM_data import MyData
from common.COM_utilities import *
# TODO:图像选择存在兼容性问题
import time


class IntroduceEdit(CommonPoco):
    """简介编辑界面"""

    def __init__(self):
        CommonPoco.__init__(self)

    def chapterEdit(self):
        self.find_object("LuaUIIntroduceEdit", description="简介编辑界面", waitTime=3)

    def topBar(self, type):
        """顶部按钮 Preview，Release，Back  ("TopBar")"""
        if type == "Preview":
            self.click_object("BtnPreview", description="浏览按钮")
        if type == "Release":
            self.click_object("BtnRelease", description="审核按钮")
            self.releaseConfirm()
        if type == "Back":
            self.click_object("BtnBack", description="返回按钮")

    def releaseConfirm(self):
        """审核条款确认"""
        if self.find_object("LuaUIReleaseConfirmDlg", description="审核确认界面"):
            self.findClick_childobject(self.poco("Term").child("BtnCheck"), "游戏条款")
            self.findClick_childobject(self.poco("Age").child("BtnCheck"), "年龄确认")
            self.findClick_childobject(self.poco("Code").child("BtnCheck"), "行为规范", sleeptime=1)
            self.findClick_childobject(self.poco("Bottom").child("BtnOK"), "提交审核", sleeptime=2)
        if self.find_try("UIEnjoyChapter", description="是否首次审核"):
            self.click_object("LaterBtn", description="再说")  # ("RateBtn")

    def editDesc(self):
        """编辑描述文本"""
        localtime = time.asctime(time.localtime(time.time()))
        self.click_object("InputDescAndroid", description="描述文本输入框", waitTime=1, sleeptime=1)
        # for i in range(10):
        #     keyevent("67")
        text(localtime)
        if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
            pass
        else:
            self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                   description="点击提交按钮")

    def editTitle(self, bookname):
        """编辑标题文本"""
        self.click_object("InputTitleAndroid", description="标题文本输入框", waitTime=1, sleeptime=1)
        # for i in range(10):
        #     keyevent("67")
        text(bookname)
        # poco("TxtCategory")
        # pos1600= (0.448, 0.232)
        # pos1080=(0.431, 0.168)
        if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
            pass
        else:
            self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                   description="点击提交按钮")

    def editCategory(self):
        """选择类型"""
        # poco("TxtCategory")
        self.click_object("BtnCategory", description="选择类型")
        try:
            categoryItemPOCO = \
                self.poco("LuaUIReCategory").child("Items").child("Viewport").child("Content").child("Item(Clone)")[
                    2].wait(
                    5)
        except:
            self.log.error("等待-【{}】-元素可见超时".format("选择类型"))
        self.findClick_childobject(categoryItemPOCO, description="选择类型")

    def editCoverIcon(self):
        """选择封面"""
        if self.find_object("CoverIcon", description="是否无封面"):
            self.findClick_childobject(self.poco("LuaUIIntroduceEdit").child("Cover"), description="选择封面",
                                       waitTime=2, sleeptime=2)
            POCO = self.poco("Options").child("Button(Clone)")[0]
            self.findClick_childobject(POCO, description="从我的图库中", sleeptime=2)
            sleep(2)
            if self.android_tryfind("com.android.packageinstaller:id/permission_allow_button", description="检查开启图库权限",
                                    waitTime=3):
                self.android_findClick("com.android.packageinstaller:id/permission_allow_button",
                                       "com.android.packageinstaller:id/permission_allow_button",
                                       description="检查开启图库权限", waitTime=1
                                       )
            if MyData.ConfData_dir["ADBdevice"] == "127.0.0.1:7555":
                print("mumu模拟器类型")
                self.mumu()
            else:
                self.android_findClick("com.google.android.apps.photos:id/image",
                                       "com.google.android.apps.photos:id/image",
                                       description="选择图片",
                                       waitTime=3)
                pos = self.androidpoco("android.view.ViewGroup")[0].child(
                    "com.google.android.apps.photos:id/title").wait(5).get_position()
                pos[1] = pos[1] + 0.1
                # print("dddddddd:",pos)
                touch(PosTurn(pos))
                print("确认图片")
                self.android_findClick("com.google.android.apps.photos:id/photos_photoeditor_fragments_editor3_save",
                                       "com.google.android.apps.photos:id/photos_photoeditor_fragments_editor3_save",
                                       description="完成保存",
                                       waitTime=5)
            self.mysleep(5)
            COM_utilities.clock()
            while self.find_try("LoadingFlower", description="判断加载是否完成"):
                print("图片loading中")
                sleep(1)
                mytime = float(COM_utilities.clock("stop"))
                if mytime > 30:
                    print("图片选择失败，请检查权限问题")
                    log(Exception("图片选择失败，请检查权限问题"))
                    raise Exception("图片选择失败，请检查权限问题")

        else:
            print("已存在封面，跳过封面选择")

    def mumu(self):
        # touch(COM_utilities.PosTurn((0.748, 0.527)))
        if self.android_tryfind("com.android.gallery3d:id/gl_root_view", description="选择图片", waitTime=5):
            self.android_findClick("com.android.gallery3d:id/gl_root_view",
                                   "com.android.gallery3d:id/gl_root_view",
                                   description="选择图片",
                                   waitTime=3)
        if self.android_tryfind("com.android.gallery3d:id/gl_root_view", description="选择图片", waitTime=5):
            self.android_findClick("com.android.gallery3d:id/gl_root_view",
                                   "com.android.gallery3d:id/gl_root_view",
                                   description="选择图片",
                                   waitTime=3)
        self.mysleep(5)
        if self.android_tryfind("com.android.gallery3d:id/gl_root_view", description="选择图片", waitTime=1):
            self.android_findClick("com.android.gallery3d:id/gl_root_view",
                                   "com.android.gallery3d:id/gl_root_view",
                                   description="选择图片",
                                   waitTime=2)
        self.android_findClick("com.android.gallery3d:id/filtershow_done",
                               "com.android.gallery3d:id/filtershow_done",
                               description="点击保存",
                               waitTime=5)

        # pos = COM_utilities.PosTurn((0.1, 0.1))
        # print("选择第一个图集")
        # touch(pos)
        # sleep(2)
        # pos = COM_utilities.PosTurn((0.17, 0.17))
        # print("选择第一个图片")
        # touch(pos)
        # sleep(2)
        # pos = COM_utilities.PosTurn((0.5, 0.5))
        # touch(pos)
        # sleep(2)
        # pos = COM_utilities.PosTurn((0.05, 0.05))
        # print("尝试点击上方保存按钮")
        # touch(pos)

    def mainprocess(self, bookname):
        """书籍简介编辑以及审核流程"""
        self.editTitle(bookname)
        self.editDesc()
        self.editCategory()
        self.editCoverIcon()
        self.topBar("Release")
        # if chapters_self.find_object(self.poco,"CenterBtn",description="未审核通过按钮"):#当存在数字不够的i情况
        #     chapters_self.click_object("CenterBtn", description="不审核")
        #     self.topBar("Back")


