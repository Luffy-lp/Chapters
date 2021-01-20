from common import COM_utilities
from common.COM_findobject import CommonPoco
from common.COM_utilities import *
# from pages.startgame.page_loginView import LoginView
from scenes.scenes_login.SCN_newuser import NewUserGuide


# TODO:当用户存在多个账号的情况下

class SignIn(CommonPoco):
    SignIn_info = {}
    _pos = [0.5, 0.53]

    def __init__(self):
        CommonPoco.__init__(self)

    def issign(self):
        """判断是否登陆"""
        clock()
        while not self.find_try("UIUserInfoSys", description="检测是否登陆成功"):
            NewUserGuide1 = NewUserGuide()
            NewUserGuide1.newUserPopUp()
            mytime = float(clock("stop"))
            if mytime > 30:
                print("检测是否登陆成功失败")
                log(Exception("检测是否登陆成功失败"))
                raise Exception("检测是否登陆成功失败")
        ProfileBt = self.poco("Profile").child("Label")
        self.findClick_childobject(ProfileBt, description="切换到Profile界面")
        if self.find_try("Sign", description="登陆按钮"):
            self.SignIn_info["用户登陆状态"] = False
            return self.SignIn_info
        else:
            self.SignIn_info["用户登陆状态"] = True
            return self.SignIn_info
        return True

    def loginGuide(self):
        """选择登陆方式,Google,FaceBook"""
        if MyData.UserData_dir["loginInfo"]["loginGuide"] == "Google":
            self.click_Google()
            self.mysleep(3)
            if self.android_tryfind("android.widget.FrameLayout", description="Google绑定", waitTime=3):
                try:
                    listname = self.androidpoco("com.google.android.gms:id/account_name").wait(5)
                    for i in listname:
                        name = i.get_text()
                        if name == MyData.UserData_dir["loginInfo"]["loginemail"]:
                            print(name)
                            self.findClick_childobject(i, description="登录Google用户")
                            self.SignIn_info["Google用户"] = name
                            return True
                    name = listname.get_text()
                    self.findClick_childobject(listname, description="登录Google用户")
                    self.SignIn_info["Google用户"] = name
                except:
                    pass
                if self.android_tryfind("identifierId", description="Google绑定", waitTime=3):
                    self.androidpoco("identifierId").set_text(MyData.UserData_dir["loginInfo"]["loginemail"])
                    self.android_findClick("identifierNext", "identifierNext", description="点击继续", waitTime=1, sleeptime=2)
                    self.androidpoco("android.widget.EditText").set_text(MyData.UserData_dir["loginInfo"]["loginpassword"])
                    self.android_findClick("passwordNext", "passwordNext", description="下一步", waitTime=1, sleeptime=2)
                    self.android_findClick("signinconsentNext", "signinconsentNext", description="同意", waitTime=1,
                                           sleeptime=1)
                    self.android_findClick("com.google.android.gms:id/sud_navbar_next",
                                           "com.google.android.gms:id/sud_navbar_next", description="Next", waitTime=1,
                                           sleeptime=3)
                    self.click_Google()
            self.bindLoginComfirm()
            self.mysleep(2)

            return True
        if MyData.UserData_dir["loginInfo"]["loginGuide"] == "FaceBook":
            self.click_FaceBook()
            self.mysleep(5)
            if self.android_tryfind("m_login_email", description="faceBook未登录", waitTime=3):
                # m_login_emailPOCO=self.androidpoco("m_login_email")
                # self.findClick_childobject(m_login_emailPOCO,description="点击输入邮箱",waitTime=1,sleeptime=2)
                self.androidpoco("m_login_email").set_text(MyData.UserData_dir["loginInfo"]["loginemail"])
                sleep(2)
                self.androidpoco("m_login_password").set_text(MyData.UserData_dir["loginInfo"]["loginpassword"])
                self.mysleep(2)
                if self.android_tryfind("登录 ", description="首次登录", waitTime=1):
                    loginPOCO = self.androidpoco("登录 ").wait(3)
                    self.findClick_childobject(loginPOCO, description="点击登录", waitTime=1, sleeptime=5)

                if self.android_tryfind("u_0_1", description="使用相同信息登录", waitTime=1):
                    loginPOCO1 = self.androidpoco("u_0_1")[0]
                    self.findClick_childobject(loginPOCO1, description="点击继续", waitTime=1, sleeptime=2)

    def bindLoginComfirm(self):
        """登陆Comfirm按钮判断"""
        click(PosTurn(self._pos))
        sleep(3)
        if self.poco("UIBindLoginComfirm").child("Button").wait(1).exists():
            LoginComfirmBtn = self.poco("UIBindLoginComfirm").child("Button")
            self.findClick_childobject(LoginComfirmBtn, description="Comfirm按钮")

    def process_profilelogin(self):
        """个人信息登陆流程Google,FaceBook"""
        self.issign()
        print(self.SignIn_info["用户登陆状态"])
        if self.SignIn_info["用户登陆状态"] == False:
            self.click_Signin()
            if not self.show_checkImage1().wait(1).exists():
                self.check_agree()
            self.loginGuide()
            self.mysleep(5)
        return True

    def loginGuide_login_process(self, login="Google", email="15019423971", password="yo5161381"):
        """进入游戏登陆流程"""
        self.loginGuide()
        sleep(10)
        click(PosTurn(self._pos))  # 盲点按钮
        self.bindLoginComfirm()

    def click_Signin(self):
        """Signin按钮"""
        self.click_object("Sign", description="登陆按钮")

    def check_agree(self):
        """勾选同意"""
        POCOBtn = self.poco("PolicyBtn").child("Image")
        self.findClick_childobject(POCOBtn, description="勾选同意按钮")

    def click_Google(self):
        """选择Google方式登陆"""
        self.click_object("GoogleBtn", description="选择Google方式", waitTime=1)

    def click_FaceBook(self):
        """选择FaceBook方式登陆"""
        self.click_object("FaceBookBtn", description="选择FaceBook方式")

    def click_Back(self):
        """返回按钮"""
        Backbtn = self.poco("GuideViewBackBtn").child("Image")
        self.findClick_childobject(Backbtn, description="返回按钮")

    def show_checkImage1(self):
        """勾选图片√"""
        checkImage1 = self.poco("PolicyBtn").child("Image1")
        return checkImage1

# width = G.DEVICE.display_info['width']
# SignIn1 = SignIn()
# SignIn1.process_profilelogin()
