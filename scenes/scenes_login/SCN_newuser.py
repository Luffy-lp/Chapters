from common.COM_findobject import CommonPoco
from airtest.core.api import *

class NewUserGuide(CommonPoco):
    def __init__(self):
        CommonPoco.__init__(self)
    def newUserPopUp(self):
        """新手引导"""
        if self.find_try( "UINewGuide", description="新手引导选择类型界面", waitTime=2,sleeptime=3):
            sleep(3)
            self.click_object( "Skip",description="skip跳过新手引导",waitTime=5)
            return True,"弹出新手引导"
        else:
            print("无新手引导")
            return False,"未弹出新手引导"
