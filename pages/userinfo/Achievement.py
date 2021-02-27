from common.COM_findobject import FindObject


class Achievement(FindObject):
    name={}

    def __init__(self):
        FindObject.__init__(self)

    def click_achievement(self):
        """点击跳到个人信息的achievement"""
        AchievementPOCO=self.poco("ToptGroup").child("Achievement").child("Label")
        self.findClick_childobject(AchievementPOCO, description="achievement按钮并点击", waitTime=1)

    #成就Baby Steps
    def click_babysteps(self):
        """点击成就Baby Steps"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Baby Steps":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().click()

    #成就Half Hour Hero
    def click_half(self):
        """点击成就Half Hour Hero"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Half Hour Hero":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().click()

    # 成就Investor
    def click_investor(self):
        """点击成就Investor"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Investor":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()

    #成就Technocrat
    def click_technocrat(self):
        print("点击成就Technocrat")
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Technocrat":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().click()

        # 成就Loyal Reader
    def click_loyalreader(self):
        """点击成就Loyal Reader"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Loyal Reader":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        self.name = object.get_TMPtext()
        print("ccc:", object.parent().get_name())
        object.parent().click()
        return self.name

    #成就Influencer
    def click_influencer(self):
        """点击成就Influencer"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Influencer":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().click()

    # 成就Chatty Cathy
    def click_chattycathy(self):
        """点击成就Chatty Cathy"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Chatty Cathy":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()



    #成就Weekly Warrior
    def click_weeklywarrior(self):
        """点击成就Weekly Warrior"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Weekly Warrior":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().child(nameMatches="TitleImgL.*").click()
    # 成就Early Bird
    def click_earlybird(self):
        """点击成就Early Bird"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Early Bird":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()

        # 成就Nightingale
    def click_nightingale(self):
        """点击成就Nightingale"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Nightingale":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()

    # 成就Marathoner
    def click_marathoner(self):
        """点击成就Marathoner"""
        object = None
        list = self.poco("LeftItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Marathoner":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()

        # 成就Story Master
    def click_storymaster(self):
        """点击成就Story Master"""
        object = None
        list = self.poco("RightItem").child("Title")
        for i in list:
            if i.get_TMPtext() == "Story Master":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        print(object.get_name())
        print("ccc:", object.parent().get_name())
        object.parent().click()

    def click_Getreward(self):
        """点击GetRaward按钮"""
        if self.find_try("Button",description="可解锁/获取奖励"):
            AchievementPOCO = self.poco("Center").child("ScrollView").offspring("Text (TMP)")
            AchievementPOCO.click([0.5,0.25])
            # self.findClick_childobject(AchievementPOCO, description="按钮",waitTime=1)

    def click_discoverback(self):
        """点击返回上一级"""
        discoverbackPOCO = self.poco("DiscoverBack").child("IgRed")
        self.findClick_childobject(discoverbackPOCO, description="返回按钮并点击", waitTime=1)
