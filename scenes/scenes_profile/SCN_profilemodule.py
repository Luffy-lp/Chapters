import time
from airtest.core.api import *
from pages.userinfo.profile import Profile
from common.COM_findobject import CommonPoco
from airtest.core.api import touch
from airtest.core.cv import Template
import sys
from common.COM_utilities import *

class Profilemodule(Profile):
    Profilemodule_info = {}

    def swipe_head(self):
        """滑动个人信息的头像"""
        AchievementPOCO = self.poco("UserInfoVeiw").child("Head")
        self.findSwipe_object("AchievrmentPOCO", 0.1, POCOobject=AchievementPOCO, swipeTye="y",beginPos=[0.4,0.6])

    def swipe_Card(self):
        """移动Card标题"""
        Cardtitle = self.poco("Card").child("Title")
        self.findSwipe_object("Cardtitle", 0.5, POCOobject=Cardtitle, swipeTye="y")

    def swipe_Neutral(self):
        """移动表情--脸无表情"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Neutral":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        emoticonsPOCO = object
        self.findSwipe_object("Neutral", 0.8, POCOobject=emoticonsPOCO, swipeTye="y",beginPos=[0.3,0.7])

    def swipe_eventRewards(self):
        """移动AD奖励信息一栏"""
        eventrewardsPOCO = self.poco("Viewport").offspring("eventRewards")
        self.findSwipe_object("eventrewardsPOCO",0.5,POCOobject=eventrewardsPOCO,swipeTye="y")

    def swipe_bio(self):
        """移动Bio一栏"""
        editPOCO = self.poco("Bio").child("BioDes")
        self.findSwipe_object("editPOCO",0.5,editPOCO,swipeTye="y")

    def swipe_region(self):
        """移动Region一栏"""
        editPOCO = self.poco("Region").child("RegionDes")
        self.findSwipe_object("editPOCO",0.4,editPOCO,swipeTye="y")

    def showachievement_step(self):
        """展示成就变更的步骤"""
        self.click_profile()
        self.swipe_head()
        print("1111")
        sleep(5)
        self.swipe_Card()
        print("222")
        sleep(5)
        self.click_Achievement_button()
        self.click_showloyalreader()
        print(self.Profile_info)
        self.Profilemodule_info["name"] = self.Profile_info
        self.click_topback()
        return self.Profilemodule_info["name"]

    def changeemoticons_step(self):
        """变换表情步骤"""
        self.click_profile()
        self.click_background()
        self.click_emoticons()
        self.click_laughing()
        self.Profilemodule_info["emoticons"] = self.Profile_info
        sleep(3)
        if self.click_save():
            sleep(3)
            return self.Profilemodule_info["emoticons"]
        else:
            self.click_back()
            return self.Profilemodule_info["emoticons"]

    def editname_step(self,nameString=""):
        """改名步骤"""
        self.click_profile()
        self.click_edit()
        sleep(2)
        self.editNickname(Nickname=nameString)
        sleep(1)
        print(self.Profile_info)
        self.Profilemodule_info["name"] = self.Profile_info
        if self.findClick_Image("Paperplanebutton.png", record_pos=(0.454, 0.312)):
            pass
        else:
            self.android_findClick("com.mars.avgchapters:id/btn_send", "com.mars.avgchapters:id/btn_send",
                                   description="点击提交按钮")

        sleep(3)
        self.click_editback()
        return self.Profilemodule_info["name"]

    def changehead_step(self):
        """更换头像的步骤"""
        self.click_profile()
        self.click_edit()
        sleep(2)
        self.click_head()
        sleep(2)
        self.refuse_member_renew()
        i = 0
        while i < 3:
            self.click_maybel()
            i = i + 1
        self.click_game_avatar()
        self.click_headportrait()
        self.click_headback()

    def changeavatar_step(self):
        """更换角色步骤"""
        self.click_profile()
        self.click_background()
        sleep(5)
        self.refuse_member_renew()
        i = 0
        while i < 3:
            self.click_maybel()
            i = i + 1
        sleep(1)
        self.click_avatar()
        self.click_choose_avatar()
        self.Profilemodule_info["_instanceId"] = self.Profile_info["_instanceId"]
        self.click_back()
        sleep(1)
        self.click_accept_popups()
        sleep(5)
        return self.Profilemodule_info["_instanceId"]

    def ChangeUseravatar(self):
        """更换个人信息背景角色"""
        self.changeavatar_step()
        return True

    def ChangeUseremoticons(self):
        """更换个人信息表情"""
        self.changeemoticons_step()
        return True

    def nameedit(self,name=""):
        """修改名字"""
        self.editname_step(nameString=name)
        return True

    def Change_showAchievement(self):
        """展示的成就选择"""
        self.showachievement_step()
        return True

    def Changeheadportrait(self):
        """更换个人信息的头像"""
        self.changehead_step()
        return True


# tt= Profilemodule()
# tt.nameedit(name="qwe651")