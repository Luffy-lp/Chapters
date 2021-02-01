from common.COM_findobject import FindObject
from airtest.core.api import *

class NewUserGuide(FindObject):
    def __init__(self):
        FindObject.__init__(self)
    def newUserPopUp(self):
        """新手引导"""
        if self.find_try( "UINewGuide", description="新手引导选择类型界面", waitTime=2,sleeptime=3):
            # self.click_object("Skip",description="skip跳过新手引导",waitTime=5)
            self.up_use_render__Click_try("Skip","Skip",description="skip跳过新手引导",waitTime=5)
            return True,"弹出新手引导"
        else:
            print("无新手引导")
            return False,"未弹出新手引导"