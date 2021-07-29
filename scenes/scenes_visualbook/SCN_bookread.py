import random
import string

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
from common.COM_trans import *


class BookRead(FindObject):
    # myShop = Shop()
    def __init__(self):
        FindObject.__init__(self)
        self.StdPocoAgent1 = StdPocoAgent()
        self._POS = COM_utilities.PosTurn([0.5, 0.3])
        self.isstopRead = True  # 阅读状态
        self.isbookLoad = False
        self.iserrTime = 0
        self.touchtime = 0
        self._etime = 0
        self.progress_info = {}
        self.BookRead_info = {}
        self.randomNUM = True
        self.getstoryoptionslist = {}
        self.Story_cfg_chapter_dir = {}
        self.option_record = {}
        self.NormalSayRoleRight = None
        self.old_RoleRight_role_id = None
        self.achatProgress = None
        self.pos_id = None  # 当前选项self.pos_id值
        self.chat_type = None
        self.filename_head = None
        self.Result_info = {}

    def bookRead(self, bookid=None, chapterProgress=None):
        """视觉小说阅读"""
        self.reset_read()
        if self.poco("UIDialogue").wait(5).exists():
            clock()
            if self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励"):
                pass
            elif self.find_try("TxtFree", "非付费用户章节头广告"):
                touch(self._POS)
                keyevent("HOME")
                start_app("com.mars.avgchapters")
                sleep(2)
            if self.find_try("VisualRoleRender", "全身像类型"):
                if self.find_try("CloseBtn",description="全身像引导",waitTime=1):
                   self.findClick_try("CloseBtn","CloseBtn",description="关闭弹框")
                   self.findClick_try("Set", "Set", description="设置引导",sleeptime=1)
                   self.findClick_try("CloseBtn", "CloseBtn", description="关闭弹框")
                self.BookRead_info["showWhole"] = True
            self.getbookprogress(bookid, chapterProgress)
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
        print("阅读进度：", readprogress)
        self.progress_info["chapterProgress"] = chapterProgress
        MyData.read_story_cfg_chapter(BookID,
                                      str(self.progress_info["chapterProgress"]))  # 拉取章节信息存Story_cfg_chapter_dir表
        self.progress_info["chatProgress"] = readprogress  # 更新本地当前阅读对话进度
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        self.updte_oldReadProgress()  # 保存老进度
        self.progress_info["chat_num"] = MyData.Story_cfg_chapter_dir["length"] + 10000  # 当前章节对话总数
        self.progress_info["BookID"] = BookID
        self.option_record["resourceProgress"] = self.progress_info["chatProgress"]
        print("阅读书籍:", BookID)
        print("章节进度:", self.progress_info["chapterProgress"])
        print("对话总数:", self.progress_info["chat_num"])
        print("对话进度:", self.progress_info["chatProgress"])
        return self.progress_info

    def dialogueCourseJudge(self):
        """对话处理"""
        print("======================================================================")
        clock()
        self.updte_oldReadProgress()  # 保存老进度
        self.precondition()  # 转场前置判断
        self.resource_judgment()  # 对话资源判断
        self.chat_typeconf()  # 对话处理
        self.updte_readprogress()  # 更新当前书籍阅读进度
        self.progressjudge()  # 书籍阅读进度是否异常判断
        self.dialogueEndPOP()  # 阅读结束弹框判断
        self.freeze_poco=None
        clock("stop")
        print("======================================================================")

    def precondition(self):
        """前置处理"""
        if self.option_record["scene_bg_id"] != self.progress_info["option_info"]["scene_bg_id"]:
            print("转场等待")
            sleep(1.2)
            self.sceneBG_check()
        if self.progress_info["option_info"]["is_need_around"] == 1:
            print("场景环绕等待")
            sleep(2.5)
        self.option_record["scene_bg_id"] = self.progress_info["option_info"]["scene_bg_id"]  # 背景

    def updte_readprogress(self):
        """更新当前书籍阅读进度"""
        readprogress = MyData.getreadprogress_local(self.StdPocoAgent1)  # 拉取本地当前阅读进度
        self.progress_info["chatProgress"] = readprogress  # 更新本地进度
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        print("更新章节进度:", self.progress_info["chapterProgress"])
        print("更新对话进度:", self.progress_info["chatProgress"])

    def updte_oldReadProgress(self):
        """记录老的书籍阅读进度"""
        self.option_record["oldChatProgress"] = str(self.progress_info["chatProgress"])  # 记录当前进度

    def resource_result(self, result, findAtrr, des):
        """检测结果"""
        if result is False:
            dec = self.filename_head + des
            self.BookRead_info["result"] = False
            self.BookRead_info[str(self.progress_info["chatProgress"])] = des + "->" + findAtrr + " is not find"
            myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)

    def sceneBG_check(self):
        # 背景检测
        SceneBGbool = self.assert_resource("Root", "SceneBG", "SpriteRenderer", "背景", waitTime=1, reportError=False)
        if SceneBGbool is not True:
            # 特效类背景检测
            SceneBGbool1 = self.assert_resource("SceneBG", "Background", "SpriteRenderer", "特效类背景", waitTime=1)
            self.resource_result(SceneBGbool1, "SpriteRenderer", "特效类背景")

    def friendID_check(self):
        """friend_id检测"""
        try:
            friend_id = self.progress_info["option_info"]["friend_id"]  # 普通文本
            if friend_id and friend_id != 0:
                log("【资源检查】:friend_id->True  [{}]".format(friend_id))
            else:
                self.resource_result(False, "txt", "friend_id")
                log(ResourceError(errorMessage="资源异常：friend_id内容为空或为0"), desc="资源异常：friend_id内容为空或为0",
                    snapshot=True)
        except:
            self.resource_result(False, "txt", "friend_id")
            log(ResourceError(errorMessage="资源异常：friend_id内容为空或为0"), desc="资源异常：friend_id内容为空或为0",
                snapshot=True)

    def goodsTxt_check(self):
        try:
            goodstype = self.progress_info["option_info"]["goodstype"]  # 普通文本
            goodsid = self.progress_info["option_info"]["goodsid"]  # 普通文本
            if goodstype and goodsid:
                log("【资源检查】:goodstype:{1},goodsid:{2}->True".format(goodstype, goodsid))
            else:
                self.resource_result(False, "txt", "goodstype和goodsid")
                log(ResourceError(errorMessage="资源异常：内容为空"), desc="资源异常：内容为空",
                    snapshot=True)
        except:
            self.resource_result(False, "txt", "goodstype和goodsid")
            log(ResourceError(errorMessage="资源异常：未找到goodstype或goodsid"), desc="资源异常：未找到goodstype或goodsid",
                snapshot=True)

    def content_check(self):
        """内容检测"""
        self.Result_info["content"] = False
        try:
            content = self.progress_info["option_info"]["content"]  # 普通文本
            mind = self.progress_info["option_info"]["mind"]  # 想象文本
            if content:
                # mystr=mytrans(content)
                log("【资源检查】:普通文本->True  [{}]".format(content))
                # log("【中文翻译】:普通文本->True  [{}]".format(mystr))
                self.Result_info["content"] = True
            elif mind:
                # mystr=mytrans(mind)
                log("【资源检查】:想象文本->True  [{}]".format(mind))
                # log("【中文翻译】:想象文本->True  [{}]".format(mystr))
                self.Result_info["content"] = True
            elif "end" in self.progress_info["option_info"]["scene_bg_id"] or "End" in \
                    self.progress_info["option_info"]["scene_bg_id"]:
                log("【资源检查】:无文本章节结束End展示->True")
                self.Result_info["content"] = True
            else:
                if self.Result_info["goods"] == False:
                    self.resource_result(False, "txt", "content或mind")
                    log(ResourceError(errorMessage="资源异常：内容为空"), desc="资源异常：内容为空",
                        snapshot=True)
        except:
            self.resource_result(False, "txt", "content或mind")
            log(ResourceError(errorMessage="资源异常：未发现content或mind"), desc="资源异常：未发现content或mind",
                snapshot=True)
        finally:
            if self.Result_info["goods"] == False and self.Result_info["content"] == False:
                self.resource_result(False, "txt", "content或mind")
                log(ResourceError(errorMessage="资源异常：未发现content或mind"), desc="资源异常：未发现content或mind",
                    snapshot=True)
            if self.Result_info["goods"] == True and self.Result_info["content"] == True:
                self.resource_result(False, "txt", "同时存在文字和物品")
                log(ResourceError(errorMessage="资源异常：同时存在文字和物品"), desc="资源异常：同时存在文字和物品",
                    snapshot=True)

    def music_check(self):
        """音乐检测"""
        if self.StdPocoAgent1.get_Music():
            log("【资源检查】:音乐资源->True")
        else:
            log(ResourceError(errorMessage="资源异常：音乐资源组件异常"), desc="资源异常：音乐资源组件异常", snapshot=True)

    def goods_check(self):
        """物品检测"""
        self.Result_info["goods"] = False
        try:
            if self.progress_info["option_info"]["show_id"]:  # 物品检测
                Goodsbool = self.assert_resource("UIShowGoods", "Img", findAttr="texture", description="物品", waitTime=2)
                self.resource_result(result=Goodsbool, findAtrr="texture", des="物品")
                self.Result_info["goods"] = Goodsbool
                return True
        except:
            log("【资源检查】:无show_id字段")

    def selectRole_check(self):
        """角色选择资源"""
        bodybool = self.assert_Body("UIChapterSelectRoleOver", "Body", "texture", description="角色Body资源")
        self.resource_result(bodybool, "texture", "角色Body资源")
        RoleHair_bool = self.assert_resource("UIChapterSelectRoleOver", "Hair", "texture", description="角色装扮Hair资源")
        self.resource_result(RoleHair_bool, "texture", "角色装扮Hair资源")
        Sbool = self.assert_resource("UIChapterSelectRoleOver", "Cloth", "texture", "角色装扮Cloth资源")
        self.resource_result(Sbool, "texture", "角色选择确认")
        return True

    def showChangeDress_check(self):
        """换装检测"""
        try:
            sleep(0.5)
            list = self.poco("Viewport").offspring("Content").children().wait(2)
            for key, vlus in enumerate(list):
                name = vlus.get_name()
                bodybool = self.assert_Body(name, "Body", "texture", description="角色装扮Body资源")
                self.resource_result(bodybool, "texture", "角色装扮Body资源")
                Clothbool = self.assert_resource(name, "Cloth", "texture", description="角色装扮Cloth资源")
                self.resource_result(Clothbool, "texture", "角色装扮Cloth资源")
                RoleHair_bool = self.assert_resource(name, "Hair", "texture", description="角色装扮Hair资源")
                self.resource_result(RoleHair_bool, "texture", "角色装扮Hair资源")
        except ResourceError as e:
            print("角色装扮Cloth图片资源异常")
            self.BookRead_info[self.achatProgress] = "角色装扮Cloth图片资源异常"
            self.BookRead_info["result"] = False
            dec = self.filename_head + "Cloth"
            myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            log(ResourceError(errorMessage="资源异常：{0}第{1}角色装扮Cloth图片资源异常".format(self.achatProgress, key)),
                desc="{0}第{1}角色装扮图片资源异常".format(self.achatProgress, key), snapshot=True)

    def role_check(self):
        """角色检测"""
        if self.BookRead_info["showWhole"] == False:
            if self.pos_id == 2:
                bodybool = self.assert_Body("NormalSayRoleLeft", "Body", "SpriteRenderer", description="左侧人物Body资源")
                self.resource_result(bodybool, "SpriteRenderer", "左侧人物Body资源")
                RoleLeft_bool = self.assert_resource("NormalSayRoleLeft", "Cloth", "SpriteRenderer", "左侧人物的Cloth资源")
                self.resource_result(RoleLeft_bool, "SpriteRenderer", "左侧人物的Cloth资源")
                RoleHair_bool = self.assert_resource("NormalSayRoleLeft", "Hair", "SpriteRenderer", "左侧人物的Hair资源")
                self.resource_result(RoleHair_bool, "SpriteRenderer", "左侧人物的Hair资源")
            elif self.pos_id == 1:
                # name = self.poco(nameMatches='^NormalSayRoleRight.*$')
                bodybool = self.assert_Body("RoleSay", "Body", "SpriteRenderer", description="右侧人物Body资源")
                self.resource_result(bodybool, "SpriteRenderer", "右侧人物Body资源")
                RoleRightbool = self.assert_resource("RoleSay", "Cloth", "SpriteRenderer", "右侧角色Cloth检测")
                self.resource_result(RoleRightbool, "SpriteRenderer", "右侧人物Cloth检测")
                RoleHair_bool = self.assert_resource("RoleSay", "Hair", "SpriteRenderer", "右侧人物的Hair资源")
                self.resource_result(RoleHair_bool, "SpriteRenderer", "右侧人物的Hair资源")
        else:
            if self.pos_id == 2:
                bodybool = self.assert_Body("VisualRoleRender", "Body", "SpriteRenderer",
                                                description="全身像左侧人物Body资源")
                self.resource_result(bodybool, "SpriteRenderer", "全身像左侧人物Body资源")
                RoleLeft_bool = self.assert_resource(bodybool, "Cloth", "SpriteRenderer", "全身像左侧人物的Cloth资源")
                self.resource_result(RoleLeft_bool, "SpriteRenderer", "全身像左侧人物的Cloth资源")
                RoleHair_bool = self.assert_resource(bodybool, "Hair", "SpriteRenderer", "全身像左侧人物的Hair资源")
                self.resource_result(RoleHair_bool, "SpriteRenderer", "全身像左侧人物的Hair资源")
            elif self.pos_id == 1:
                # name = self.poco(nameMatches='^NormalSayRoleRight.*$')
                bodybool = self.assert_Body("VisualRoleRender", "Body", "SpriteRenderer",
                                                description="全身像右侧人物Body资源")
                self.resource_result(bodybool, "SpriteRenderer", "全身像右侧人物Body资源")
                RoleRightbool = self.assert_resource(bodybool, "Cloth", "SpriteRenderer", "全身像右侧角色Cloth检测")
                self.resource_result(RoleRightbool, "SpriteRenderer", "全身像右侧人物Cloth检测")
                RoleHair_bool = self.assert_resource(bodybool, "Hair", "SpriteRenderer", "全身像右侧人物的Hair资源")
                self.resource_result(RoleHair_bool, "SpriteRenderer", "全身像右侧人物的Hair资源")

    def oldShowChangeDress_check(self):
        log(ResourceError(errorMessage="【旧版换装提醒】"), desc="【旧版换装提醒", snapshot=True, level="error")
        self.resource_result(False, "旧版换装提醒", "旧版换装提醒")

    def setRoleName_check(self):
        RoleName = self.assert_getText("UICanvasStatic", "Placeholder", "TMPtext", description="角色名称检测")
        self.resource_result(RoleName, "TMPtext", "角色名称检测")

    def head_check(self):
        """电话头像检测"""
        bodybool = self.assert_Body("UIChapterCallPhone", "Body", "texture", description="电话呼叫方头像Body资源")
        self.resource_result(bodybool, "texture", "电话呼叫方头像Body资源")
        RoleRightbool = self.assert_resource("UIChapterCallPhone", "Cloth", "texture", "电话呼叫方头像Cloth检测")
        self.resource_result(RoleRightbool, "texture", "电话呼叫方头像Cloth检测")
        RoleHair_bool = self.assert_resource("UIChapterCallPhone", "Hair", "texture", "电话呼叫方头像Hair资源")
        self.resource_result(RoleHair_bool, "texture", "电话呼叫方头像Hair资源")

    def mail_check(self):
        """邮件检测"""
        bodybool = self.assert_Body("UIChapterMail", "Body", "texture", description="邮件头像Body资源")
        self.resource_result(bodybool, "texture", "邮件头像Body资源")
        RoleRightbool = self.assert_resource("UIChapterMail", "Cloth", "texture", "邮件头像Cloth检测")
        self.resource_result(RoleRightbool, "texture", "邮件头像Cloth检测")
        RoleHair_bool = self.assert_resource("UIChapterMail", "Hair", "texture", "邮件头像Hair资源")
        self.resource_result(RoleHair_bool, "texture", "邮件头像Hair资源")

    def friendHead_check(self):
        """短信头像检测"""
        bodybool = self.assert_Body("FriendHead", "Body", "texture", description="短信头像Body资源")
        self.resource_result(bodybool, "texture", "短信头像Body资源")
        RoleRightbool = self.assert_resource("FriendHead", "Cloth", "texture", "短信头像Cloth检测")
        self.resource_result(RoleRightbool, "texture", "短信头像Cloth检测")
        RoleHair_bool = self.assert_resource("FriendHead", "Hair", "texture", "短信头像Hair资源")
        self.resource_result(RoleHair_bool, "texture", "短信头像Hair资源")

    def resource_judgment(self):
        """选项资源判断"""
        if self.option_record["resourceProgress"] == str(self.progress_info["chatProgress"]):
            return
        self.Result_info = {}
        self.Result_info["goods"] = False
        self.achatProgress = str(self.progress_info["chatProgress"])
        self.pos_id = self.progress_info["option_info"]["pos_id"]  # 当前选项self.pos_id值
        self.chat_type = int(self.progress_info["option_info"]["chat_type"])
        self.filename_head = str(self.progress_info["chapterProgress"]) + "_" + self.achatProgress
        method_list = MyData.type_check_dir[self.chat_type]
        print("【阅读类型】:{0}对话类型->【阅读进度：{1}】".format(method_list[0], self.achatProgress))
        mylog.info("【阅读类型】:{0}对话类型->【阅读进度：{1}】".format(method_list[0], self.achatProgress))
        for i in range(1, len(method_list)):
            methodName = "self." + method_list[i]
            eval(methodName)()
        self.option_record["resourceProgress"] = str(self.progress_info["chatProgress"])

    def chat_typeconf(self):
        """选项判断"""
        chat_id = self.progress_info["option_info"]["chat_type"]  # 当前选项self.chat_type值
        select_id = self.progress_info["option_info"]["select_id"]  # select_id值
        # is_touch=False
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
            touch(self._POS, times=2, duration=0.2)
            # is_touch=True
            print("点击操作")
        else:
            try:
                if self.randomNUM:
                    self.randomNUM = False
                    Item0 = self.poco("UIChapterSelectList").child("Item")[0].wait(1)
                else:
                    self.randomNUM = True
                    Item0 = self.poco("UIChapterSelectList").child("Item(Clone)")[0].wait(1)
                self.findClick_childobject(Item0, description="选项")
            except:
                print("未发现选项")
        self.touchtime = self.touchtime + 1

    def progressjudge(self):
        """进度异常判断"""
        if self.option_record["oldChatProgress"] == str(self.progress_info["chatProgress"]):
            self._etime = self._etime + 1
            print("进度相同容错处理")
            # touch(self._POS)
            sleep(0.2)
            self.updte_readprogress()
        else:
            self._etime = 0
        if self._etime >= 5:
            self.BookRead_info["Jank"] = self.BookRead_info["Jank"] + 1
            VisualRead: dict = MyData.newPoP_dir["VisualRead"]
            for k, v in VisualRead.items():
                mybool=self.findClick_try(k, v, description="突发性弹框")
                if mybool:
                    return
            print("卡顿或异常次数：", self.BookRead_info["Jank"])
            if self.BookRead_info["Jank"] > 30:
                print("卡顿或异常次数较多", self.BookRead_info["Jank"])
                mylog.error("异常次数过多或检查启用新存档是否失败")
                log(Exception("异常次数过多或检查启用新存档是否失败"), snapshot=True)
                raise Exception
                return False

    def reset_read(self):
        """阅读参数初始化"""
        self.isstopRead = False
        self.Popuplist = []  # 清空之前的弹框列表
        self.BookRead_info["Jank"] = 0
        self.touchtime = 0
        # self.progress_info["results"] = True
        self.progress_info["storyoption"] = {}
        self.option_record["scene_bg_id"] = 0
        self.NormalSayRoleRight = None
        self.old_RoleRight_role_id = None
        self._etime = 0
        self.BookRead_info["showWhole"] = False

    def dialogueEndPOP(self):
        """章节尾弹框"""
        if int(self.option_record["oldChatProgress"]) == self.progress_info["chat_num"]:
            self.isstopRead = True
            touch(self._POS)
            self.common_Popup_Manage()
            time = 20
            if self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1):
                while (self.find_try("UIChapterContinue", description="章节尾弹框", waitTime=1)):
                    time -= 1
                    if time <= 15:
                        self.rebtn()
                    elif time <= 0:
                        log(Exception("弹框检测异常"), snapshot=True)
                        raise
                    self.common_Popup_Manage()
                    sleep(3)
                self.BookRead_info["clicks"] = self.touchtime
                self.BookRead_info["Pop-up"] = self.Popuplist
                return True

    def rebtn(self):
        """备用弹框检测"""
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
        self.findClick_try("UIChapterContinue", "BtnGet", description="章节尾奖励", sleeptime=0.5)
        self.findClick_try("UIChapterContinue", "ContinueBtn", description="章节尾弹框", sleeptime=0.5)
