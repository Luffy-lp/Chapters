import random
import string

from airtest.core.api import *
from poco.drivers.std import StdPocoAgent
from poco.exceptions import PocoNoSuchNodeException

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
        self.old_filename_head=None
        self.Result_info = {}
        self.all_list = []
        self.no_test_list = []
        self.jumpPOS = None
        self.selectPOS = None
        self.TextPOCO = None
        self.read_finish = False
        self.oldBookErrorList=[]

    def process_bookRead(self, bookid=None, chapterProgress=None):
        """视觉小说阅读流程"""
        self.reset_read()  # 阅读前参数处理
        if self.find_try("UIDialogue", description="阅读界面", waitTime=3):
            clock()
            self.manage_AD()  # 前置广告管理
            self.FullBody()  # 全身像临时处理
            self.getbookprogress(bookid, chapterProgress)
            self.get_JumpPOS()  # 跳转按钮位置获取
            if self.read_finish:
                self.process_dialogueReplenish()
                self.dialogueEndPOP()
            else:
                while not self.isstopRead:
                    self.process_dialogueManage()  # 阅读过程判断对应章节显示的内容
                return True
        else:
            print("结束阅读")
            self.BookRead_info["spendtime"] = str(clock("stop")) + "秒"
            return True

    def process_dialogueManage(self):
        """对话处理"""
        print("======================================================================")
        clock()
        self.freeze_poco = None
        self.updte_oldReadProgress()  # 保存老进度
        self.precondition()  # 转场前置判断
        self.resource_judgment()  # 对话资源判断
        self.chat_typeconf()  # 对话处理
        self.updte_readprogress()  # 更新当前书籍阅读进度
        self.progressjudge()  # 书籍阅读进度是否异常判断
        self.process_dialogueReplenish()  # 补全对话检测处理
        self.dialogueEndPOP()  # 阅读结束弹框判断
        clock("stop")
        print("======================================================================")

    def process_dialogueReplenish(self):
        if int(self.option_record["oldChatProgress"]) == self.progress_info["chat_num"] or self.read_finish == True:
            MyData.w_yaml_dialogue_result()  # 记录到对白记录表中
            print("进入补全")
            self.isstopRead = True
            self.getAllList(10001)
            self.getNoList()
            self.out_find()
            self.updte_oldReadProgress()
            # self.dialogueEndPOP()

    def getAllList(self, begin):
        """获取所有项"""
        num = int(self.progress_info["chat_num"]) - 10000
        for i in range(0, num):
            sum = i + begin
            self.all_list.append(sum)
        return self.all_list

    def getNoList(self):
        """获取未读项"""
        print("已阅读对白数：", len(MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])]))
        print("阅读覆盖率：", len(MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])]) / len(self.all_list))
        for i in MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])]:
            if i in self.all_list:
                self.all_list.remove(i)
        self.all_list.append(int(self.progress_info["chat_num"]))
        return self.all_list

    def jumpToDialogue(self, i):
        """调转到对应对白"""
        if self.progress_info["chatProgress"] == i:
            return True
        self.TextPOCO.set_text(str(i))
        sleep(0.1)
        touch(self.jumpPOS)
        sleep(0.1)
        self.updte_readprogress()
        time = 2
        while time > 0:
            time -= 1
            if self.progress_info["chatProgress"] == i:
                return True
            else:
                self.TextPOCO.set_text(str(i))
                sleep(0.1)
                touch(self.jumpPOS)
                sleep(0.1)
                self.updte_readprogress()
        self.chat_typeconf()

    def out_find(self):
        """遗漏项补全"""
        print(self.all_list)
        for i in self.all_list:
            print("======================================================================")
            clock()
            print("补全：", i)
            self.freeze_poco = None
            self.updte_oldReadProgress()  # 保存老进度
            self.jumpToDialogue(i)
            self.updte_readprogress()
            self.precondition()
            self.resource_judgment()
            self.progressjudge()  # 书籍阅读进度是否异常判断
            # self.chat_typeconf()  # 对话处理
            clock("stop")
            print("======================================================================")

    def getbookprogress(self, BookID, chapterProgress):
        """获取当前书籍信息"""
        self.BookRead_info["result"] = True
        self.all_list = []
        readprogress = MyData.getreadprogress_local(self.StdPocoAgent1)  # 拉取本地当前阅读进度
        self.progress_info["chapterProgress"] = chapterProgress
        MyData.read_story_cfg_chapter(BookID, str(chapterProgress))  # 拉取章节信息存Story_cfg_chapter_dir表
        self.progress_info["chatProgress"] = readprogress  # 更新本地当前阅读对话进度
        self.progress_info["option_info"] = MyData.Story_cfg_chapter_dir[
            str(self.progress_info["chatProgress"])]  # 更新对话信息
        self.updte_oldReadProgress()  # 保存老进度
        self.progress_info["chat_num"] = MyData.Story_cfg_chapter_dir["length"] + 10000  # 当前章节对话总数
        self.progress_info["BookID"] = BookID
        self.option_record["resourceProgress"] = self.progress_info["chatProgress"]
        MyData.r_yaml_dialogue_result()
        if str(self.progress_info["chapterProgress"]) not in MyData.dialogueResult_dir:
            print("首次阅读")
            MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])] = []
        elif self.progress_info["chat_num"] in MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])]:
            print("已经完成过一次阅读")
            self.read_finish = True
        print("阅读书籍:", self.progress_info["BookID"])
        print("章节进度:", self.progress_info["chapterProgress"])
        print("对话总数:", self.progress_info["chat_num"])
        print("对话进度:", self.progress_info["chatProgress"])
        return self.progress_info

    def manage_AD(self):
        """广告处理"""
        self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励")
        if self.find_try("TxtFree", "非付费用户章节头广告"):
            touch(self._POS)
            keyevent("HOME")
            start_app("com.mars.avgchapters")
            sleep(2)

    def FullBody(self):
        """全身像处理"""
        if self.find_try("VisualRoleRender", "全身像类型"):
            if self.find_try("UIFullBodyGuide", description="全身像引导", waitTime=1):
                self.findClick_try("CloseBtn", "CloseBtn", description="关闭弹框")
                self.findClick_try("Set", "Set", description="设置引导", sleeptime=1)
                self.findClick_try("CloseBtn", "CloseBtn", description="关闭弹框")
            self.BookRead_info["showWhole"] = True

    def get_JumpPOS(self):
        """跳转按钮位置获取"""
        if self.jumpPOS == None:
            pos = self.poco("Text (TMP)").wait(2).get_position()
            if MyData.DeviceData_dir["offset"]:
                print(MyData.DeviceData_dir["offset"])
                pos[1] += MyData.DeviceData_dir["offset"]
                print(pos[1])
            # self.poco("Text (TMP)").click()
            self.jumpPOS = COM_utilities.PosTurn(pos)
            self.TextPOCO = self.poco("InputField").wait(2)

    def precondition(self):
        """前置处理"""
        self.achatProgress = str(self.progress_info["chatProgress"])
        self.filename_head = str(self.progress_info["chapterProgress"]) + "_" + self.achatProgress
        self.old_filename_head=str(self.progress_info["chapterProgress"])
        if self.option_record["scene_bg_id"] != self.progress_info["option_info"]["scene_bg_id"]:
            print("切换场景")
            sleep(3)
            if self.progress_info["option_info"]["chat_type"] != 13:
                self.sceneBG_check()
        if self.progress_info["option_info"]["is_need_around"] == 1:
            print("场景环绕等待")
            sleep(3.5)
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

    # def resource_result(self, result, findAtrr, des):
    #     """检测结果"""
    #     if result is False:
    #         dec = self.filename_head + des
    #         self.BookRead_info["result"] = False
    #         self.BookRead_info[str(self.progress_info["chatProgress"])] = des + "->" + findAtrr + " is not find"
    #         myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
    def resource_result(self, result, findAtrr, des):
        """检测结果"""
        if result is False:
            if self.progress_info["BookID"][0] == "1" and ("电话呼叫方头像" in des or "Back1" in des):
                role_id = str(self.progress_info["option_info"]["role_id"])
                dec = self.old_filename_head +"roleID"+role_id+des
                if dec not in self.oldBookErrorList:
                    self.oldBookErrorList.append(dec)
                    self.BookRead_info["result"] = False
                    self.BookRead_info[str(self.progress_info["chatProgress"])] = des + "->" + findAtrr + " is not find"
                    myscreenshot(path_BOOKREAD_ERROR_IMAGE, dec)
            else:
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
                return friend_id
            else:
                self.resource_result(False, "txt", "friend_id")
                log(ResourceError(errorMessage="资源异常：friend_id内容为空或为0"), desc="资源异常：friend_id内容为空或为0",
                    snapshot=True)
        except:
            self.resource_result(False, "txt", "friend_id")
            log(ResourceError(errorMessage="资源异常：friend_id内容为空或为0"), desc="资源异常：friend_id内容为空或为0",
                snapshot=True)
        return False

    # def goodsTxt_check(self):
    #     try:
    #         goodstype = self.progress_info["option_info"]["goodstype"]  # 普通文本
    #         goodsid = self.progress_info["option_info"]["goodsid"]  # 普通文本
    #         if goodstype and goodsid:
    #             log("【资源检查】:goodstype:{1},goodsid:{2}->True".format(goodstype, goodsid))
    #         else:
    #             self.resource_result(False, "txt", "goodstype和goodsid")
    #             log(ResourceError(errorMessage="资源异常：内容为空"), desc="资源异常：内容为空",
    #                 snapshot=True)
    #     except:
    #         self.resource_result(False, "txt", "goodstype和goodsid")
    #         log(ResourceError(errorMessage="资源异常：未找到goodstype或goodsid"), desc="资源异常：未找到goodstype或goodsid",
    #             snapshot=True)

    def goods_check(self):
        """物品检测"""
        try:
            show_id = self.progress_info["option_info"]["show_id"]
        except:
            log("【资源检查】:无show_id字段")
        if show_id:
            self.Result_info["goods"]=self.resource_check("UIShowGoods", "Img", "texture", "物品")

    def selectRole_check(self):
        """角色选择资源"""
        parentName = "UIChapterSelectRoleOver"
        role_id = str(self.progress_info["option_info"]["role_id"])
        fashion_id = str(self.progress_info["option_info"]["fashion_id"])
        face_id = self.progress_info["option_info"]["face_id"]
        self.roleParts_check(parentName, "texture", "角色装扮", role_id=role_id, fashion_id=fashion_id, face_id=face_id)

    def showChangeDress_check(self):
        """换装检测"""
        try:
            list = self.poco("Viewport").offspring("Content").children().wait(2)
        except PocoNoSuchNodeException as e:
            print(e)
            raise
        role_id = str(self.progress_info["option_info"]["role_id"])
        fashion_id = str(self.progress_info["option_info"]["fashion_id"])
        face_id = self.progress_info["option_info"]["face_id"]
        for key, vlus in enumerate(list):
            name = vlus.get_name()
            self.roleParts_check(name, "texture", "角色换装", role_id=role_id, fashion_id=fashion_id, face_id=face_id)
    def manyVideo_check(self):
        """多人视频检测"""
        try:
            video_id = self.progress_info["option_info"]["video_id"]
            role_id = self.progress_info["option_info"]["role_id"]
            sayParentName, attr = "SayHead", "texture"
            videoList = video_id.split("#")
            chatIdList=videoList[0].split("*")
            bgList = videoList[1].split("*")
            if len(chatIdList)!=len(bgList):
                self.resource_result(False, "_chat.txt", des="多人视频背景和角色数不匹配")
                log("{0}配置检查异常".format("多人视频背景和角色数不匹配"))
                return
        except:
            self.resource_result(False, "_chat.txt", des="多人视频背景配置错误")
            log("{0}配置检查异常".format("多人视频背景配置错误"))
            return
        self.resource_check("ChatRole", "Bg", attr, "多人视频背景")
        des = "说话人角色"
        self.roleParts_check(sayParentName, attr, des, role_id)
        des = "聊天角色"
        chatRoleParentName = "ChatRole"
        role_id = videoList[0]
        self.roleParts_check(chatRoleParentName, attr, des, role_id)

    def role_check(self):
        """角色检测"""
        parameter = self.role_parameter()
        self.roleParts_check(parameter["parentName"], parameter["attr"], parameter["des"], parameter["role_id"],parameter["fashion_id"], parameter["face_id"])

    def setRoleName_check(self):
        """角色名称检测"""
        RoleName = self.assert_getText("UICanvasStatic", "Placeholder", "TMPtext", description="角色名称检测")
        self.resource_result(RoleName, "TMPtext", "角色名称检测")

    def mail_check(self):
        """邮件检测"""
        friend_id = self.friendID_check()
        if friend_id:
            parentName, attr, des = "UIChapterMail", "texture", "邮件头像"
            self.roleParts_check(parentName, attr, des, friend_id)

    def friendHead_check(self):
        """短信头像检测"""
        friend_id = self.friendID_check()
        if friend_id:
            parentName, attr, des = "FriendHead", "texture", "短信头像"
            self.roleParts_check(parentName, attr, des, friend_id)

    def head_check(self):
        """电话头像检测"""
        friend_id = self.friendID_check()
        if friend_id:
            friend_id=str(friend_id)
            try:
                friend_fashion_id = str(self.progress_info["option_info"]["friend_fashion_id"])
            except:
                friend_fashion_id=None
            role_id = str(self.progress_info["option_info"]["role_id"])
            fashion_id = str(self.progress_info["option_info"]["fashion_id"])
            fashion_id = str(self.progress_info["option_info"]["fashion_id"])
            parentName, attr = "SelfHead", "texture"
            if self.progress_info["BookID"][0] == "1":
                des = "电话被呼叫方头像"
                parentName = "Head"
                self.roleParts_check(parentName, attr, des, role_id, fashion_id=fashion_id)
            else:
                if friend_id == role_id:
                    des = "电话被呼叫方头像"
                    parentName = "Head"
                    self.roleParts_check(parentName, attr, des, role_id, fashion_id=fashion_id)
                else:
                    des = "电话呼叫方头像"
                    self.roleParts_check(parentName, attr, des, role_id, fashion_id=fashion_id)
                    des = "电话被呼叫方头像"
                    parentName = "Head"
                    self.roleParts_check(parentName, attr, des, friend_id, fashion_id=friend_fashion_id)

    def oldShowChangeDress_check(self):
        log(ResourceError(errorMessage="【旧版换装提醒】"), desc="【旧版换装提醒", snapshot=True, level="error")
        self.resource_result(False, "旧版换装提醒", "旧版换装提醒")

    def resource_check(self, parentName, partName, Attr, description):
        """通用资源检测方法"""
        bool = self.assert_resource(parentName, partName, Attr, description=description)
        self.resource_result(bool, Attr, description)
        return bool

    def face_check(self,parentName, partName, Attr, face_id,description):
        """face检测"""
        bool = self.assert_face(parentName, partName, Attr,face_id,description)
        description=face_id+description
        self.resource_result(bool, Attr, description)

    def roleParts_check(self, parentName, attr, des, role_id, fashion_id=None, face_id=None):
        """通用角色部件遍历"""
        bookid = self.progress_info["BookID"]
        if role_id and role_id is not "0":
            fashion_list = MyData.getfashion(bookid, role_id, fashion_id)
            for i in fashion_list:
                description = des + i
                self.resource_check(parentName, i, attr, description)
            if face_id:
                self.face_check(parentName, "Face1", "texture", face_id,"表情")
        else:
            log(Exception("role_id不存在"), snapshot=True)
            return
    def checkSleep(self):
        """检测过快会导致问题"""
        sleep(0.1)
        print("睡眠")
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
        try:
            if self.StdPocoAgent1.get_Music():
                log("【资源检查】:音乐资源->True")
            else:
                self.resource_result(False, "组件", "音乐组件")
                log(ResourceError(errorMessage="资源异常：音乐资源组件异常"), desc="资源异常：音乐资源组件异常", snapshot=True)
        except:
            self.resource_result(False, "组件", "音乐组件")
            log(ResourceError(errorMessage="资源异常：音乐资源组件异常"), desc="资源异常：音乐资源组件异常", snapshot=True)

    def role_parameter(self):
        """角色检测参数获取 texture  SpriteRenderer"""
        parentName, attr, full_des, place_des = "VisualRoleRender", "texture", "全身", "左侧"
        role_id = str(self.progress_info["option_info"]["role_id"])
        fashion_id = str(self.progress_info["option_info"]["fashion_id"])
        face_id = self.progress_info["option_info"]["face_id"]
        if self.pos_id == 2:
            place_des = "左侧"
        elif self.pos_id == 1:
            place_des = "右侧"
        else:
            return
        if self.BookRead_info["showWhole"] == False:
            parentName = "RoleSay"
            full_des = "半身"
        des = full_des + place_des
        parameter = {
            "parentName": parentName,
            "attr": attr,
            "des": des,
            "role_id": role_id,
            "fashion_id": fashion_id,
            "face_id": face_id
        }
        return parameter

    def resource_judgment(self):
        """选项资源判断"""
        if self.option_record["resourceProgress"] == str(self.progress_info["chatProgress"]):
            return
        self.Result_info = {}
        self.Result_info["goods"] = False
        self.pos_id = self.progress_info["option_info"]["pos_id"]  # 当前选项self.pos_id值
        self.chat_type = int(self.progress_info["option_info"]["chat_type"])
        # self.filename_head = str(self.progress_info["chapterProgress"]) + "_" + self.achatProgress
        method_list = MyData.type_check_dir[self.chat_type]
        print("【阅读类型】:{0}对话类型->【阅读进度：{1}】".format(method_list[0], self.achatProgress))
        mylog.info("【阅读类型】:{0}对话类型->【阅读进度：{1}】".format(method_list[0], self.achatProgress))
        for i in range(1, len(method_list)):
            methodName = "self." + method_list[i]
            eval(methodName)()
        self.option_record["resourceProgress"] = str(self.progress_info["chatProgress"])
        MyData.dialogueResult_dir[str(self.progress_info["chapterProgress"])].append(self.progress_info["chatProgress"])

    def chat_typeconf(self):
        """对话处理"""
        chat_id = self.progress_info["option_info"]["chat_type"]  # 当前选项self.chat_type值
        select_id = self.progress_info["option_info"]["select_id"]  # select_id值
        # is_touch=False
        if chat_id in MyData.chat_type_dir:
            description = MyData.chat_type_dir[chat_id][0]
            print("description", description)
            print("chat_id", chat_id)
            for val in range(1, len(MyData.chat_type_dir[chat_id])):
                clickname = MyData.chat_type_dir[chat_id][val]
                if type(clickname) == int:
                    sleep(clickname)
                else:
                    self.findClick_try(clickname, clickname, description=description, waitTime=2, sleeptime=2)
            if chat_id is 10:
                self.ChangeDress_Manage()
        elif select_id == 0:
            if int(self.option_record["oldChatProgress"]) == self.progress_info["chat_num"]:
                return
            touch(self._POS, times=2, duration=0.2)
            # is_touch=True
            print("点击操作")
        else:
            self.selectManage(select_id)
        self.touchtime = self.touchtime + 1
    def ChangeDress_Manage(self):
        """更新角色形象"""
        roleID=str(self.progress_info["option_info"]["role_id"])
        MyData.updateUserRoleFashion(self.progress_info["BookID"],roleID)
    def get_selectPOS(self):
        """跳转按钮位置获取"""
        if self.selectPOS == None:
            try:
                pos = self.poco("UIChapterSelectList").child("Item")[0].get_position()
            except:
                print("获取选项1")
            if MyData.DeviceData_dir["offset"]:
                print(MyData.DeviceData_dir["offset"])
                pos[1] += MyData.DeviceData_dir["offset"]
            self.selectPOS = COM_utilities.PosTurn(pos)
        return self.selectPOS

    def selectManage(self, select_id):
        print("选项")
        try:
            # self.get_selectPOS()
            # touch(self.selectPOS)
            # sleep(0.5)
            Item0 = self.poco("UIChapterSelectList").child("Item")[0].wait(1)
            self.findClick_childobject(Item0, description="选项")
        except:
            print("未发现选项")

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
        if self._etime >= 4:
            self.BookRead_info["Jank"] = self.BookRead_info["Jank"] + 1
            VisualRead: dict = MyData.newPoP_dir["VisualRead"]
            for k, v in VisualRead.items():
                mybool = self.findClick_try(k, v, description="突发性弹框")
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
            MyData.w_yaml_dialogue_result()
            sleep(1)
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
