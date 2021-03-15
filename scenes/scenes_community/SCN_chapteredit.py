from airtest.core.api import *
from common.COM_findobject import FindObject
from common.my_log import mylog
from scenes.scenes_community.SCN_creation import Creation
from scenes.scenes_community.SCN_IntroduceEdit import IntroduceEdit
from scenes.scenes_community.SCN_mainstudio import MainStudio


class ChapterEdit(FindObject):
    """小说编辑界面"""
    ChapterEdit_info = {}

    def __init__(self):
        FindObject.__init__(self)

    def LuaUIChapterEdit(self):
        self.find_object("LuaUIChapterEdit", description="章节编辑界面", waitTime=3)

    def into_mainstudio(self):
        self.click_object("BtnEdit", description="进入创作工作室", sleeptime=2)

    def into_IntroduceEdit(self):
        """编辑简介入口"""
        if self.find_try("btnEdit", description="简介第一次编辑", waitTime=3):
            self.findClick_object("NoCover(Clone)", "btnEdit", description="进入简介编辑", waitTime=1,
                                  sleeptime=2)
        else:
            self.click_object("EditStatus", description="进入简介编辑")

    def AddChapter(self):
        self.click_object("BtnAddChapter", description="新增章节")

    def topBar(self, type):
        """顶部按钮 Back：返回按钮，Guide：帮助按钮，Edit：设置书籍完结"""
        if type == "Edit":
            self.click_object("BtnEdit", description="操作书籍")
            POCOend = self.poco("Options").child("Button(Clone)")[0].wait(5)
            self.findClick_childobject(POCOend, description="设置书籍完结", sleeptime=3)
        if type == "Guide":
            self.click_object("BtnGuide", description="帮助按钮")
        if type == "Back":
            self.click_object("BtnBack", description="返回按钮")

    def process_creationStoryFlow(self, bookname):
        """创作室主流程"""
        MainStudio1 = MainStudio()
        MainStudio1.branchprocess()
        self.into_IntroduceEdit()
        IntroduceEdit1 = IntroduceEdit()
        IntroduceEdit1.mainprocess(bookname)
        sleep(3)
        self.getChapterEdit_info()
        self.topBar("Back")  # 返回到上一级
        sleep(1)
        self.topBar("Back")  # 返回到创作小说主页
        return True

    def getChapterEdit_info(self):
        try:
            stroyTitle = self.poco("TxtTitle").get_TMPtext()
            stroyDescript = self.poco("TxtDescript").get_TMPtext()
            stroyStatus = self.poco("TxtStatus").get_TMPtext()
            self.ChapterEdit_info["stroyTitle"] = stroyTitle
            self.ChapterEdit_info["stroyDescript"] = stroyDescript
            self.ChapterEdit_info["stroyStatus"] = stroyStatus
        except:
            mylog.error("等待-【{}】-元素可见超时".format("书籍详情信息"))
# ChapterEdit1=ChapterEdit()
# ChapterEdit1.process_creationStoryFlow("lipeng0000")