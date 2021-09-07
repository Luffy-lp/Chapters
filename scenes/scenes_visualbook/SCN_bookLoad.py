from airtest.core.api import *

from common import COM_utilities
from common.COM_findobject import FindObject
from common.my_log import mylog
from date.Chapters_data import MyData
class BookLoad(FindObject):
    BookLoad_info={}

    def __init__(self):
        FindObject.__init__(self)
        self._POS = COM_utilities.PosTurn([0.5, 0.6])

    def bookLoad(self,bookid=None):
        """书籍加载DefaultBg"""
        startime = time.time()
        while self.find_try("ChapterLoad", description="书籍加载界面", waitTime=3):
            loadtime = time.time() - startime
            if loadtime > 2000:
                self.findClick_object("HomeBtn", "HomeBtn", description="加载书籍超时,返回大厅")
                # log(loadtime, timestamp=time.time(), desc="加载书籍超时", snapshot=True)
                log(Exception("加载书籍异常"),snapshot=True)
                raise Exception("加载书籍超时")
        if self.find_try("SceneBG", description="书籍场景", waitTime=5, tryTime=3):
            loadtime = time.time() - startime
            self.BookLoad_info["书籍加载时间："]=loadtime
            log("完成书籍加载，加载时间为{0}秒".format(loadtime), timestamp=time.time(), desc="完成书籍加载", snapshot=True)
            return True
        else:
            log(Exception("加载书籍异常"), snapshot=True)
            raise Exception("加载书籍超时")

