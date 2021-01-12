from common.COM_findobject import CommonPoco
from common.COM_data import MyData

class Discover(CommonPoco):
    def __init__(self):
        CommonPoco.__init__(self)

    def discoverPopup(self):  # 积分弹框
        """大厅弹框检查"""
        self.heartBeat()
        print(MyData.popup_dir[0])
        poplist = MyData.popup_dir[0]
        for k in poplist:
            self.findClick_try(k["args"][0],k["args"][1],description=k["func_name"], waitTime=0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UITwentyFourHourReward", "BtnGet", "24小时新手礼包", waitTime=0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UISignActivity", "Back", "月签到活动", waitTime=0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UIGetLoginCredit", "FreeBtn", "每日登陆积分", 0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UIDailyLoginRewardABTest", "ClaimtBtn", "一日三签活动弹框", 0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UITreasureHint", "sure", "宝箱弹框", 0.2, tryTime=1, sleeptime=3)
        # self.findClick_try("UIGetOffCredit", "GetBtn", "用户登陆奖励", 0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("UIPrivacyPopup", "BtnAccept", "游戏条款", 0.2, tryTime=1, sleeptime=2)
        # self.findClick_try("LuaUIThanksPopup", "Back", "答谢弹框", 0.2, tryTime=1, sleeptime=2)
        if self.find_try("UIGiftPopup", "推送礼包", 0.2, tryTime=1, sleeptime=2):
            self.findClick_try("GiftShake", "GiftBag3", "礼物", 0.2, tryTime=1, sleeptime=2)
            self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
            self.findClick_try("UIBagItemReward", "BtnRead", "背包道具推送", 0.2, tryTime=1, sleeptime=2)
        return True, CommonPoco.Popuplist
