from time import sleep

from common.COM_devices import CommonDevices
from common.COM_findobject import CommonPoco
from common.COM_data import MyData

class Discover(CommonPoco):
    def __init__(self):
        CommonPoco.__init__(self)

    def discoverPopup(self):  # 积分弹框
        """大厅弹框检查"""
        poplist = MyData.popup_dir[0]
        this = True
        self.UIAlterPoP()
        while this:
            if self.poco("PopupPanel").children():
                child = self.poco("PopupPanel").child(nameMatches="^UI.*", visible=True)
                for list in child:
                    listname = list.get_name()
                    print("listname:", listname)
                    for k in poplist:
                        if listname==k["args"][0]:
                            if listname == "UIGiftPopup":
                                if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1):
                                    self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=5)
                                    self.findClick_try("UIBagItemReward", "BtnStore", "会员卡", 0.2, tryTime=1, sleeptime=2)
                                    self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
                            else:
                                self.findClick_try(k["args"][0], k["args"][1], description=k["func_name"], waitTime=0.2,
                                                   tryTime=1, sleeptime=2)
            elif self.poco("PopUpPanel").children():
                child1 = self.poco("PopUpPanel").child(nameMatches="^UI.*", visible=True)
                for list in child1:
                    listname = list.get_name()
                    print("listname:", listname)
                    for k in poplist:
                        if listname==k["args"][0]:
                            if listname == "UIGiftPopup":
                                if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1):
                                    self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=5)
                                    self.findClick_try("UIBagItemReward", "BtnStore", "会员卡", 0.2, tryTime=1, sleeptime=2)
                                    self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
                            else:
                                self.findClick_try(k["args"][0], k["args"][1], description=k["func_name"], waitTime=0.2,
                                                   tryTime=1, sleeptime=2)
            else:
                this = False
        return True, CommonPoco.Popuplist
# Discover1=Discover()
# Discover1.discoverPopup()

