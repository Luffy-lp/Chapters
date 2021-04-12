from date.Chapters_data import MyData
from scenes.SCN_pageTurn import PageTurn
from scenes.scenes_SidePanel.SCN_SidePanel import SidePanel
class Help(SidePanel):
    def __init__(self):
        self.LanguagePanel_info = {}
        SidePanel.__init__(self)
    def click_About(self):
        self.click_object("regard",description="About",sleeptime=1)
    def get_userID(self):
        PageTurn1=PageTurn()
        PageTurn1.Upper_click("chapter")
        self.click_help()
        self.click_About()
        uuid=self.poco("userid").get_TMPtext()
        MyData.UserData_dir["uuid"] = uuid
        print("获取到的用户ID:",MyData.UserData_dir["uuid"])
        self.click_back()
        self.click_back()
        PageTurn1.click_pos("8","5")
# Help1=Help()
# Help1.get_userID()


