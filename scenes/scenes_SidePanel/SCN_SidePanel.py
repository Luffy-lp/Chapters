from airtest.core.api import touch

from common import COM_utilities
from common.COM_findobject import FindObject


class SidePanel(FindObject):
    def __init__(self):
        FindObject.__init__(self)
    def click_language(self):
        self.click_object("language",description="语言选择界面",sleeptime=1)
    def click_back(self):
        self.click_object("back",description="返回",sleeptime=1)
    def click_help(self):
        self.click_object("help",description="帮助",sleeptime=1)
    def click_pos(self, x, y):
        x = float("0." + x)
        y = float("0." + y)
        pos = [x, y]
        touch(COM_utilities.PosTurn(pos))
        print("点击位置:", COM_utilities.PosTurn(pos))