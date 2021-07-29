import time

from airtest.core.api import assert_equal
from common.COM_findobject import FindObject, log
from date.Chapters_data import MyData


# TODO:概率出现未成功点击书籍的

class BookNewDetail(FindObject):
    BookNewDetail_info = {}
    __instance = None

    def __init__(self):
        FindObject.__init__(self)

    def bookNewDetailPOP(self):
        if self.find_try("UIVisualDetailView", "书籍详情页", waitTime=2):
            self.UIAlterPoP()

    def getBookNewDetail_info(self, BookID, UIbookName):
        Bookname = MyData.Stroy_data_dir[BookID]
        print("接口查询的书籍名称：", Bookname)
        self.BookNewDetail_info["BookName"] = UIbookName
        self.BookNewDetail_info["BookID"] = BookID
        MyData.UserData_dir["bookDetailInfo"] = self.BookNewDetail_info
        print(MyData.UserData_dir)
        return True

    def get_readBookInfo(self):
        print("书籍类型检测")
        data = MyData.getBookInfo(uuid=MyData.UserData_dir["uuid"], bookId=MyData.bookInfo_dir["BookID"])
        self.BookNewDetail_info["sequel_from"] = data["sequel_from"]

    def book_chapters(self, index):
        self.poco("TestInput").wait(1).set_text(index)
        self.click_object("TestInput", description="搜索框")
        self.click_object("UIVisualDetailView", description="详情页")

    def book_Play(self, index=None):
        """新版本的play"""
        self.get_readBookInfo()
        self.book_chapters(index)
        if self.findClick_object("Play", "Play", description="Play按钮", waitTime=5):
            pass
        else:
            self.findClick_object("DaypassPlay", "DaypassPlay", description="Daypass按钮", waitTime=1)
        if self.BookNewDetail_info["sequel_from"]:
            self.findClick_try("UpBtn", "UpBtn", description="Yes,I do")
        if int(MyData.UserData_dir["diamond"]) < 4999:
            MyData.updateUsercurrency("diamond", "4999")
        if int(MyData.UserData_dir["ticket"]) < 99:
            MyData.updateUsercurrency("ticket", "99")
        return True

    # def book_Play(self, index=None):
    #     self.get_readBookInfo()
    #     if index:
    #         try:
    #             POCO = self.poco("chapterBtn(Clone)")[int(index) - 1]
    #             self.findClick_childobject(POCO, description="选择第{}章".format(index), waitTime=3)
    #         except:
    #             try:
    #                 self.click_close()
    #                 self.click_object("SearchBtn", description="bookid搜索按钮", waitTime=1)
    #                 self.bookNewDetailPOP()
    #                 POCO = self.poco("chapterBtn(Clone)")[int(index) - 1]
    #                 self.findClick_childobject(POCO, description="选择第{}章".format(index), waitTime=3)
    #             except:
    #                 log(Exception("{}章节不存在请查询章节是否上传.......".format(index)))
    #     if self.find_try("Play", description="Play按钮", waitTime=1):
    #         self.findClick_object("Play", "Play", description="Play按钮", waitTime=1)
    #         if self.BookNewDetail_info["sequel_from"]:
    #             self.findClick_try("UpBtn", "UpBtn", description="Yes,I do")
    #         if self.UIAlterPoP():
    #             self.findClick_object("Play", "Play", description="Play按钮", waitTime=1)
    #             if self.BookNewDetail_info["sequel_from"]:
    #                 self.findClick_try("UpBtn", "UpBtn", description="Yes,I do")
    #     else:
    #         self.findClick_object("DaypassPlay", "DaypassPlay", description="Daypass按钮", waitTime=1)
    #     if int(MyData.UserData_dir["diamond"]) < 4999:
    #         MyData.updateUsercurrency("diamond", "4999")
    #     if int(MyData.UserData_dir["ticket"]) < 99:
    #         MyData.updateUsercurrency("ticket", "99")
    #     return True

    def click_close(self):
        """详情页关闭按钮"""
        self.findClick_try("UIVisualDetailView", "Close", description="关闭详情页按钮")

    def click_Reset(self, type="SetBook"):
        """SetBook,SetChapter"""
        if self.findClick_object("BottomBg", "Reset", description="重置按钮"):
            if type == "SetBook":
                self.findClick_object("UIRestart", "SetBook", description="重置书籍", sleeptime=0.5)
                self.poco("Mask").child("Button").click()
                print("关闭Reset界面")
                return True
            elif type == "SetChapter":
                self.findClick_object("UIRestart", "SetChapter", description="重置章节", sleeptime=0.5)
                self.poco("UIVisualDetailView").child("Button").click()
                return True

    def bookChoose_Shelf(self, bookShelf, index):
        """找到书架招数WeekView"""
        index = int(index)
        View = bookShelf + "View"
        Scr = bookShelf + "Scr"
        Myboopoco = self.poco(bookShelf)
        self.find_object(bookShelf, description=bookShelf + "书架")
        self.findSwipe_object(bookShelf, 0.5, POCOobject=Myboopoco, swipeTye="y")  # 滑动找书架
        while (True):
            try:
                thebook = \
                    self.poco(View).child(Scr).child("Viewport").child("Content").child("0(Clone)")[
                        index].wait(5)
                UIbookName = thebook.child("TextName").wait(2).get_TMPtext()
                print("页面显示的书籍名称：", UIbookName)
                POCOclik = thebook.child("Image")
                print("POCOclik:", POCOclik.get_position())
                BookID = MyData.Bookshelf__dir["Weekly Update"][index]
                print("BookID:", BookID)
                Bookname = self.getBookNewDetail_info(BookID, UIbookName)
                self.findClick_childobject(POCOclik, description="点击书籍封面", waitTime=5, sleeptime=1)
                self.bookNewDetailPOP()
                return True, Bookname, self.BookNewDetail_info  # 接口书籍名称，当前详情页书籍信息
            except:
                print("未能点击对应的书籍")
                if index <= 5:
                    index = index + 1
                else:
                    return False, None
        time.sleep(3)

    def bookChoose(self, bookShelf, index=0):
        """Discover Banner,Weekly,Mybook，Search，testSearh"""
        index = int(index)
        if bookShelf == "Banner":
            # print("数据库中大厅banner书籍以及阅读进度", self.Bookshelf__dir["readprogressList"])
            self.find_object("ScrollHot", description="大厅banner的书籍滑动控件")  # 获取第一个大厅banner的书籍滑动控件type :  ScrollRect
            POCO = self.poco("ScrollView").child("Viewport").offspring("ScrollHot").offspring("Content").child("0")[1]
            if self.findchildobject_try(POCO, description="大厅banner"):
                self.findClick_childobject(POCO, description="大厅banner")
            banner_list = self.poco("ScrollHot").child("Viewport").child("Content").children()
            for i in banner_list:
                print("banner滑动图", i.get_name())
            print("banner滑动图的长度：", len(banner_list))
            if len(banner_list) != 4:
                assert_equal(False, True, "banner滑动图数量异常!")
                return
            else:
                self.findClick_childobject(banner_list[1], description="点击第二个滑动banner滑动图", sleeptime=3)
                self.bookNewDetailPOP()
            BookID = MyData.Bookshelf__dir["banner_data"][index]
            print("BookID:", BookID)
            UIbookName = self.poco("TitleScr").offspring("BookTitle").wait(2).get_TMPtext()
            Bookname = self.getBookNewDetail_info(BookID, UIbookName)
            print("Bookname:", Bookname)
            print("UIbookName:", UIbookName)
            return True, Bookname, self.BookNewDetail_info
        if bookShelf == "Weekly":
            # "获取书籍的名称"
            Myboopoco = self.poco("WeekView")
            self.find_object("WeekView", description="周排行书架")  # 找书架
            self.findSwipe_object("WeekView", 0.5, POCOobject=Myboopoco, swipeTye="y")  # 滑动找书架
            time.sleep(3)
            while (True):
                try:
                    thebook = \
                        self.poco("WeekView").child("WeekScr").child("Viewport").child("Content").child("0(Clone)")[
                            index].wait(5)
                    UIbookName = thebook.child("TextName").wait(2).get_TMPtext()
                    print("页面显示的书籍名称：", UIbookName)
                    POCOclik = thebook.child("Image")
                    print("POCOclik:", POCOclik.get_position())
                    BookID = MyData.Bookshelf__dir["Weekly Update"][index]
                    print("BookID:", BookID)
                    Bookname = self.getBookNewDetail_info(BookID, UIbookName)
                    self.findClick_childobject(POCOclik, description="点击书籍封面", waitTime=5, sleeptime=1)
                    self.bookNewDetailPOP()
                    return True, Bookname, self.BookNewDetail_info  # 接口书籍名称，当前详情页书籍信息
                except:
                    print("未能点击对应的书籍")
                    if index <= 5:
                        index = index + 1
                    else:
                        return False, None
        if bookShelf == "Mybook":
            print("选择Mybook书架")
            Myboopoco = self.poco("MybookView")
            self.find_object("MybookView", description="Mybook书架")  #
            self.findSwipe_object("MybookView", 0.5, POCOobject=Myboopoco, swipeTye="y")
            while (True):
                try:
                    thebook = \
                        self.poco("MybookView").child("MybookScr").child("Viewport").child("Content").child("0(Clone)")[
                            index].wait(3)
                    bookName = thebook.child("TextName").wait(2).get_TMPtext()
                    print("发现对应的书籍", bookName)
                    POCO = thebook.child("Reading").click()
                    self.findClick_childobject(POCO, description="点击书籍", waitTime=1, sleeptime=3)
                    bookName = bookShelf + ":" + bookName
                    return True, bookName
                except:
                    print("未能点击对应的书籍，退出")
                    if index <= 5:
                        index = index + 1
                    else:
                        return False
