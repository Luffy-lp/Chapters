from common import COM_utilities
from common.COM_data import MyData
from common.COM_findobject import FindObject
from common.COM_utilities import *

class SidePanel(FindObject):
    def __init__(self):
        FindObject.__init__(self)
    def click_language(self):
        self.click_object("language",description="语言选择界面",sleeptime=1)
    def click_back(self):
        self.click_object("back",description="返回",sleeptime=1)