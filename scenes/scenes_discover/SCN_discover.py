from common.COM_findobject import CommonPoco
from common.COM_data import MyData

class Discover(CommonPoco):
    def __init__(self):
        CommonPoco.__init__(self)

    def discoverPopup(self):  # 积分弹框
        """大厅弹框检查"""
        print(MyData.popup_dir[0])
        poplist = MyData.popup_dir[0]
        for k in poplist:
            if k["args"][0]=="UIAlter":
                self.heartBeat()
            if k["args"][0]=="UIGiftPopup":
                if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1, sleeptime=2):
                    self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=2)
                    self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
                    self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
            else:
                self.findClick_try(k["args"][0],k["args"][1],description=k["func_name"], waitTime=0.2, tryTime=1, sleeptime=2)
        return True, CommonPoco.Popuplist
