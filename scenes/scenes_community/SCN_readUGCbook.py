from airtest.core.api import *
from common.COM_findobject import FindObject
from common import COM_utilities


class ReadUGCBook(FindObject):
    touchTime = 0
    ReadUGCBook_info = {}
    Chattime = 0

    def __init__(self):
        FindObject.__init__(self)
        self._POS = COM_utilities.PosTurn([0.5, 0.9])

    def choosebook(self, index_x=0, index_y=0):
        """选择书籍"""
        index_x = int(index_x)
        index_y = int(index_y)
        object_x = self.poco("BookItems(Clone)")[index_x].child("BooItem")[index_y]  # 选择书籍
        objectBook = object_x.child("RawImage")  # 选择第几个书籍
        BookName = object_x.child("BookName").get_TMPtext()
        self.ReadUGCBook_info["BookName"] = BookName
        print(self.ReadUGCBook_info["BookName"])
        self.findClick_childobject(objectBook, description="UGC书籍封面", sleeptime=2)
        return self.ReadUGCBook_info

    def click_Read(self):
        Readobject = self.poco("LuaUIStoryBook").child("Content").child("Read")
        self.findClick_childobject(Readobject, description="Read", waitTime=2, tryTime=2)

    def bookRead(self, Chattime):
        """视觉小说阅读界面"""
        Chattime = int(Chattime)
        self.ReadUGCBook_info["errorTime"] = 0
        self.Chattime = Chattime
        if self.poco("LuaUIChatBookRead").wait(5).exists():
            self.isstopRead = False
            while self.Chattime > 0:
                touch(self._POS)
                self.touchTime = self.touchTime + 1
                print("点击次数：", self.touchTime)
                self.StoryEndAd()
        else:
            print("未检测到UGC阅读界面")

    def StoryEndAd(self):
        """章节尾检测"""
        if self.find_try("Options", description="结束菜单", waitTime=0.3):
            touch(self._POS)
            self.Chattime = self.Chattime - 1
            if self.Chattime <= 0:
                BackObject = self.poco("OptionItem(Clone)").child("Options").child("Center").child("Back")
                self.findClick_childobject(BackObject, description="返回到主界面")
                return True
            if self.find_try("UIChatStoryEndAd", description="章节尾广告"):
                self.click_object("BtnUnlock", description="选择使用票")  # poco("BtnAD")选择看广告
                self.click_object("Read", description="阅读")  # poco("BtnAD")选择看广告
            self.dialogueEndPOP()
            self.findClick_try("Read", "Read", description="阅读按钮")
            self.findClick_try("BtnRestart", "BtnRestart", description="返回到章节头")
            print("Chattime:", self.Chattime)
            self.ReadUGCBook_info["阅读剩余次数"] = self.Chattime
            self.ReadUGCBook_info["点击次数"] = self.touchTime
            return True

    def dialogueEndPOP(self):
        """章节尾弹框"""
        # self.poco.wait_for_any()
        touch(self._POS)
        self.findClick_try("UIEnjoyChapter", "LaterBtn", description="章节尾Enjoy弹框", waitTime=1, sleeptime=1)
        if self.find_try("UISupportVote", description="章节尾Support弹框", waitTime=1):
            BackObject = self.poco("UISupportVote").child("Bottom").child("Back").child("Image").wait(2)
            self.findClick_childobject(BackObject, description="Mybe Later", waitTime=0.5)

    def mainprocess(self, index_x=0, index_y=0, time=2):
        """短信小说阅读流程"""
        self.choosebook(index_x, index_y)
        self.click_Read()
        self.bookRead(time)
        return True
