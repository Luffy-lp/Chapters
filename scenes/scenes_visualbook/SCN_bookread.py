from airtest.core.api import *
from common.COM_findobject import CommonPoco
from common import COM_utilities
# TODO：查找书籍不准确，角色形象弹框影响阅读速度
# SODO：书籍的当前进度要从接口获得
# TODO：付费选项弹出的快捷购买未处理
from common.COM_data import MyData
from common.COM_utilities import clock
from common.my_log import mylog


class VisualBook(CommonPoco):
    isstopRead = True  # 阅读状态
    isbookLoad = False
    iserrTime = 0
    touchtime = 0
    _etime = 0
    ReadBook_info = {}
    getstoryoptionslist={}
    ReadBook_info["storyoption"]={}
    def __init__(self):
        CommonPoco.__init__(self)
        self._POS = COM_utilities.PosTurn([0.31, 0.55])
        # self.getReadBook_info("10001")

    def bookLoad(self):
        """书籍加载"""
        if self.find_try("DefaultBg", description="书籍加载界面", waitTime=1, tryTime=3):
            startime = time.time()
            while self.poco("DefaultBg").wait(3).exists():
                loadtime = time.time() - startime
                if self.find_try("Discover"):
                    mylog.error("加载书籍异常")
                    log(Exception("加载书籍异常，自动返回到大厅"))
                    raise
                print("书籍加载中", loadtime)
                if loadtime > 360:
                    self.findClick_object("HomeBtn", "HomeBtn", description="加载书籍超时,返回大厅")
                    mylog.error("加载书籍超时")
                    log(loadtime, timestamp=time.time(), desc="加载书籍超时", snapshot=True)
                    raise
                    return False
            loadtime = time.time() - startime
            return True, loadtime
            print("完成书籍加载，加载时间为{0}秒".format(loadtime))
            log(loadtime, timestamp=time.time(), desc="完成书籍加载", snapshot=True)
        time.sleep(3)

    def bookRead(self, Item=0):
        """视觉小说阅读界面"""
        self.Popuplist = []  # 清空之前的弹框列表
        self.ReadBook_info["异常次数"] = 0
        POS = None
        self.getReadBook_info(MyData.UserData_dir["bookDetailInfo"]["BookID"])
        print(int(MyData.UserData_dir["bookDetailInfo"]["BookID"]))
        print(int(self.ReadBook_info["chatProgress"]))
        self.getstoryoptionslist=MyData.getstoryoptions(int(MyData.UserData_dir["bookDetailInfo"]["BookID"]), int(self.ReadBook_info["chapterProgress"]))
        print("getstoryoptionslist",self.getstoryoptionslist)
        if self.getstoryoptionslist:
            for k in self.getstoryoptionslist:
                for k1, v1 in k.items():
                    self.ReadBook_info["storyoption"][k1]=v1
        if self.poco("UIDialogue").wait(5).exists():
            self.findClick_try("UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励", waitTime=2)
            touch(self._POS)
            self.isstopRead = False
            time.sleep(3)
            clock()
            # stroyoption = {
            #     "description": None,
            #     "find_name": [],
            #     "touch_name": {}
            # }
            while (not self.isstopRead):
                bchatProgress = self.ReadBook_info["chatProgress"]
                print("记录选项进度", bchatProgress)
                if self.poco("UIChapterSelectList").child("Item").wait(0.2).exists():  # "UISelectList")老版本
                    Item0 = self.poco("UIChapterSelectList").child("Item")[Item]
                    # if Item0.child("FreeBg").wait(0.1).exists():
                    # TXT=Item0.child("Txt").get_TMPtext()
                    # mylog.info("当前进度：【{0}】选择的选项：-【{1}】".format(self.ReadBook_info["chatProgress"],TXT))
                    Item0.click()
                    if POS == None:
                        POS = Item0.get_position()
                        self._POS = COM_utilities.PosTurn(POS)
                    print("点击第{0}个选项".format(Item + 1))
                else:
                    touch(self._POS)
                self.touchtime = self.touchtime + 1
                print("点击次数{0}".format(self.touchtime))
                self.dialogueCourseJudge(bchatProgress)  # 阅读过程判断对应章节显示的内容
        else:
            print("未检测到阅读界面")

    def getReadBook_info(self, BookID):
        if BookID == None:
            BookID = MyData.UserData_dir["bookDetailInfo"]["BookID"]  # 获取当前的BookID
        readprogress = MyData.getreadprogress(BookID)  # 获取书籍进度
        chapterProgress = readprogress["chapterProgress"]  # 获取章节进度
        chatProgress = readprogress["chatProgress"]  # 获取到选项进度
        chat_num = MyData.Story_cfg_chapter_dir[str(chapterProgress)]["chat_num"]  # 获取到当前章节总数
        self.ReadBook_info["chapterProgress"] = chapterProgress
        self.ReadBook_info["chat_num"] = chat_num + 10000
        self.ReadBook_info["chatProgress"] = chatProgress
        self.ReadBook_info["BookID"] = BookID
        # self.ReadBook_info["BookName"]=MyData.UserData_dir["bookDetailInfo"]["BookName"]
        return self.ReadBook_info

    def dialogueCourseJudge(self, bchatProgress):
        readprogress = MyData.getreadprogress(self.ReadBook_info["BookID"])  # 获取书籍进度
        self.ReadBook_info["chatProgress"] = readprogress["chatProgress"]
        achatProgress = self.ReadBook_info["chatProgress"]
        print("上一页ID::", bchatProgress)
        print("当前页ID:", achatProgress)
        print("本章总页数:", self.ReadBook_info["chat_num"])
        if int(achatProgress) in self.ReadBook_info["storyoption"].keys():
            description = self.ReadBook_info["storyoption"][achatProgress][0]
            for val in range(1, len(self.ReadBook_info["storyoption"][achatProgress])):
                clickname = self.ReadBook_info["storyoption"][achatProgress][val]
                print("clickname", clickname)
                print("description", description)
                self.findClick_object(clickname, clickname, description=description, waitTime=1, sleeptime=2)
        if achatProgress == self.ReadBook_info["chat_num"]:
            touch(self._POS)
            self.dialogueEndPOP()  # 阅读结束弹框判断
        if achatProgress == bchatProgress:
            self._etime = self._etime + 1
            if self._etime > 2:
                self._etime = 0
                if self.roleDressJudge() == True:
                    return
                else:
                    # utilities.screenshot(loc_desc="有卡顿")
                    self.ReadBook_info["异常次数"] = self.ReadBook_info["异常次数"] + 1
                    print("卡顿或异常次数：", self.ReadBook_info["异常次数"])
                    if self.ReadBook_info["异常次数"] > 20:
                        print("卡顿或异常次数较多", self.ReadBook_info["异常次数"])
                        mylog.error("异常次数过多读书可能卡死")
                        log(Exception("异常次数过多读书可能卡死"))
                        raise Exception
                        return False
        else:
            print("正常点击")
            self._etime = 0

    def roleDressJudge(self):
        if self.find_try("UIChangeDress", "角色装扮选择", waitTime=0.2, tryTime=1):  # UIPortraitDress老版本
            self.findClick_object("NextCellButton", "NextCellButton", description="装扮右滑", sleeptime=2)
            while (self.find_try("UIChangeDress", "角色装扮选择", waitTime=0.2, tryTime=1)):
                if self.find_try("ButtonNoPrice", description="选择免费选项", sleeptime=3):
                    self.findClick_try("ButtonNoPrice", "ButtonNoPrice", description="选择免费选项", sleeptime=0.5)
                elif self.find_try("ButtonPrice", description="付费选项", sleeptime=0.5):
                    self.findClick_try("NextCellButton", "NextCellButton", description="装扮右滑", sleeptime=0.5)
            return True

        if self.find_try("UIOldSetName", description="老的角色名称设置", waitTime=0.1, tryTime=1):  # "UISetName"
            self.poco("InputField").click()
            text("RoleName")
            self.poco("ConfirmBtn").click(sleep_interval=0.2)
            self.poco("ConfirmBtn").click()
            # poco("UIQuickPayFrame")快速购买

    def dialogueEndPOP(self):
        """章节尾弹框"""
        # self.poco.wait_for_any()
        touch(self._POS)
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
# VisualBook=VisualBook()
# print(BookNewDetail1.ReadBook_info)
# BookNewDetail1.bookChoose("Weekly",index=0)
