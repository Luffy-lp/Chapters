from common import COM_utilities
from common.COM_data import MyData
from common.COM_findobject import FindObject
from common.COM_utilities import *
# from pages.startgame.page_loginView import LoginView
from scenes.scenes_login.SCN_gameloaded import GameLoaded
from scenes.scenes_login.SCN_newuser import NewUserGuide


# TODO:当用户存在多个账号的情况下

class SignIn(FindObject):
    SignIn_info = {}
    _pos = [0.5, 0.53]

    def __init__(self):
        FindObject.__init__(self)

    def issign(self):
        """判断是否完成登陆"""
        clock()
        GameLoaded1 = GameLoaded()
        NewUserGuide1 = NewUserGuide()
        while not self.find_try("UserBackground", description="用户信息界面"):
            GameLoaded1.gameloading()
            NewUserGuide1.newUserPopUp()
            mytime = float(clock("stop"))
            if mytime > 120:
                log(Exception("检测是否登陆成功失败"))
                self.SignIn_info["用户登陆状态"] = "尝试登陆失败"
                raise Exception("检测是否登陆成功失败")
        self.SignIn_info["用户登陆状态"] = "完成登陆"
        return True

    def loginGuide(self):
        """登陆流程"""
        if MyData.UserData_dir["loginInfo"]["loginGuide"] == "Google":
            self.click_Google()
            self.mysleep(5)
            if self.android_tryfind("com.google.android.gms:id/list", description="Google绑定用户选择", waitTime=3):
                try:
                    listname = self.androidpoco("com.google.android.gms:id/account_name")
                    for i in listname:
                        name = i.get_text()
                        if name == MyData.UserData_dir["loginInfo"]["loginemail"]:
                            print("你登陆的用户:", name)
                            self.findClick_childobject(i, description="登录Google用户")
                            self.SignIn_info["Google用户"] = name
                            return True
                    name = listname[0].get_text()
                    print("未找到你想要登陆的用户，目前登陆用户:", name)
                    self.findClick_childobject(listname[0], description="登录Google用户")
                    self.SignIn_info["Google用户"] = name
                    self.bindLoginComfirm()
                except:
                    pass
            elif self.android_tryfind("identifierId", description="Google新增用户", waitTime=3):
                self.androidpoco("identifierId").set_text(MyData.UserData_dir["loginInfo"]["loginemail"])
                self.android_findClick("identifierNext", "identifierNext", description="点击继续", waitTime=1, sleeptime=2)
                self.androidpoco("android.widget.EditText").set_text(MyData.UserData_dir["loginInfo"]["loginpassword"])
                self.android_findClick("passwordNext", "passwordNext", description="下一步", waitTime=1, sleeptime=2)
                self.android_findClick("signinconsentNext", "signinconsentNext", description="同意", waitTime=1,
                                       sleeptime=1)
                if self.findClick_try("android.widget.Button", "android.widget.Button", description="接受", waitTime=2,
                                      sleeptime=1, pocotype="Androidpoco"):
                    print("添加账号成功")
                else:
                    self.findClick_try("com.google.android.gms:id/sud_navbar_next",
                                       "com.google.android.gms:id/sud_navbar_next", description="Next", waitTime=1,
                                       sleeptime=3, pocotype="Androidpoco")
                    self.click_Google()
                    self.bindLoginComfirm()
            else:
                print("已绑定过用户")
            return True
        if MyData.UserData_dir["loginInfo"]["loginGuide"] == "FaceBook":
            self.click_FaceBook()
            self.mysleep(5)
            if self.android_tryfind("m_login_email", description="faceBook未登录", waitTime=3):
                self.androidpoco("m_login_email").set_text(MyData.UserData_dir["loginInfo"]["loginemail"])
                sleep(2)
                self.androidpoco("m_login_password").set_text(MyData.UserData_dir["loginInfo"]["loginpassword"])
                self.mysleep(2)
                if self.android_tryfind("android.widget.Button", description="登录", waitTime=1):
                    self.android_findClick("android.widget.Button","android.widget.Button",description="登陆按钮",sleeptime=3)
                if self.android_tryfind("登录 ", description="首次登录", waitTime=1):
                    loginPOCO = self.androidpoco("登录 ").wait(3)
                    self.findClick_childobject(loginPOCO, description="点击登录", waitTime=1, sleeptime=5)
                if self.androidpoco(nameMatches="^u_0_1.*").wait(1):
                    loginPOCO1 = self.androidpoco(nameMatches="^u_0_1.*")
                    self.findClick_childobject(loginPOCO1, description="继续", waitTime=1)
            elif self.androidpoco(nameMatches="^帐号.*").wait(1):#未添加Fackbook账号
                 loginPOCO1=self.androidpoco(nameMatches="^帐号.*")
                 loginPOCO1.set_text(MyData.UserData_dir["loginInfo"]["loginemail"])
                 sleep(1)
                 self.androidpoco(nameMatches="^密码.*").set_text(MyData.UserData_dir["loginInfo"]["loginpassword"])
                 sleep(2)
                 loginPOCO2 = self.androidpoco(nameMatches="^登录.*")
                 self.findClick_childobject(loginPOCO2, description="登录",waitTime=1)
            elif self.androidpoco(nameMatches="^u_0_1.*").wait(1):
                 loginPOCO1=self.androidpoco(nameMatches="^u_0_1.*")
                 self.findClick_childobject(loginPOCO1, description="继续",waitTime=1)


    def bindLoginComfirm(self):
        """登陆Comfirm按钮判断"""
        click(PosTurn(self._pos))
        if self.poco("UIBindLoginComfirm").child("Button").wait(3).exists():
            LoginComfirmBtn = self.poco("UIBindLoginComfirm").child("Button")
            self.findClick_childobject(LoginComfirmBtn, description="Comfirm按钮", waitTime=3)

    def process_profilelogin(self):
        """个人信息登陆流程Google,FaceBook"""
        if self.find_try("UserBackground", description="用户信息界面", waitTime=5) == True:
            self.SignIn_info["用户登陆状态"] = "已登陆"
        else:
            self.SignIn_info["用户登陆状态"] = "未登陆"
            self.click_Profile()
            self.click_Signin()
            self.check_agree()
            self.loginGuide()
            self.mysleep(5)
            self.issign()
        return True

    def loginGuide_login_process(self, login="Google", email="15019423971", password="yo5161381"):
        """进入游戏登陆流程"""
        self.loginGuide()
        sleep(10)
        click(PosTurn(self._pos))  # 盲点按钮
        self.bindLoginComfirm()

    def click_Profile(self):
        self.findClick_object("Profile", "Profile", description="Profile", waitTime=5)

    def click_Signin(self):
        """Signin按钮"""
        self.notchfit__Click_try("Sign", "Sign", description="Sign in按钮", waitTime=5)

    def check_agree(self):
        """勾选同意"""
        POCOBtn = self.poco("PolicyBtn").child("Image")
        if not self.show_checkImage1().wait(1).exists():
            self.findClick_childobject(POCOBtn, description="勾选同意按钮")

    def click_Google(self):
        """选择Google方式登陆"""
        self.click_object("GoogleBtn", description="选择Google方式", waitTime=1)

    def click_FaceBook(self):
        """选择FaceBook方式登陆"""
        self.click_object("FaceBookBtn", description="选择FaceBook方式")

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
# SignIn1.loginGuide()
# if SignIn1.android_tryfind("com.google.android.gms:id/list", description="Google绑定用户选择", waitTime=3):
#     print("ddddddddd")
# elif SignIn1.android_tryfind("identifierId", description="Google新增用户", waitTime=3):
#     print("eeeeeeeeeeeee")
# else:print("ccccccccccccccccccc")
