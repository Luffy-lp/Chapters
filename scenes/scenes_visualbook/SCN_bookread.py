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
    NormalSayRoleRight=None
    old_RoleRight_role_id=None
    def __init__(self):
        FindObject.__init__(self)
        self.myShop = Shop()
        self._POS = COM_utilities.PosTurn([0.5, 0.6])
        self.StdPocoAgent1 = StdPocoAgent()

    def bookRead(self, bookid=None, chapterProgress=None):
        """视觉小说阅读"""
        self.reset_read()
        if self.poco("UIDialogue").wait(5).exists():
            clock()
            self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励", waitTime=1, sleeptime=3)
            self.getbookprogress(bookid, chapterProgress)
            sleep(1)
            while not self.isstopRead:
                self.dialogueCourseJudge()  # 阅读过程判断对应章节显示的内容
            return True
        else:
            print("结束阅读")
            self.BookRead_info["spendtime"] = str(clock("stop")) + "秒"
            return True

    def getbookprogress(self, BookID, chapterProgress):
        """初始化当前书籍信息"""
        self.BookRead_info["result"] = True
        readprogress = MyData.getreadprogress_local(self.StdPocoAgent1)  # 拉取本地当前阅读进度
        print("readprogress", readprogress)
        self.progress_info["chapterProgress"] = chapterProgress
        MyData.read_story_cfg_chapter(BookID,
                                      str(self.progress_info["chapterProgress"]))  # 拉取章节信息存Story_cfg_chapter_dir表
        self.progress_info["chatProgress"] = readprogress  # 更新本地当前阅读对话进度
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
        self.progress_info["chatProgress"] = readprogress
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        print("更新章节进度:", self.progress_info["chapterProgress"])
        print("更新对话进度:", self.progress_info["chatProgress"])

    def updte_oldReadProgress(self):
        """记录老的书籍阅读进度"""
        self.option_record["chatProgress"] = str(self.progress_info["chatProgress"])  # 记录当前进度
        print("之前的进度:", self.option_record["chatProgress"])

    def resource_result(self, result, findAtrr, des, filename_head):
        """检测结果"""
        if result is False:
            dec = filename_head + des
            self.BookRead_info["result"] = False
            self.BookRead_info[str(self.progress_info["chatProgress"])] = des + "->" + findAtrr + " is not find"
            myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
    def rightPos_judge(self):
        """判断右侧角色位置"""
        if self.NormalSayRoleRight == None:
            if self.poco("NormalSayRoleRight").offspring("Body").wait(0.5).exists():
                self.NormalSayRoleRight = True
                self.old_RoleRight_role_id = self.progress_info["option_info"]["role_id"]
            else:
                self.NormalSayRoleRight = False
                self.old_RoleRight_role_id = self.progress_info["option_info"]["role_id"]
        if self.progress_info["option_info"]["role_id"] is not self.old_RoleRight_role_id:
            self.NormalSayRoleRight = not self.NormalSayRoleRight
            self.old_RoleRight_role_id = self.progress_info["option_info"]["role_id"]
    def resource_judgment(self):
        """选项资源判断"""
        achatProgress = str(self.progress_info["chatProgress"])
        pos_id = self.progress_info["option_info"]["pos_id"]  # 当前选项pos_id值
        chat_type = int(self.progress_info["option_info"]["chat_type"])
        filename_head = str(self.progress_info["chapterProgress"]) + "_" + achatProgress
        if chat_type:
            # 背景检测
            SceneBGbool = self.assert_resource("Root", "SceneBG", "SpriteRenderer", "背景", 2, reportError=False)
            if SceneBGbool is False:
                # 特效类背景检测
                SceneBGbool1 = self.assert_resource("SceneBG", "Background", "SpriteRenderer", "特效类背景", waitTime=1)
                self.resource_result(SceneBGbool1, "SpriteRenderer", "特效类背景", filename_head=filename_head)
        try:
            if self.progress_info["option_info"]["show_id"]:  # 物品检测
                Goodsbool = self.assert_resource("UIShowGoods", "Img", findAttr="texture", description="物品", waitTime=2)
                self.resource_result(result=Goodsbool, findAtrr="texture", des="物品", filename_head=filename_head)
                return True
        except:
            print("不存在show_id")
        # if self.progress_info["option_info"]["show_id"]: #物品检测
        #     print("发现配置物品")
        #     try:
        #         texture=self.poco("UIShowGoods").offspring("Img").wait(2).attr("texture")
        #         if texture:
        #             print("物品texture", texture)
        #         else:
        #             self.BookRead_info["result"] = False
        #             dec = filename_head + "Goods"
        #             print("配置的物品{0}的texture为空", self.progress_info["option_info"]["show_id"])
        #             myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
        #             log(ResourceError(errorMessage="资源异常：物品的texture为空"), desc="物品的texture为空", snapshot=True)
        #     except:
        #         self.BookRead_info["result"] = False
        #         dec = filename_head + "Goods"
        #         print("配置的物品{0}未找到对应的texture",self.progress_info["option_info"]["show_id"])
        #         myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
        #         log(ResourceError(errorMessage="资源异常：未找到物品的texture"), desc="未找到物品的texture",snapshot=True)
        #     return True
        try:
            content = self.progress_info["option_info"]["content"]  # 普通文本
            mind = self.progress_info["option_info"]["mind"]  # 想象文本
            if content:
                # print("普通文本:", content)
                log("【资源检查】:普通文本->True",content)
            elif mind:
                # print("想象文本:", mind)
                log("【资源检查】:想象文本->True",mind)
            elif chat_type == 10:
                # print("换装类型无文本")
                log("【资源检查】:换装类型文本->True")
            else:
                self.BookRead_info["result"] = False
                print("内容为空:", content)
                dec = filename_head + "content"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="资源异常：内容为空"), desc="资源异常：内容为空",
                    snapshot=True)
        except:
            print("无content配置")
        if self.StdPocoAgent1.get_Music():
            log("【资源检查】:音乐资源->True")
        else:
            log(ResourceError(errorMessage="资源异常：音乐资源组件异常"), desc="资源异常：音乐资源组件异常",snapshot=True)
        if chat_type == 28:
            Sbool = self.assert_resource("UIChapterSelectRoleOver", "Cloth", "texture", "角色选择确认",waitTime=2)
            self.resource_result(Sbool,"texture","角色选择确认",filename_head=filename_head)
            return
            # if self.poco("UIChapterSelectRoleOver").offspring("Cloth").attr("texture"):
            #     print("角色选择确认chat_type",chat_type)
            # else:
            #     self.BookRead_info["result"] = False
            #     dec = filename_head + "Cloth"
            #     myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #     log(ResourceError(errorMessage="资源异常：角色选择确认资源异常"), desc="资源异常：角色选择确认资源异常",
            #         snapshot=True)
        if chat_type == 2:
            log("【资源检查】:旁白不检测资源")
            return True
        if chat_type == 8 or chat_type == 15 or chat_type == 16 or chat_type == 19 or chat_type == 26 or chat_type == 29:
            log("【资源检查】:电话类暂不检测")
            return True
        if chat_type == 7 or chat_type == 23:
            log("【资源检查】:短信类型不检测资源")
            return True
        if chat_type == 3:
            log("【资源检查】:角色名称设置不检测资源")
            return True
        if chat_type == 4 or chat_type == 5 or chat_type == 6 or chat_type == 9:
            log("【资源检查】:旧版换装不检测资源")
            return True
        if chat_type == 10:
            try:
                list = self.poco("Viewport").offspring("Content").children().wait(2)
                for key, vlus in enumerate(list):
                    name=vlus.get_name()
                    Clothbool = self.assert_resource(name,"Cloth","texture",description="角色装扮Cloth资源",waitTime=2)
                    self.resource_result(Clothbool, "texture", "角色装扮Cloth资源", filename_head=filename_head)
                    # if vlus.attr("texture"):
                    #     print("第{0}个肤色Cloth图片资源为：{1}".format(key, vlus.attr("texture")))
                    # else:
                    #     print("角色装扮Cloth图片资源异常")
                    #     self.BookRead_info[achatProgress] = "角色装扮Cloth图片资源异常"
                    #     self.BookRead_info["result"] = False
                    #     dec = filename_head + "Cloth"
                    #     myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                    #     log(ResourceError(errorMessage="资源异常：{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                    #         desc="{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key), snapshot=True)
            except ResourceError as e:
                print("角色装扮Cloth图片资源异常")
                self.BookRead_info[achatProgress] = "角色装扮Cloth图片资源异常"
                self.BookRead_info["result"] = False
                dec = filename_head + "Cloth"
                myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
                log(ResourceError(errorMessage="资源异常：{0}第{1}角色装扮Cloth图片资源异常".format(achatProgress, key)),
                    desc="{0}第{1}角色装扮图片资源异常".format(achatProgress, key), snapshot=True)
            return
        if pos_id == 2:
            RoleLeft_bool = self.assert_resource("NormalSayRoleLeft", "Cloth", "SpriteRenderer", "左侧人物的Cloth资源",waitTime=2)
            self.resource_result(RoleLeft_bool,"SpriteRenderer","左侧人物的Cloth资源",filename_head=filename_head)
            # try:
            #     NormalSayRoleLeft_bool = self.poco("NormalSayRoleLeft").offspring("Cloth").attr(
            #         "SpriteRenderer")
            #     print("左侧人物Cloth检测")
            #     if NormalSayRoleLeft_bool:
            #         print("左侧人物的Cloth资源正常")
            #     else:
            #         self.BookRead_info[achatProgress] = "左侧人物的Cloth的资源丢失"
            #         self.BookRead_info["result"] = False
            #         log(ResourceError(errorMessage="资源异常：NormalSayRoleLeft->Cloth的资源丢失"),
            #             desc="左侧人物的Cloth的资源丢失", snapshot=True)
            # except:
            #     self.BookRead_info[achatProgress] = "左侧人物的SpriteRenderer获取失败"
            #     self.BookRead_info["result"] = False
            #     dec = filename_head + "Cloth"
            #     myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #     log(ResourceError(errorMessage="资源异常：NormalSayRoleLeft->SpriteRenderer获取失败"),
            #         desc="左侧人物的SpriteRenderer获取失败", snapshot=True)

        elif pos_id == 1:
            RoleRightbool = self.assert_resource("RoleSay", "Cloth", "SpriteRenderer", "右侧角色Cloth检测", waitTime=2)
            self.resource_result(RoleRightbool, "SpriteRenderer", "右侧人物Cloth检测", filename_head=filename_head)
            # self.rightPos_judge()
            # if self.NormalSayRoleRight:
            #     RoleRightbool = self.assert_resource("NormalSayRoleRight", "Cloth", "SpriteRenderer", "右侧1角色Cloth检测",waitTime=2)
            #     self.resource_result(RoleRightbool,"SpriteRenderer","右侧1人物Cloth检测",filename_head=filename_head)
            # else:
            #     RoleRight2bool= self.assert_resource("NormalSayRoleRight2", "Cloth", "SpriteRenderer", "右侧2角色Cloth检测", waitTime=1)
            #     self.resource_result(RoleRight2bool, "SpriteRenderer", "右侧2角色Cloth检测", filename_head=filename_head)
            # if self.poco("NormalSayRoleRight").offspring("Body").wait(0.5).exists():
            #     try:
            #         NormalSayRoleRight = self.poco("NormalSayRoleRight").offspring("Cloth").wait(2).attr(
            #             "SpriteRenderer")
            #         print("右侧1人物Cloth检测")
            #         if NormalSayRoleRight:
            #             print("NormalSayRoleRight资源正常")
            #         else:
            #             self.BookRead_info[achatProgress] = "右侧1人物的SpriteRenderer为flase"
            #             self.BookRead_info["result"] = False
            #             dec = filename_head + "Cloth"
            #             myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #             log(ResourceError(errorMessage="资源异常：右侧1人物的SpriteRenderer为flase"),
            #                 desc="右侧1人物的SpriteRenderer为flase",
            #                 snapshot=True)
            #     except:
            #         self.BookRead_info[achatProgress] = "右侧1人物的未找到SpriteRenderer"
            #         self.BookRead_info["result"] = False
            #         dec = filename_head + "Cloth"
            #         myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #         log(ResourceError(errorMessage="资源异常：右侧1人物的未找到SpriteRenderer"),
            #             desc="右侧1人物的未找到SpriteRenderer",
            #             snapshot=True)
            #
            # else:
            #     # self.poco("NormalSayRoleRight2").offspring("Body").wait(0.2).exists():
            #     try:
            #         NormalSayRoleRight2 = self.poco("NormalSayRoleRight2").offspring("Cloth").wait(2).attr(
            #             "SpriteRenderer")
            #         print("右侧2人物Cloth检测")
            #         if NormalSayRoleRight2:
            #             print("NormalSayRoleRight2资源正常")
            #         else:
            #             self.BookRead_info[achatProgress] = "右侧2人物的SpriteRenderer为flase"
            #             self.BookRead_info["result"] = False
            #             dec = filename_head + "Cloth"
            #             myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #             log(ResourceError(errorMessage="资源异常：右侧2人物的SpriteRenderer为flase"),
            #                 desc="右侧2人物的SpriteRenderer为flase",
            #                 snapshot=True)
            #     except:
            #         self.BookRead_info[achatProgress] = "右侧2人物的未找到SpriteRenderer"
            #         self.BookRead_info["result"] = False
            #         dec = filename_head + "Cloth"
            #         myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            #         log(ResourceError(errorMessage="资源异常：右侧2人物的未找到SpriteRenderer"),
            #             desc="右侧2人物的未找到SpriteRenderer",
            #             snapshot=True)

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
        time = 3
        while time > 0:
            time -= 1
            if self.option_record["chatProgress"] == str(self.progress_info["chatProgress"]):
                print("进度相同容错处理")
                sleep(1)
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
        self.NormalSayRoleRight = None
        self.old_RoleRight_role_id=None
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
