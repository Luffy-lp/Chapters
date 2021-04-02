from airtest.core.api import *
from common.COM_findobject import FindObject
from common.my_log import mylog
from date.Chapters_data import MyData
class BookLoad(FindObject):
    BookLoad_info={}
    def __init__(self):
        FindObject.__init__(self)

    def bookLoad(self,bookid=None):
        """书籍加载"""
        if self.find_try("DefaultBg", description="书籍加载界面", waitTime=2, tryTime=2):
            startime = time.time()
            while self.poco("DefaultBg").wait(3).exists():
                loadtime = time.time() - startime
                if MyData.UserData_dir["bookDetailInfo"]["BookID"]:
                    MyData.download_bookresource(MyData.UserData_dir["bookDetailInfo"]["BookID"])
                else:
                    MyData.UserData_dir["bookDetailInfo"]["BookID"]=bookid
                    MyData.download_bookresource(bookid)
                sleep(2)
                if self.find_try("Discover",description="是否返回大厅",waitTime=1):
                    mylog.error("加载书籍异常")
                    log(Exception("加载书籍异常，自动返回到大厅"),snapshot=True)
                    raise Exception("加载书籍异常，自动返回到大厅")
                print("书籍加载中", loadtime)
                if loadtime > 360:
                    self.findClick_object("HomeBtn", "HomeBtn", description="加载书籍超时,返回大厅")
                    mylog.error("加载书籍超时")
                    log(loadtime, timestamp=time.time(), desc="加载书籍超时", snapshot=True)
                    raise Exception("加载书籍超时")
            loadtime = time.time() - startime
            self.BookLoad_info["书籍加载时间："]=loadtime
            print("完成书籍加载，加载时间为{0}秒".format(loadtime))
            log(loadtime, timestamp=time.time(), desc="完成书籍加载", snapshot=True)
        return True