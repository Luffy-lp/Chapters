from airtest.core.api import touch, sleep

from common import COM_utilities
from date.Chapters_data import MyData
from common.COM_findobject import FindObject
from scenes.scenes_discover.SCN_discover import Discover


class PageTurn(FindObject):
    # def __init__(self):
    #     FindObject.__init__(self)
    def getState(self):
        self.find_try("DiscoverCanvas")

    def get_HomePOS(self):
        """跳转按钮位置获取"""
        pos = self.poco("Home").get_position()
        if MyData.DeviceData_dir["offset"]:
            print(MyData.DeviceData_dir["offset"])
            pos[1] += MyData.DeviceData_dir["offset"]
        pos= COM_utilities.PosTurn(pos)
        # self.poco("Text (TMP)").click()
        return pos

    def Bottom_click(self, index):
        """0~4对应底部主场景"""
        index = str(index)
        if index == "0":
            time=5
            while self.find_try("Home",description="小房子"):

                time-=1
                if time<0:
                    return
                pos =self.get_HomePOS()
                touch(pos)
                sleep(1)
        if self.find_object("Bottom", description="底部跳转", waitTime=3):
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
                print("票入口进入商城")
            if type == "diamond":
                self.poco("Upper").child("DiamondBtn").click()
                print("钻石入口进入商城")

    def click_close(self):
        self.findClick_object("Mask", "Button", description="关闭按钮")

    def click_pos(self, x, y):
        x = float("0." + x)
        y = float("0." + y)
        pos = [x, y]
        touch(COM_utilities.PosTurn(pos))
        print("点击位置:", COM_utilities.PosTurn(pos))
    def click_back(self):
        """返回上个界面按钮"""
        self.findClick_childobject(self.poco("BtnBack"), description="返回到上一个界面", waitTime=2,sleeptime=2)
        # MYMainStudio.back_click()
        # sleep(2)
        # MYMainStudio.back_click()
    # def exit_click():
    #     """返回上个界面按钮"""
    #     MyData.DeviceData_dir["poco"].findClick_object("BtnBack", "BtnBack", description="Exit按钮", waitTime=2,sleeptime=2)
