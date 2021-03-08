from airtest.core.api import touch

from common import COM_utilities
from common.COM_data import MyData
from common.COM_findobject import FindObject
from scenes.scenes_discover.SCN_discover import Discover


class PageTurn(FindObject):
    def __init__(self):
        FindObject.__init__(self)

    def Bottom_click(self, index):
        """0~4对应底部主场景"""
        index = str(index)
        if self.find_object("Bottom", description="底部跳转", waitTime=float(MyData.EnvData_dir["sleepLevel"])):
            Bottom = self.poco("Bottom").child(index)
            self.findClick_childobject(Bottom, description="底部跳转到" + index,
                                       waitTime=3 + float(MyData.EnvData_dir["sleepLevel"]))
            if index == "0":  # 如果跳转到大厅后需要检查弹框
                myDiscover = Discover()
                myDiscover.discoverPopup()
                return True

    def Upper_click(self, type):
        """chapters,credit,ticket,diamond"""
        if self.find_object("Bottom"):
            if type == "chapter":
                self.poco("Upper").child("Chapter").click()
                print("打开侧边栏")
            if type == "credit":
                self.poco("Upper").child("CreditBtn").click()
                print("点击积分")
            if type == "ticket":
                self.poco("Upper").child("TicketBtn").click()
                print("返回创作")
            if type == "diamond":
                self.poco("Upper").child("DiamondBtn").click()
                print("返回创作")

    def click_close(self):
        self.findClick_object("Mask", "Button", description="关闭按钮")

    def click_pos(self,x,y):
        x=float("0."+x)
        y=float("0."+y)
        touch(COM_utilities.PosTurn([x,y]))
