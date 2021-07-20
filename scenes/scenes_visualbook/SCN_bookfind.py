import time

from airtest.core.api import assert_equal, text, keyevent
from common.COM_findobject import FindObject, log
from date.Chapters_data import MyData

# TODO:概率出现未成功点击书籍的

class Bookfind(FindObject):
    Bookfind_info = {}

    def __init__(self):
        FindObject.__init__(self)

    # def bookNewDetailPOP(self):

        # self.find_object("UIBookNewDetail", "书籍详情页", waitTime=2, tryTime=10)
        # print("详情页弹框配置：",MyData.popup_dir[1])
        # poplist = MyData.popup_dir[1]
        # for k in poplist:
        #     if k["args"][0]=="UIAlter":
        #         self.UIAlterPoP()
        #     if k["args"][0]=="UIPassGuide":
        #         while (self.find_try("UIPassGuide", description="道具票使用", waitTime=0.5, tryTime=1)):
        #             self.findClick_object("UIPassGuide", "Close", description="Close按钮")
        #             self.findClick_object("UIPassGuide", "ExitBtn", description="Exit按钮")
        #     else:
        #         self.findClick_try(k["args"][0],k["args"][1],description=k["func_name"], waitTime=0.2, tryTime=1, sleeptime=2)
    # def bookChoose(self):
    def bookChoose_Search(self,bookName):
        """通过书籍名称查找"""
        self.findClick_object("SearchBar","SearchBar",description="查询按钮")
        text(bookName)
        time.sleep(3)
        POCO=self.poco("BookItem(Clone)")[0].offspring("Image")
        self.findClick_childobject(POCO,description="书籍封面")
        POCO.click()
        time.sleep(2)
        POCO.click()

    def bookChoose_bookid(self,bookid):
        """通过书籍ID查找"""
        self.poco("InputField").set_text(bookid)
        self.click_object("SearchBtn",description="bookid搜索按钮",waitTime=1,sleeptime=2)
        if self.find_try("UIBookNewDetail", "书籍详情页", waitTime=2):
            self.UIAlterPoP()
        elif self.find_try("UIBookErrorEmail", "书籍详情页"):
            log(Exception("书籍不存在"),snapshot=True)
        else:
            log(Exception("查找书籍异常原因未知"), snapshot=True)
        # self.bookNewDetailPOP()
    def bookChoose_Shelf(self,bookShelf,index):
        """找到书架招数WeekView"""
        index = int(index)
        View=bookShelf+"View"
        Scr=bookShelf+"Scr"
        Myboopoco = self.poco(View)
        self.find_childobject(Myboopoco, description=bookShelf+"书架")
        self.findSwipe_object(bookShelf, 0.5, POCOobject=Myboopoco, swipeTye="y") #滑动找书架
        while True:
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

    def getBookNewDetail_info(self, BookID, UIbookName):
        Bookname = MyData.Stroy_data_dir[BookID]
        print("接口查询的书籍名称：", Bookname)
        self.BookNewDetail_info["BookName"] = UIbookName
        self.BookNewDetail_info["BookID"] = BookID
        MyData.UserData_dir["bookDetailInfo"] = self.BookNewDetail_info
        print(MyData.UserData_dir)
        return True

# Bookfind1=Bookfind()
# aa=Bookfind1.find_try("Discover",description="大厅")
# print(aa)

# # # if Bookfind1.poco("NormalSayRoleLeft").offspring("Body"):
# # #    aaa= Bookfind1.poco("NormalSayRoleLeft").offspring("Body").get_SpriteRenderer()
# # #    print(aaa)
# Bookfind1.traversal()