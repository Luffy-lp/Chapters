from airtest.core.api import *
from common.COM_findobject import FindObject
from common import COM_utilities
from date.Chapters_data import MyData
from common.COM_utilities import clock, myscreenshot
from common.my_log import mylog
from pages.shop.shop import Shop
from common.COM_Error import ResourceError
from common.COM_path import *


class BookRead(FindObject):
    isstopRead = True  # 阅读状态
    isbookLoad = False
    iserrTime = 0
    touchtime = 0
    _etime = 0
    ReadBook_info = {}
    getstoryoptionslist = {}
    ReadBook_info["storyoption"] = {}
    ReadBook_info["resource"] = True
    Story_cfg_chapter_dir = {}

    def __init__(self):
        FindObject.__init__(self)
        self.myShop = Shop()
        self._POS = COM_utilities.PosTurn([0.5, 0.6])

    def bookRead(self, bookid=None):
        """视觉小说阅读"""
        self.isstopRead = False
        self.Popuplist = []  # 清空之前的弹框列表
        self.ReadBook_info["卡顿次数"] = 0
        if self.poco("UIDialogue").wait(5).exists():
            self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励", waitTime=2, sleeptime=3)
            # if self.ReadBook_info["chatProgress"] == 10001:
            self.getReadBook_info(bookid)
            clock()
            sleep(1)
            # touch(self._POS)
            while (not self.isstopRead):
                print("点击次数{0}".format(self.touchtime))
                self.dialogueCourseJudge()  # 阅读过程判断对应章节显示的内容
            return True
        else:
            print("结束阅读")
            return True

    def getReadBook_info(self, BookID):
        """获取当前书籍信息"""
        readprogress = MyData.getreadprogress(BookID)  # 获取书籍进度
        print("readprogress", readprogress[BookID])
        chapterProgress = readprogress[BookID]["chapterProgress"]  # 获取章节进度
        print("chapterProgress", chapterProgress)
        chatProgress = readprogress[BookID]["chatProgress"]  # 获取到选项进度
        print("chatProgress", chatProgress)
        story_cfg_chapter = MyData.read_story_cfg_chapter(BookID, str(chapterProgress))  # 写入章节信息表
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
        # print("MyData.Story_cfg_chapter_dir", MyData.Story_cfg_chapter_dir)
        option_info = MyData.Story_cfg_chapter_dir[achatProgress]  # 选项配置
        chat_type = option_info["chat_type"]  # 当前选项chat_type值
        select_id = option_info["select_id"]  # select_id值
        print("当前选项chat_type值", chat_type)
        print("当前选项select_id值", select_id)
        print("本章总页数:", self.ReadBook_info["chat_num"])
        print("记录选项进度:", achatProgress)
        self.resource_judgment(option_info, achatProgress)  # 选项资源判断
        self.chat_typeconf(chat_type, select_id)  # 根据情况处理点击
        if int(achatProgress) == self.ReadBook_info["chat_num"]:
            self.dialogueEndPOP()  # 阅读结束弹框判断
        self.progressjudge(achatProgress)  # 进度异常判断

    def resource_judgment(self, option_info, achatProgress):
        """选项资源判断"""
        pos_id = option_info["pos_id"]  # 当前选项pos_id值
        chat_type = int(option_info["chat_type"])
        if self.poco("SceneBG").wait(2).exists():
            try:
                if self.poco("SceneBG").wait(2).attr("SpriteRenderer"):
                    print("SceneBG资源正常")
                else:
                    self.ReadBook_info[achatProgress] = "SceneBG的SpriteRenderer为flase"
                    self.ReadBook_info["resource"] = False
                    dec = achatProgress + "背景"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="SceneBG的SpriteRenderer为flase"), desc="SceneBG的SpriteRenderer为flase",
                        snapshot=True)
            except ResourceError as e:
                self.ReadBook_info[achatProgress] = "SceneBG的SpriteRenderer丢失"
                self.ReadBook_info["resource"] = False
                dec = achatProgress + "SceneBG"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="SceneBG的SpriteRenderer丢失"), desc="SceneBG的SpriteRenderer丢失", snapshot=True)
        else:
            self.ReadBook_info[achatProgress] = "SceneBG的enable为flase"
            self.ReadBook_info["resource"] = False
            dec = achatProgress + "SceneBG"
            myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            log(ResourceError(errorMessage="{0}SceneBG的enable为flase".format(achatProgress)),
                desc="{0}SceneBG的enable为flase".format(achatProgress),
                snapshot=True)
        if chat_type == 4 or chat_type == 5 or chat_type == 6 or chat_type == 9 or chat_type == 10:
            print("检测角色换装资源")
            try:
                list = self.poco("Viewport").offspring("Cloth").wait(2)
                for key, vlus in enumerate(list):
                    if vlus.attr("texture"):
                        print("第{0}个肤色Cloth图片资源为：{1}".format(key, vlus.attr("texture")))
                    else:
                        print("角色装扮Cloth图片资源异常")
                        self.ReadBook_info[achatProgress] = "角色装扮Cloth图片资源异常"
                        self.ReadBook_info["resource"] = False
                        dec = achatProgress + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                            desc="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key), snapshot=True)
            except ResourceError as e:
                print("角色装扮Cloth图片资源异常")
                self.ReadBook_info[achatProgress] = "角色装扮Cloth图片资源异常"
                self.ReadBook_info["resource"] = False
                dec = achatProgress + "Cloth"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                    desc="{0}第{1}角色装扮图片资源异常".format(achatProgress, key), snapshot=True)
        elif pos_id == 2:
            try:
                NormalSayRoleLeft_bool = self.poco("NormalSayRoleLeft").offspring("Cloth").attr(
                    "SpriteRenderer")
                if NormalSayRoleLeft_bool == True:
                    print("NormalSayRoleLeft->Clotht资源正常")
                else:
                    self.ReadBook_info[achatProgress] = "NormalSayRoleLeft->Cloth的资源丢失"
                    self.ReadBook_info["resource"] = False
                    log(ResourceError(errorMessage="NormalSayRoleLeft->Cloth的资源丢失"),
                        desc="NormalSayRoleLeft->Cloth的资源丢失", snapshot=True)
            except:
                self.ReadBook_info[achatProgress] = "NormalSayRoleLeft->SpriteRenderer获取失败"
                self.ReadBook_info["resource"] = False
                dec = achatProgress + "Cloth"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="NormalSayRoleLeft->SpriteRenderer获取失败"),
                    desc="NormalSayRoleLeft->SpriteRenderer获取失败", snapshot=True)

        elif pos_id == 1:
            if self.poco("NormalSayRoleRight").offspring("Body").wait(0.2).exists():
                try:
                    NormalSayRoleRight = self.poco("NormalSayRoleRight").offspring("Cloth").wait(2).attr(
                        "SpriteRenderer")
                    if NormalSayRoleRight:
                        print("NormalSayRoleRight资源正常")
                    else:
                        self.ReadBook_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer为flase"
                        self.ReadBook_info["resource"] = False
                        dec = achatProgress + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer为flase"),
                            desc="NormalSayRoleRight->SpriteRenderer为flase",
                            snapshot=True)
                except:
                    self.ReadBook_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer丢失"
                    self.ReadBook_info["resource"] = False
                    dec = achatProgress + "Cloth"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer丢失"),
                        desc="NormalSayRoleRight->SpriteRenderer丢失",
                        snapshot=True)

            if self.poco("NormalSayRoleRight2").offspring("Body").wait(0.2).exists():
                try:
                    NormalSayRoleRight2 = self.poco("NormalSayRoleRight2").offspring("Cloth").wait(2).attr(
                        "SpriteRenderer")
                    if NormalSayRoleRight2:
                        print("右2角色Cloth资源正常")
                    else:
                        self.ReadBook_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer为flase"
                        self.ReadBook_info["resource"] = False
                        dec = achatProgress + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer为flase"),
                            desc="NormalSayRoleRight->SpriteRenderer为flase",
                            snapshot=True)
                except:
                    self.ReadBook_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer丢失"
                    self.ReadBook_info["resource"] = False
                    dec = achatProgress + "Cloth"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer丢失"),
                        desc="NormalSayRoleRight->SpriteRenderer丢失",
                        snapshot=True)

    def chat_typeconf(self, chat_id, select_id):
        """选项判断"""
        if chat_id in MyData.chat_type_dir:
            description = MyData.chat_type_dir[chat_id][0]
            print("description", description)
            mylog.info("description")
            print("chat_id", chat_id)
            for val in range(1, len(MyData.chat_type_dir[chat_id])):
                clickname = MyData.chat_type_dir[chat_id][val]
                if type(clickname) == int:
                    sleep(clickname)
                else:
                    self.findClick_try(clickname, clickname, description=description, waitTime=2, sleeptime=2)
        if select_id == 0:
            touch(self._POS)
            print("普通点击")
        else:
            if self.poco("UIChapterSelectList").child("Item").exists():  # "UISelectList")老版本
                Item0 = self.poco("UIChapterSelectList").child("Item")[0]
                self.findClick_childobject(Item0, description="点击选项")
            if self.find_try("UIQuickPayFrame", description="快捷购买", waitTime=0.2):
                self.myShop.quick_purchase()
        self.touchtime = self.touchtime + 1

    def progressjudge(self, achatProgress):
        """进度异常判断"""
        readprogress = MyData.getreadprogress(self.ReadBook_info["BookID"])  # 获取当前进度
        self.ReadBook_info["chatProgress"] = readprogress[self.ReadBook_info["BookID"]]["chatProgress"]
        print("点击后进度：", self.ReadBook_info["chatProgress"])
        if achatProgress == str(self.ReadBook_info["chatProgress"]):
            sleep(2)
            readprogress = MyData.getreadprogress(self.ReadBook_info["BookID"])  # 获取当前进度
            self.ReadBook_info["chatProgress"] = readprogress[self.ReadBook_info["BookID"]]["chatProgress"]
            self._etime = self._etime + 1
            if self._etime >= 2:
                self._etime = 0
                self.ReadBook_info["卡顿次数"] = self.ReadBook_info["卡顿次数"] + 1
                print("卡顿或异常次数：", self.ReadBook_info["卡顿次数"])
                if self.ReadBook_info["卡顿次数"] > 50:
                    print("卡顿或异常次数较多", self.ReadBook_info["卡顿次数"])
                    mylog.error("异常次数过多或检查启用新存档是否失败")
                    log(Exception("异常次数过多或检查启用新存档是否失败"), snapshot=True)
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
                    print("一级弹框已处理")
                self.findClick_try("UIChapterStar", "CloseBtn", description="阅读分享", waitTime=1)
                self.findClick_try("UIChapterContinue", "BtnGet", description="章节尾奖励", waitTime=0.5, sleeptime=2)
                self.findClick_try("UIChapterContinue", "ContinueBtn", description="章节尾弹框", waitTime=0.5, sleeptime=2)
                self.isstopRead = True
                self.ReadBook_info["点击次数"] = self.touchtime
            sleep(3)
            self.ReadBook_info["阅读弹框"] = self.Popuplist
            self.ReadBook_info["阅读情况"] = "完成阅读"
            return True
