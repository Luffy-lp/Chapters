from airtest.core.api import log

from common import COM_utilities
from date.Chapters_data import MyData
from common.COM_findobject import FindObject

class Discover(FindObject):
    discoverPopup_info={}
    def __init__(self):
        FindObject.__init__(self)
    def discoverPopup(self):  # 积分弹框
        """大厅弹框检查"""
        self.Popuplist=[]
        poplist = MyData.popup_dir[0]
        FullScreenPanellist = MyData.popup_dir[2]
        havePopup = True
        self.UIAlterPoP()
        COM_utilities.clock()  # 插入计时器

        while havePopup:
            print("进入弹框判断")
            mytime = float(COM_utilities.clock("stop"))
            if mytime > 60:
                log(Exception("弹框处理超时...."),snapshot=True)
                raise Exception
            if self.poco("FullScreenPanel").children():
                if FullScreenPanellist:
                    for k in FullScreenPanellist:
                        self.findClick_try(k["args"][0], k["args"][1], description=k["func_name"], waitTime=1,
                                           tryTime=1, sleeptime=2)
            if self.poco("PopupPanel").children():
                print("进入PopupPanel弹框判断")
                list1 = []
                child = self.poco("PopupPanel").child(nameMatches="^UI.*", visible=True)
                for list in child:
                    listname = list.get_name()
                    list1.append(list)
                list1.sort(key=lambda x: x.attr('_ilayer'), reverse=False)
                listname=list1[len(list1) - 1].get_name()
                print("listname:", listname)
                for k in poplist:
                    if listname==k["args"][0]:
                        if listname == "UIGiftPopup":
                            if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1):
                                self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=5)
                                self.findClick_try("UIBagItemReward", "BtnStore", "会员卡", 0.2, tryTime=1, sleeptime=1)
                                self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=1)
                        else:
                            self.findClick_try(k["args"][0], k["args"][1], description=k["func_name"], waitTime=1,tryTime=1, sleeptime=2)
            elif self.poco("PopUpPanel").children():
                print("进入PopUpPanel弹框判断")
                try:
                    child1 = self.poco("PopUpPanel").child(nameMatches="^UI.*", visible=True)
                    for list in child1:
                        listname = list.get_name()
                        print("listname:", listname)
                        for k in poplist:
                            if listname==k["args"][0]:
                                if listname == "UIGiftPopup":
                                    if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1):
                                        self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=5)
                                        self.findClick_try("UIBagItemReward", "BtnStore", "会员卡", 0.2, tryTime=1, sleeptime=1)
                                        self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=1)
                                else:
                                    self.findClick_try(k["args"][0], k["args"][1], description=k["func_name"], waitTime=1,
                                                       tryTime=1, sleeptime=0.5)
                except:
                    print("PopUpPanel非点击弹框")
            else:
                print("判断当前无弹框")
                havePopup = False
            self.discoverPopup_info["弹框列表："]=FindObject.Popuplist
        return True