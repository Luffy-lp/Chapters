from common.COM_findobject import CommonPoco


class CardPanel(CommonPoco):
    """书籍详情页"""
    def __init__(self):
        CommonPoco.__init__(self)
        # poco("UIBookNewDetail")
    def click_close(self):
        """会员快捷入口按钮"""
        self.findClick_object("BookDetail_Bubble", "BookDetail_Bubble", description="会员快捷入口")

    def click_Reset(self, type="SetBook"):
        """SetBook,SetChapter"""