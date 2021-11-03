from airtest.core.api import *
from common.COM_findobject import FindObject



class Community(FindObject):
    """短信小说社区主页"""

    def __init__(self):
        FindObject.__init__(self)
        # self.storiesPOP()

    def into_workshop(self):
        """进入工作室"""
        self.findClick_object("UINewBookRack", "CreateBtn", description="进入工作室", sleeptime=2)
        return True

    def storiesPOP(self):
        """短信小说弹框处理"""
        self.find_object("UINewBookRack", description="短信小说界面", waitTime=1)
        if self.find_try("UISignActivity", description="短信小说日历奖励", waitTime=1):
            self.click_object("Claim", description="领取日历奖励")
            self.findClick_object("UIClaimReward", "BtnGet", description="短信小说日历奖励", waitTime=1)
            self.click_object("Back", description="关闭日历奖励")