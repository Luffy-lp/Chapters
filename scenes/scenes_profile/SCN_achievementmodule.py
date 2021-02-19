import time
from airtest.core.api import *
from pages.userinfo.Achievement import Achievement
from common.COM_findobject import FindObject

class Achievementmodule(Achievement):
    Achievementmodule_info = {}

    def swipe_investor(self):
        """移动成就Investor"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Investor":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_technocrat(self):
        """移动成就Technocrat"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Technocrat":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_loyalreader(self):
        """移动成就Loyal Reader"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Loyal Reader":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_influencer(self):
        """移动成就Influencer"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Influencer":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_chattycathy(self):
        """移动成就Chatty Cathy"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Chatty Cathy":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_weeklywarrior(self):
        """移动成就Weekly Warrior"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Weekly Warrior":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_earlybird(self):
        """移动成就Earliy Bird"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Early Bird":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_nightingale(self):
        """移动成就Nightgale"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Nightingale":
                print(i.get_TMPtext())
                object = i.parent()
                break
            else:
                print("failed")
        print(object.get_name())
        self.findSwipe_object("object", 0.5, POCOobject=object, swipeTye="y")

    def swipe_Achievement_level2(self):
        """移动成就等级图标，等级2"""
        Am_level = self.poco("Center").child("ScrollView").child("Content").offspring("1").child("Image")
        self.findSwipe_object("Am_level", 0.5, POCOobject=Am_level, swipeTye="x")

    def swipe_Achievement_level3(self):
        """移动成就等级图标，等级3"""
        Achievement_level = self.poco("Center").child("ScrollView").child("Content").offspring("2").child("Image")
        self.findSwipe_object("Achievement_level", 0.5, POCOobject=Achievement_level, swipeTye="x")

    def swipe_Achievement_level4(self):
        """移动成就等级图标等级4"""
        Achievement_level = self.poco("Content").offspring("3").child("Image")
        self.findSwipe_object("Achievement_level", 0.5, POCOobject=Achievement_level,swipeTye="x")

    def swipe_Achievement_level5(self):
        """移动成就等级图标等级5"""
        Achievement_level = self.poco("Center").child("ScrollView").child("Content").offspring("4").child("Image")
        self.findSwipe_object("Achievement_level", 0.5, POCOobject=Achievement_level, swipeTye="x")

    def operatiomAchievement_step(self):
        """演示操作成就步骤"""
        self.click_achievement()
        self.swipe_weeklywarrior()
        sleep(2)
        self.click_weeklywarrior()
        self.Achievementmodule_info["name"] = self.name
        sleep(2)
        discoverbackPOCO = self.poco("Center").child("ScrollView").offspring("Button")
        if self.find_try("Button"):
            # self.findSwipe_object("discoverbackPOCO", 0.89, POCOobject=discoverbackPOCO, swipeTye="y")
            self.click_Getreward()
        sleep(3)
        self.click_discoverback()
        sleep(5)
        return self.Achievementmodule_info["name"]

    def operationAchievememt(self):
        """对成就进行一定的操作"""
        self.operatiomAchievement_step()
        return True
