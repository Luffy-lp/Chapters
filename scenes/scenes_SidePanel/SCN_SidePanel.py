from common.COM_findobject import FindObject


class SidePanel(FindObject):
    def __init__(self):
        FindObject.__init__(self)
    def click_language(self):
        self.click_object("language",description="语言选择界面",sleeptime=1)
    def click_back(self):
        self.click_object("back",description="返回",sleeptime=1)