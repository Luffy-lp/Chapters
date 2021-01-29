from airtest.core.api import *
from common.COM_findobject import FindObject
from common import COM_utilities
from common.COM_data import MyData
from common.COM_utilities import clock
from common.my_log import mylog
from pages.shop.shop import Shop


class BookRead(FindObject):
    isstopRead = True  # 阅读状态
    isbookLoad = False
    iserrTime = 0
    touchtime = 0
    _etime = 0
    ReadBook_info = {}
    getstoryoptionslist = {}
    ReadBook_info["storyoption"] = {}
    Story_cfg_chapter_dir = {}

    def __init__(self):
        FindObject.__init__(self)
        self.myShop = Shop()
        self._POS = COM_utilities.PosTurn([0.31, 0.55])

    def bookRead(self, bookid=None):
        """视觉小说阅读界面"""
        self.isstopRead = False
        self.Popuplist = []  # 清空之前的弹框列表
        self.ReadBook_info["异常次数"] = 0
        self.getReadBook_info(bookid)
        if self.poco("UIDialogue").wait(5).exists():
            if self.ReadBook_info["chatProgress"]==10001:
                self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励", waitTime=2,sleeptime=100)
            clock()
            sleep(1)
            print(int(MyData.UserData_dir["bookDetailInfo"]["BookID"]))
            print(int(self.ReadBook_info["chapterProgress"]))
            touch(self._POS)
            while (not self.isstopRead):
                print("点击次数{0}".format(self.touchtime))
                self.dialogueCourseJudge()  # 阅读过程判断对应章节显示的内容
        else:
            print("未检测到阅读界面")

    def getReadBook_info(self, BookID):
        """获取当前书籍信息"""
        if not MyData.UserData_dir["bookDetailInfo"]["BookID"]:
            MyData.UserData_dir["bookDetailInfo"]["BookID"] = BookID
            MyData.download_bookresource(MyData.UserData_dir["bookDetailInfo"]["BookID"])
        else:
            BookID = MyData.UserData_dir["bookDetailInfo"]["BookID"]
        readprogress = MyData.getreadprogress(BookID)  # 获取书籍进度
        print("readprogress", readprogress)
        chapterProgress = readprogress[BookID]["chapterProgress"]  # 获取章节进度
        print("chapterProgress", chapterProgress)
        chatProgress = readprogress[BookID]["chatProgress"]  # 获取到选项进度
        print("chatProgress", chatProgress)
        story_cfg_chapter = MyData.read_story_cfg_chapter(BookID, str(chapterProgress))  # 写入章节信息表
        print("story_cfg_chapter", story_cfg_chapter)
        # MyData.read_story_cfg_chapter(BookID, chapterProgress)  # 写入章节信息表
        self.ReadBook_info["chapterProgress"] = chapterProgress
        self.ReadBook_info["chat_num"] = story_cfg_chapter["length"] + 10000
        self.ReadBook_info["chatProgress"] = chatProgress
        self.ReadBook_info["BookID"] = BookID
        # self.ReadBook_info["BookName"]=MyData.UserData_dir["bookDetailInfo"]["BookName"]
        return self.ReadBook_info

    def dialogueCourseJudge(self):
        """对话处理"""
        achatProgress = str(self.ReadBook_info["chatProgress"])
        print("MyData.Story_cfg_chapter_dir", MyData.Story_cfg_chapter_dir)
        print("achatProgress", achatProgress)
        chat_type = MyData.Story_cfg_chapter_dir[achatProgress]["chat_type"]  # 当前选项chat_type值
        select_id = MyData.Story_cfg_chapter_dir[achatProgress]["select_id"]  # select_id值
        print("当前选项chat_type值", chat_type)
        print("当前选项select_id值", select_id)
        print("本章总页数:", self.ReadBook_info["chat_num"])
        print("记录选项进度:", achatProgress)
        self.chat_typeconf(chat_type, select_id)  # 处理特殊选择类型
        self.progressjudge(achatProgress)
        if int(achatProgress) == self.ReadBook_info["chat_num"]:
            self.dialogueEndPOP()  # 阅读结束弹框判断
    def chat_typeconf(self, chat_id, select_id):
        """选项判断"""
        if chat_id in MyData.chat_type_dir:
            description = MyData.chat_type_dir[chat_id][0]
            print("description", description)
            mylog.info("description")
            for val in range(1, len(MyData.chat_type_dir[chat_id])):
                clickname = MyData.chat_type_dir[chat_id][val]
                if type(clickname) == int:
                    sleep(clickname)
                else:
                    self.findClick_try(clickname, clickname, description=description, waitTime=2, sleeptime=2)
        if select_id == 0:
            touch(self._POS)
            sleep(0.2)
        else:
            if self.poco("UIChapterSelectList").child("Item").exists():  # "UISelectList")老版本
                Item0 = self.poco("UIChapterSelectList").child("Item")[0]
                self.findClick_childobject(Item0, description="点击选项")
            if self.find_try("UIQuickPayFrame", description="快捷购买", waitTime=0.2):
                self.myShop.quick_purchase()
        self.touchtime = self.touchtime + 1

    def progressjudge(self, achatProgress):
        readprogress = MyData.getreadprogress(self.ReadBook_info["BookID"])  # 获取当前进度
        self.ReadBook_info["chatProgress"] = readprogress[self.ReadBook_info["BookID"]]["chatProgress"]
        print("点击后进度：", self.ReadBook_info["chatProgress"])
        if achatProgress == str(self.ReadBook_info["chatProgress"]):
            self._etime = self._etime + 1
            if self._etime >= 2:
                self._etime = 0
                self.ReadBook_info["异常次数"] = self.ReadBook_info["异常次数"] + 1
                print("卡顿或异常次数：", self.ReadBook_info["异常次数"])
                if self.ReadBook_info["异常次数"] > 50:
                    print("卡顿或异常次数较多", self.ReadBook_info["异常次数"])
                    mylog.error("异常次数过多读书可能卡死")
                    log(Exception("异常次数过多读书可能卡死"))
                    raise Exception
                    return False
        else:
            print("正常点击")
            self._etime = 0

    def dialogueEndPOP(self):
        """章节尾弹框"""
        # self.poco.wait_for_any()
        if self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1):
            stoptime = str(clock("stop")) + "秒"
            self.ReadBook_info["阅读时长"] = stoptime
            while (self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1)):
                if self.poco("UIRewardPopup").wait(5).exists():
                    print("检测到有弹框，结束阅读")
                    if self.poco("UIRewardPopup").wait(2).exists():
                        print("弹框类型为奖励弹框")
                        self.findClick_try("RoleCard", "BtnGet", description="角色卡奖励", waitTime=0.5)
                        self.findClick_try("AdGroup", "BtnGet", description="付费用户章节尾奖励", waitTime=0.5)
                else:
                    print("未检测到任何弹框")
                self.findClick_try("UIChapterStar", "CloseBtn", description="阅读分享", waitTime=1)
                self.findClick_try("UIChapterContinue", "BtnGet", description="章节尾奖励", waitTime=0.5, sleeptime=2)
                self.findClick_try("UIChapterContinue", "ContinueBtn", description="章节尾弹框", waitTime=0.5, sleeptime=2)
                self.isstopRead = True
                self.ReadBook_info["点击次数"] = self.touchtime
                mylog.info("结束阅读")
                print("结束阅读")
            sleep(3)
            self.ReadBook_info["章节尾弹框详情"] = self.Popuplist
            self.ReadBook_info["阅读情况"] = "完成阅读"
            return True
    # def roleDressJudge(self):
    #     if self.find_try("UIOldSetName", description="老的角色名称设置", waitTime=0.1, tryTime=1):  # "UISetName"
    #         self.poco("InputField").click()
    #         text("RoleName")
    #         self.poco("ConfirmBtn").click(sleep_interval=0.2)
    #         self.poco("ConfirmBtn").click()
    #         # poco("UIQuickPayFrame")快速购买


BookRead1 = BookRead()
BookRead1.bookRead("10001")
# print(BookNewDetail1.ReadBook_info)
# BookNewDetail1.bookChoose("Weekly",index=0)
