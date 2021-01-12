from common.COM_findobject import CommonPoco

class PagBookDetail(CommonPoco):
    """书籍详情页"""
    def __init__(self):
        CommonPoco.__init__(self)
        self.PagBookDetail_dir={}
        self.get_pagBookDetail_data()

    def click_card(self):
        """卡片按钮"""
        self.findClick_object("BottomBg", "Card", description="卡片按钮")

    def click_like(self):
        """收藏按钮"""
        self.findClick_object("BottomBg", "Like", description="收藏按钮")

    def click_comment(self):
        """评论按钮"""
        self.findClick_object("BottomBg", "Comment", description="评论按钮")

    def click_Reset(self):
        """重置按钮按钮"""
        self.findClick_object("BottomBg", "Reset", description="重置按钮")

    def click_Play(self):
        """Play按钮"""
        self.findclick("click_Play","Play按钮",sleeptime=2)

    def click_close(self):
        """关闭页面按钮"""
        self.findclick("click_close","关闭页面按钮",sleeptime=1)

    def click_daypass(self):
        """Daypass入口按钮"""
        self.findClick_object("Daypass", "Daypass", description="Daypass入口按钮", sleeptime=2)

    def click_close(self):
        """会员快捷入口按钮"""
        self.findClick_object("BookDetail_Bubble", "BookDetail_Bubble", description="会员快捷入口")

    def click_card(self):
        self.findClick_object("BottomBg", "Reset", description="Close按钮")

    def click_card(self):
        self.findClick_object("BottomBg", "Card", description="Close按钮")

    def click_card(self):
        self.findClick_object("BottomBg", "Card", description="Close按钮")

    def click_close(self):
        if self.findClick_object("Mask", "Button", description="关闭详情页按钮"):
            return True
    def get_pagBookDetail_data(self):
        pageglist = self.Element_dir["bookdetailData"]["bookdetail"]["page_bookdetail"]
        print(pageglist)
        for dir in pageglist:
            for k,v in dir.items():
                self.PagBookDetail_dir[k]=v
    def findclick(self,name,description,waitTime=0.2,sleeptime=0):
        findobject=self.PagBookDetail_dir[name]["findobject"]
        clickobject=self.PagBookDetail_dir[name]["clickobject"]
        self.findClick_object(findobject, clickobject, description=description,waitTime=waitTime, sleeptime=sleeptime)