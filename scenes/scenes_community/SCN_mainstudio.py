from airtest.core.api import *
from common.COM_findobject import FindObject
from common.COM_utilities import *
from common.COM_Error import MyException


# TODO:返回到上一个界面应该用树代替

class MainStudio(FindObject):
    """作家工作室"""
    chapterDlg = 0

    def __init__(self):
        FindObject.__init__(self)

    def LuaUITalkEdit2(self):
        self.find_object("LuaUITalkEdit2", description="对话编辑页面2", waitTime=3)
        self.LuaUIStudio()
        self.findClick_object("UINewBookRack", "CreateBtn", description="进入工作室", waitTime=1, sleeptime=2)

    def LuaUIStudio(self):
        """新手引导界面检查"""
        self.find_object("LuaUIStudio", description="工作室显示UI", waitTime=3)
        clock()
        while self.find_try("LuaUIGuide", description="新手引导界面"):
            self.findClick_try("LuaUIGuide", "LuaUIGuide", description="点击下一步", sleeptime=1)
            mytime = float(clock("stop"))
            if mytime > 80:
                print("新手引导界面异常")
                log(Exception("查找新手引导界面异常"), snapshot=True)
                raise Exception("查找新手引导界面异常")

    def storiesPOP(self):
        self.find_object("LuaUITalkEdit2", description="短信小说界面", waitTime=3)

    def chooseHead(self):
        """选择角色头像"""
        if self.findClick_object("LuaUIRoleCreateDlg", "Head", description="选择头像弹框", waitTime=1):
            self.click_object("BtnHead", description="选择图像")
            self.find_object("UIBottomForm", description="选择角色方式", waitTime=3)
            POCO = self.poco("Options").child("Button(Clone)")[0]
            self.findClick_childobject(POCO, description="选择Avatar Gallery")
            sleep(2)
            if self.find_object("ConentPageView", description="等待刷新图像列表", waitTime=10):
                POCO = self.poco("LoopStaggeredGridView1").child("Viewport").child("Content").child("Item(Clone)")[
                    self.chapterDlg]
                self.findClick_childobject(POCO, description="选择一个图像", waitTime=5)
                self.chapterDlg = self.chapterDlg + 1

    def writeName(self, name="lipeng"):
        if self.findClick_object("LuaUIRoleCreateDlg", "Head", description="选择头像弹框", waitTime=1, sleeptime=2):
            CreateDlgTXTPOCO = self.poco("LuaUIRoleCreateDlg").child("Bg").child("InputField").child("Text Area")
            self.findClick_childobject(CreateDlgTXTPOCO, description="点击输入角色名称", waitTime=1, sleeptime=1)
            text(name)
            print("输入角色姓名：", name)
            sleep(1)

    def submitOK(self):
        self.findClick_try("BtnOK", "BtnOK", description="OK")
        sleep(1)
        self.findClick_try("BtnOK", "BtnOK", description="OK")

    def characterUI(self, characterType):
        """弹出角色图像弹框 main,supporting主要角色和次要角色"""
        if characterType == "main":
            MainPOCO = self.poco("MainCharacter").child("HeadMask").wait(3)
            self.findClick_childobject(MainPOCO, description="主角色图像框", waitTime=1)
        if characterType == "supporting":
            Supportinglist = self.poco("SupportingCharcters").child("Viewport").child("Content").child(
                "RoleItem(Clone)")
            SuPOCO = self.poco("SupportingCharcters").child("Viewport").child("Content").child("RoleItem(Clone)")[
                len(Supportinglist) - 1].child("HeadMask").wait(2)
            self.findClick_childobject(SuPOCO, description="次角色图像框", waitTime=1)

    def talk(self, name, txt="this Characterinput"):  # Narration系统说话
        """对话内容角色编对话方法 name：main,Narration，角色名称 名称不能超过7个字母否则无法找到txt："""
        if name == "main":
            print("主角色发言")
            object = self.poco("MainCharacter").child("HeadMask")
            self.findClick_childobject(object, description=name, waitTime=1)
            self.findClick_object("InputBar", "InputBar", description="点击输入框", waitTime=1, sleeptime=2)
            text(txt)
            print("输入内容：", txt)
            # self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312))
            if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
                pass
            else:
                self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                       description="点击提交按钮")
            return True
        list = self.poco("TxtName").wait(3)
        object = None
        for i in list:
            print(i.get_TMPtext())
            if i.get_TMPtext() == name:
                object = i
        if object:
            object = object.parent()
            self.findClick_childobject(object, description=name, waitTime=1)
            self.findClick_object("InputBar", "InputBar", description="点击输入框", waitTime=1, sleeptime=2)
            # self.poco("InputBar").click()
            text(txt)
            print("输入内容：", txt)
            if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
                pass
            else:
                self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                       description="点击提交按钮")
        else:
            print("未找到对应的角色,创建此角色")
            self.creatCharacter(name)

    def click_addChoice(self):
        """点击工具弹框添加选项按钮"""
        if self.find_try("BtnTool", description="工具弹框"):
            self.click_object("BtnTool", description="工具弹框按钮")
            if self.find_try("TutorialWindow", description="新书籍新手引导", waitTime=1):
                self.click_object("Close", description="关闭", sleeptime=1)
                self.click_object("BtnTool", description="工具弹框按钮")
            self.click_object("BtnChoice", description="添加选项")
        else:
            print("已经存在创建的选项")

    def editorOptionDES(self, OptionName, description):
        """修改选项描述，OptionA，OptionB"""
        POCO = self.poco(OptionName).child("InputField").child("Text Area")
        tXt = POCO.child("Text").get_TMPtext()
        self.findClick_childobject(POCO, description="A选择描述框")
        text(description)

    def click_Paperplanebutton(self):
        """内容提交按钮"""
        if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
            pass
        else:
            self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                   description="点击提交按钮")
    def click_confirm(self):
        """点击confirm按钮"""
        self.findClick_object("Button","Button",description="confirm", sleeptime=1)
    def click_con(self):
        """点击修改确认弹框按钮"""
        self.findClick_try("AlterView", "LeftBtn", description="修改确认弹框", waitTime=1, sleeptime=2)


    def creat_Choice(self, OptionName, description):
        """创建新选项
        OptionName-> 选项名称
         description  -> 选项描述 """
        if not self.find_try(OptionName, description="查看是否有" + OptionName + "选项"):
            self.findClick_childobject(self.poco("Create").child("OptionAdd"), description="创建一个新分支选项", sleeptime=1)
        else:log("已经存在{0}选项",format(OptionName))

    def intoOption(self, OptionName):
        """选择进入的选项编辑
        type:  A，B选择进入的
        """
        OptionNextPOCP = self.poco(OptionName).child("Next")
        sleep(2)
        self.findClick_childobject(OptionNextPOCP, description=OptionName + "选择选项分支场景", waitTime=5, sleeptime=2)

    def creatCharacter(self, name, characterType="supporting"):
        """name：角色名称characterType：角色类型main,supporting
        创建角色流程"""
        list = self.poco("TxtName").wait(10)
        object = None
        for i in list:
            print(i.get_TMPtext())
            if i.get_TMPtext() == name:
                print("角色已存在")
                return True
        self.characterUI(characterType)
        self.chooseHead()
        self.writeName(name)
        self.submitOK()

    def back_click(self):
        """返回上个界面按钮"""
        self.findClick_childobject(self.poco("TopBar").child("BtnBack"), description="返回到上一个界面", waitTime=2,
                                   sleeptime=2)

    def toolBar(self, type, Index=3):
        """分支工具界面
        Img ->添加图片
        Choice ->创建选项
        Jump - 设置跳转
        Index - jump 3,设置章节结束 其他未做
        """
        int(Index)
        self.click_object("BtnTool", description="点击工具按钮")
        if type == "Img":
            self.findClick_childobject(self.poco("ToolBar").child("BtnImg"), description="创建图片")
        if type == "Choice":
            self.findClick_childobject(self.poco("ToolBar").child("BtnChoice"), description="创建选项")
        if type == "Jump" and Index == 3:
            self.findClick_childobject(self.poco("ToolBar").child("BtnJump"), description="创建跳转")
            setEnd = self.poco("UIBottomForm").child("Buttons").child("Options").child("Button(Clone)")[Index]
            self.findClick_childobject(setEnd, description="设置章节结束", sleeptime=2)
        else:
            log(MyException, desc="填写了错误的下标", snapshot=True)

    def branchprocess(self):
        """分成创作页面流程"""
        self.click_addChoice()  #点击工具弹框添加选项按钮
        self.creat_Choice("OptionC","这是C选项") #创建新选项
        self.editorOptionDES("OptionC","这是C选项") #修改选项描述
        self.click_Paperplanebutton() #提交内容
        self.editorOptionDES("OptionA","这是A选项")
        self.click_Paperplanebutton()
        self.editorOptionDES("OptionB","这是B选项")
        self.click_Paperplanebutton()
        self.click_confirm() #点击confirm按钮
        # self.click_con()
        self.intoOption("OptionA")  #选择进入的选项编辑
        txt = "abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghi" \
              "jklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz"
        # self.creatCharacter("lipeng", "main")
        self.talk("lipeng", txt)
        self.talk("lilei", txt)
        self.toolBar("Jump")
        self.back_click()
        self.intoOption("OptionB")
        self.talk("lipeng", txt)
        self.talk("lilei", txt)
        self.toolBar("Jump")
        self.back_click()
        self.intoOption("OptionC")
        self.talk("lipeng", txt)
        self.talk("lilei", txt)
        self.toolBar("Jump")
        self.back_click()
        sleep(2)
        self.back_click()

    # def branchprocess(self):
    #     """封装好分支创作工作室流程"""
    #     txt = "abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghi" \
    #           "jklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz"
    #     self.LuaUIStudio()
    #     self.creatCharacter("lipeng", "main")
    #     self.creatCharacter("lilei")
    #     time = 2
    #     while (time > 0):
    #         time = time - 1
    #         self.talk("Narration", str(time))
    #         self.talk("lipeng", txt)
    #         self.talk("lilei", txt)
    #     self.branchprocess()

    def commonprocess(self):
        """封装好分支创作工作室流程"""
        txt = "abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghi" \
              "jklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz"
        self.LuaUIStudio()
        self.creatCharacter("lipeng", "main")
        self.creatCharacter("lilei")
        time = 2
        while (time > 0):
            time = time - 1
            self.talk("Narration", str(time))
            self.talk("lipeng", txt)
            self.talk("lilei", txt)
        self.branchprocess()


MainStudio1 = MainStudio()
MainStudio1.commonprocess()
