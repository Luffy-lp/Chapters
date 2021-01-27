import time

from airtest.core.api import assert_equal
from common.COM_findobject import CommonPoco
from pages.bookdetail.page_bookdetail import PagBookDetail
from common.COM_data import MyData

# TODO:概率出现未成功点击书籍的

class BookNewDetail(CommonPoco):
    BookNewDetail_info = {}
    __instance = None

    def __init__(self):
        CommonPoco.__init__(self)

    def bookNewDetailPOP(self):
        # self.find_object("UIBookNewDetail", "书籍详情页", waitTime=2, tryTime=10)
        print("详情页弹框配置：",MyData.popup_dir[1])
        poplist = MyData.popup_dir[1]
        for k in poplist:
            if k["args"][0]=="UIAlter":
                self.UIAlterPoP()
            if k["args"][0]=="UIPassGuide":
                while (self.find_try("UIPassGuide", description="道具票使用", waitTime=0.5, tryTime=1)):
                    self.findClick_object("UIPassGuide", "Close", description="Close按钮")
                    self.findClick_object("UIPassGuide", "ExitBtn", description="Exit按钮")
            else:
                self.findClick_try(k["args"][0],k["args"][1],description=k["func_name"], waitTime=0.2, tryTime=1, sleeptime=2)

    def bookChoose(self, bookShelf, index=0):
        """Discover Banner,Weekly,Mybook，Search，testSearh"""
        index = int(index)
        if bookShelf == "Banner":
            # print("数据库中大厅banner书籍以及阅读进度", self.Bookshelf__dir["readprogressList"])
            self.find_object("ScrollHot", description="大厅banner的书籍滑动控件")  # 获取第一个大厅banner的书籍滑动控件type :  ScrollRect
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
            print("BookID:",BookID)
            UIbookName = self.poco("TitleScr").offspring("BookTitle").wait(2).get_TMPtext()
            Bookname = self.getBookNewDetail_info(BookID, UIbookName)
            print("Bookname:",Bookname)
            print("UIbookName:",UIbookName) 
            return True, Bookname, self.BookNewDetail_info
        if bookShelf == "Weekly":
            # "获取书籍的名称"
            Myboopoco = self.poco("WeekView")
            self.find_object("WeekView", description="周排行书架")
            self.findSwipe_object("WeekView", 0.5, POCOobject=Myboopoco, swipeTye="y")
            time.sleep(3)
            while (True):
                try:
                    thebook = \
                        self.poco("WeekView").child("WeekScr").child("Viewport").child("Content").child("0(Clone)")[
                            index].wait(5)
                    UIbookName = thebook.child("TextName").wait(2).get_TMPtext()
                    print("页面显示的书籍名称：", UIbookName)
                    POCOclik = thebook.child("Image")
                    print("POCOclik:",POCOclik.get_position())
                    BookID = MyData.Bookshelf__dir["Weekly Update"][index]
                    print("BookID:",BookID)
                    Bookname = self.getBookNewDetail_info(BookID, UIbookName)
                    self.findClick_childobject(POCOclik,description="点击书籍封面",waitTime=5,sleeptime=1)
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

    def getBookNewDetail_info(self, BookID, UIbookName):
        Bookname = MyData.Stroy_data_dir[BookID]
        print("接口查询的书籍名称：", Bookname)
        self.BookNewDetail_info["BookName"] = UIbookName
        self.BookNewDetail_info["BookID"] = BookID
        MyData.UserData_dir["bookDetailInfo"] = self.BookNewDetail_info
        print(MyData.UserData_dir)
        return True

    # def bookNewDetailData(self):
    #     Booklist = []
    #     BookTitle = self.poco("TitleScr").child("Content").child("BookTitle")
    #     Bookname = BookTitle.get_TMPtext()
    #     Booklist.append({"Bookname": Bookname})
    #     return True, Booklist

    def book_Play(self):
        self.findClick_object("Play", "Play", description="Play按钮")
        return True

    def click_close(self):
        if self.findClick_object("Mask", "Button", description="关闭详情页按钮"):
            return True

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
                self.poco("Mask").child("Button").click()
                return True