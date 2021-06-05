from airtest.core.api import *
from poco.drivers.std import StdPocoAgent

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
    progress_info = {}
    getstoryoptionslist = {}
    Story_cfg_chapter_dir = {}
    option_record = {}
    BookRead_info = {}

    def __init__(self):
        FindObject.__init__(self)
        self.myShop = Shop()
        self._POS = COM_utilities.PosTurn([0.5, 0.6])
        self.StdPocoAgent1 = StdPocoAgent()

    def bookRead(self, bookid=None):
        """视觉小说阅读"""
        self.reset_read()
        if self.poco("UIDialogue").wait(5).exists():
            clock()
            self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励", waitTime=1, sleeptime=3)
            self.getbookprogress(bookid)
            sleep(1)
            while not self.isstopRead:
                self.dialogueCourseJudge()  # 阅读过程判断对应章节显示的内容
            return True
        else:
            print("结束阅读")
            self.BookRead_info["spendtime"] = str(clock("stop")) + "秒"
            return True

    def getbookprogress(self, BookID):
        """初始化当前书籍信息"""
        self.BookRead_info["result"] = True
        readprogress = MyData.getreadprogress_local(self.StdPocoAgent1)  # 拉取本地当前阅读进度
        MyData.read_story_cfg_chapter(BookID, str(readprogress["Item2"]))  # 拉取章节信息存Story_cfg_chapter_dir表
        self.progress_info["chatProgress"] = readprogress["Item3"]  # 更新本地当前阅读对话进度
        self.progress_info["chapterProgress"] = readprogress["Item2"]  # 更新本地当前阅读章节进度
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        self.updte_oldReadProgress()  # 保存老进度
        self.progress_info["chat_num"] = MyData.Story_cfg_chapter_dir["length"] + 10000  # 当前章节对话总数
        self.progress_info["BookID"] = BookID
        print("阅读书籍:", BookID)
        print("章节进度:", self.progress_info["chapterProgress"])
        print("对话总数:", self.progress_info["chat_num"])
        print("对话进度:", self.progress_info["chatProgress"])

        return self.progress_info

    def dialogueCourseJudge(self):
        """对话处理"""
        print("==================================================")
        clock()
        self.updte_oldReadProgress()  # 保存老进度
        self.precondition()  # 转场前置判断
        self.resource_judgment()  # 对话资源判断
        self.chat_typeconf()  # 对话处理
        sleep(0.2)
        self.updte_readprogress()  # 更新当前书籍阅读进度
        self.progressjudge()  # 书籍阅读进度是否异常判断
        self.dialogueEndPOP()  # 阅读结束弹框判断
        print("花费时间：", clock("stop"))
        print("==================================================")

    def precondition(self):
        """前置处理"""
        if self.option_record["scene_bg_id"] != self.progress_info["option_info"]["scene_bg_id"]:
            print("转场等待")
            sleep(1.5)
        if self.progress_info["option_info"]["is_need_around"] == 1:
            print("场景环绕等待")
            sleep(5.5)
        self.option_record["scene_bg_id"] = self.progress_info["option_info"]["scene_bg_id"]  # 背景

    def updte_readprogress(self):
        """更新当前书籍阅读进度"""
        readprogress = MyData.getreadprogress_local(self.StdPocoAgent1)  # 拉取本地当前阅读进度
        self.progress_info["chatProgress"] = readprogress["Item3"]  # 更新本地当前阅读对话进度
        self.progress_info["chapterProgress"] = readprogress["Item2"]  # 更新本地当前阅读章节进度
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        print("更新章节进度:", self.progress_info["chapterProgress"])
        print("更新对话进度:", self.progress_info["chatProgress"])

    def updte_oldReadProgress(self):
        """记录老的书籍阅读进度"""
        self.option_record["chatProgress"] = str(self.progress_info["chatProgress"])  # 记录当前进度
        print("之前的进度:", self.option_record["chatProgress"])

    def resource_judgment(self):
        """选项资源判断"""
        achatProgress = str(self.option_record["chatProgress"])
        pos_id = self.progress_info["option_info"]["pos_id"]  # 当前选项pos_id值
        chat_type = int(self.progress_info["option_info"]["chat_type"])
        filename_head = str(self.progress_info["chapterProgress"]) + "_" + achatProgress

        if self.poco("SceneBG").wait(2).exists():
            try:
                content = self.progress_info["option_info"]["content"]  # 选项配置
                if content:
                    print("content:", content)
                else:
                    if chat_type != 10:
                        self.BookRead_info["result"] = False
                        print("内容为空:", content)
                        dec = filename_head + "content"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="内容为空"), desc="内容为空",
                            snapshot=True)
            except:
                print("无content配置")
            try:
                if self.poco("SceneBG").wait(1).attr("SpriteRenderer"):
                    print("SceneBG资源正常")
                else:
                    self.BookRead_info[achatProgress] = "SceneBG的SpriteRenderer为flase"
                    self.BookRead_info["result"] = False
                    dec = filename_head + "背景"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="SceneBG的SpriteRenderer为flase"), desc="SceneBG的SpriteRenderer为flase",
                        snapshot=True)
            except:
                if self.poco("SceneBG").offspring("Background").wait(1).get_SpriteRenderer():
                    print("SceneBG资源正常")
                else:
                    self.BookRead_info[achatProgress] = "SceneBG的SpriteRenderer丢失"
                    self.BookRead_info["result"] = False
                    dec = filename_head + "SceneBG"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="SceneBG的SpriteRenderer丢失"), desc="SceneBG的SpriteRenderer丢失",
                        snapshot=True)
        else:
            self.BookRead_info[achatProgress] = "SceneBG的enable为flase"
            self.BookRead_info["result"] = False
            dec = filename_head + "SceneBG"
            myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            log(ResourceError(errorMessage="{0}SceneBG的enable为flase".format(achatProgress)),
                desc="{0}SceneBG的enable为flase".format(achatProgress),
                snapshot=True)
        if self.StdPocoAgent1.get_Music():
            print("获取音乐资源挂载正常")
        else:
            print("获取音乐资源挂载异常")
        if chat_type == 2:
            print("旁白不检测资源chat_type：", chat_type)
            return True
        if chat_type == 8 or chat_type == 15 or chat_type == 16 or chat_type == 19 or chat_type == 26 or chat_type == 29:
            print("打电话类型不检测资源chat_type：", chat_type)
            return True
        if chat_type == 7 or chat_type == 23:
            print("短信类型不检测资源chat_type：", chat_type)
            return True
        if chat_type == 3:
            print("角色名称设置不检测资源chat_type：", chat_type)
            return True
        if chat_type == 4 or chat_type == 5 or chat_type == 6 or chat_type == 9:
            print("旧版换装chat_type：", chat_type)
            return True
        if chat_type == 10:
            print("新版换装资源检测")
            try:
                list = self.poco("Viewport").offspring("Cloth").wait(2)
                print("list", list)
                for key, vlus in enumerate(list):
                    if vlus.attr("texture"):
                        print("第{0}个肤色Cloth图片资源为：{1}".format(key, vlus.attr("texture")))
                    else:
                        print("角色装扮Cloth图片资源异常")
                        self.BookRead_info[achatProgress] = "角色装扮Cloth图片资源异常"
                        self.BookRead_info["result"] = False
                        dec = filename_head + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                            desc="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key), snapshot=True)
            except ResourceError as e:
                print("角色装扮Cloth图片资源异常")
                self.BookRead_info[achatProgress] = "角色装扮Cloth图片资源异常"
                self.BookRead_info["result"] = False
                dec = filename_head + "Cloth"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                    desc="{0}第{1}角色装扮图片资源异常".format(achatProgress, key), snapshot=True)
            return
        if pos_id == 2:
            try:
                NormalSayRoleLeft_bool = self.poco("NormalSayRoleLeft").offspring("Cloth").attr(
                    "SpriteRenderer")
                print("左侧人物Cloth检测")
                if NormalSayRoleLeft_bool:
                    print("NormalSayRoleLeft->Clotht资源正常")
                else:
                    self.BookRead_info[achatProgress] = "NormalSayRoleLeft->Cloth的资源丢失"
                    self.BookRead_info["result"] = False
                    log(ResourceError(errorMessage="NormalSayRoleLeft->Cloth的资源丢失"),
                        desc="NormalSayRoleLeft->Cloth的资源丢失", snapshot=True)
            except:
                self.BookRead_info[achatProgress] = "NormalSayRoleLeft->SpriteRenderer获取失败"
                self.BookRead_info["result"] = False
                dec = filename_head + "Cloth"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="NormalSayRoleLeft->SpriteRenderer获取失败"),
                    desc="NormalSayRoleLeft->SpriteRenderer获取失败", snapshot=True)

        elif pos_id == 1:
            if self.poco("NormalSayRoleRight").offspring("Body").wait(0.5).exists():
                try:
                    NormalSayRoleRight = self.poco("NormalSayRoleRight").offspring("Cloth").wait(2).attr(
                        "SpriteRenderer")
                    print("右侧1人物Cloth检测")
                    if NormalSayRoleRight:
                        print("NormalSayRoleRight资源正常")
                    else:
                        self.BookRead_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer为flase"
                        self.BookRead_info["result"] = False
                        dec = filename_head + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer为flase"),
                            desc="NormalSayRoleRight->SpriteRenderer为flase",
                            snapshot=True)
                except:
                    self.BookRead_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer丢失"
                    self.BookRead_info["result"] = False
                    dec = filename_head + "Cloth"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer丢失"),
                        desc="NormalSayRoleRight->SpriteRenderer丢失",
                        snapshot=True)

            else:
                # self.poco("NormalSayRoleRight2").offspring("Body").wait(0.2).exists():
                try:
                    NormalSayRoleRight2 = self.poco("NormalSayRoleRight2").offspring("Cloth").wait(2).attr(
                        "SpriteRenderer")
                    print("右侧2人物Cloth检测")
                    if NormalSayRoleRight2:
                        print("NormalSayRoleRight2资源正常")
                    else:
                        self.BookRead_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer为flase"
                        self.BookRead_info["result"] = False
                        dec = filename_head + "Cloth"
                        myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                        log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer为flase"),
                            desc="NormalSayRoleRight->SpriteRenderer为flase",
                            snapshot=True)
                except:
                    self.BookRead_info[achatProgress] = "NormalSayRoleRight->SpriteRenderer丢失"
                    self.BookRead_info["result"] = False
                    dec = filename_head + "Cloth"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    log(ResourceError(errorMessage="NormalSayRoleRight->SpriteRenderer丢失"),
                        desc="NormalSayRoleRight->SpriteRenderer丢失",
                        snapshot=True)

    def chat_typeconf(self):
        """选项判断"""
        chat_id = self.progress_info["option_info"]["chat_type"]  # 当前选项chat_type值
        select_id = self.progress_info["option_info"]["select_id"]  # select_id值
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
        elif select_id == 0:
            touch(self._POS)
            # print("普通点击")
        else:
            if self.poco("UIChapterSelectList").child("Item").exists():  # "UISelectList")老版本
                Item0 = self.poco("UIChapterSelectList").child("Item")[0]
                self.findClick_childobject(Item0, description="点击选项")
            if self.find_try("UIQuickPayFrame", description="快捷购买", waitTime=0.2):
                self.myShop.quick_purchase()
        self.touchtime = self.touchtime + 1

    def progressjudge(self):
        """进度异常判断"""
        time=3
        while time>0:
            time-=1
            if self.option_record["chatProgress"] == str(self.progress_info["chatProgress"]):
                print("进度相同容错处理")
                sleep(0.3)
                self.updte_readprogress()
            else:
                return True
        if self._etime >= 2:
            self._etime = 0
            self.BookRead_info["Jank"] = self.BookRead_info["Jank"] + 1
            VisualRead: dict = MyData.newPoP_dir["VisualRead"]
            for k, v in VisualRead.items():
                self.findClick_try(k, v)
            print("卡顿或异常次数：", self.BookRead_info["Jank"])
            if self.BookRead_info["Jank"] > 50:
                print("卡顿或异常次数较多", self.BookRead_info["Jank"])
                mylog.error("异常次数过多或检查启用新存档是否失败")
                log(Exception("异常次数过多或检查启用新存档是否失败"), snapshot=True)
                raise Exception
                return False
        else:
            self._etime = self._etime + 1
    def reset_read(self):
        """阅读参数初始化"""
        self.isstopRead = False
        self.Popuplist = []  # 清空之前的弹框列表
        self.BookRead_info["Jank"] = 0
        self.touchtime = 0
        self.progress_info["results"] = True
        self.progress_info["storyoption"] = {}
        self.option_record["scene_bg_id"] = 0
        self._etime = 0
    def dialogueEndPOP(self):
        """章节尾弹框"""
        # self.poco.wait_for_any()
        if int(self.option_record["chatProgress"]) == self.progress_info["chat_num"]:
            if self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1):
                while (self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1)):
                    AlterTxt = MyData.newPoP_dir["dialogueEndPOP"]
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
                    self.findClick_try("UIChapterContinue", "ContinueBtn", description="章节尾弹框", waitTime=0.5,
                                       sleeptime=2)
                    self.isstopRead = True
                    self.BookRead_info["clicks"] = self.touchtime
                sleep(3)
                self.BookRead_info["Pop-up"] = self.Popuplist
                return True
