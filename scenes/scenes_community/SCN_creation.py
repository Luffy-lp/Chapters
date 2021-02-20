from common.COM_findobject import FindObject, log
from common.COM_utilities import clock


class Creation(FindObject):
    """创建短信小说"""

    def __init__(self):
        FindObject.__init__(self)
        # self.workshop()

    def workshop(self):
        self.find_object("LuaUIStudio", description="作者小说列表界面", waitTime=10)
        self.findClick_try("UIWriterIntroduceDlg", "BtnOK", description="创作小说条款",waitTime=3)

    def click_createNewBook(self):
        """创建新小说+"""
        POCO=self.poco("CoverMask").child("Text")
        clock()
        while not self.findchildobject_try(POCO,description="新增小说按钮",waitTime=1):
            self.poco.swipe([0.5, 0.5], [0.5, 0.1], duration=1.0)
            mytime = float(clock("stop"))
            if mytime > 60:
                print("查找新增小说按钮失败")
                log(Exception("查找新增小说按钮失败"),snapshot=True)
                raise Exception("查找新增小说按钮失败")

        createMask = self.poco("CoverMask").child("Text")
        pos = createMask.get_position()
        print("pos:",pos[1])
        if pos[1] > 0.9:
            self.findSwipe_object("CoverMask", 0.9, POCOobject=createMask)
        self.findClick_childobject(createMask, description="创建新小说", sleeptime=1)

    def click_back(self):
        """返回上一界面"""
        self.findClick_object("LoopListView", "BtnBack", description="返回到短信小说界面", waitTime=1)

    def select_genre(self):
        """选择小说类型界面"""
        print("选择小说类型界面")
        ContentPOCO = self.poco("Content").child("Item(Clone)")[0].wait(1).child("TxtName")
        self.findClick_childobject(ContentPOCO, description="选择类型", waitTime=2, sleeptime=1)
        self.findClick_object("LuaUICategory", "BtnNext", "下一步", waitTime=1, sleeptime=1)

    def storiesPOP(self):
        self.find_object("UINewBookRack", description="短信小说界面", waitTime=3)

    def process_createNewBook(self):
        self.workshop()
        self.click_createNewBook()
        self.mysleep(2)
        self.select_genre()
        return  True