from common.COM_findobject import CommonPoco
# TODO:当用户存在多个账号的情况下

class LoginView(CommonPoco):
    """登陆welcome界面"""

    def __init__(self):
        CommonPoco.__init__(self)
    def click_Signin(self):
        """Signin按钮"""
        self.click_object("Sign",description="登陆按钮")

    def check_agree(self):
        """勾选同意"""
        POCOBtn=self.poco("PolicyBtn").child("Image")
        self.findClick_childobject(POCOBtn, description="勾选同意按钮")
    def click_Google(self):
        """选择Google方式登陆"""
        self.click_object("GoogleBtn",description="选择Google方式")
    def click_Back(self):
        """返回按钮"""
        Backbtn= self.poco("GuideViewBackBtn").child("Image")
        self.findClick_childobject(Backbtn, description="返回按钮")
    def show_checkImage1(self):
        """勾选图片√"""
        checkImage1=self.poco("PolicyBtn").child("Image1")
        return  checkImage1