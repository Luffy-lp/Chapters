import time
from airtest.core.api import *
from common.COM_findobject import CommonPoco
from pages.shop.shop import *
from common.COM_API import *
from common.COM_data import *
from common.my_log import mylog
from common.COM_utilities import *
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class Shopmodule(Shop):
    Shopmodule_info ={}
    #滑动商品
    def swipe_diamonds(self):
        """滑动钻石商品"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring("29-1004")[0]
        self.findSwipe_object(shopPOCO,0.2,POCOobject=shopPOCO,swipeTye="y")

    def swipe_member(self):
        """滑动会员"""
        shopPOCO = self.poco("SpecialVip")
        self.findSwipe_object(shopPOCO,0.6,POCOobject=shopPOCO,swipeTye="y")

    def swipe_diamondcard(self):
        """滑动Diamond Card"""
        # shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring("31-2001")
        # self.findSwipe_object(shopPOCO,stopPos=0.9,POCOobject=shopPOCO,swipeTye="y")
        self.findSwipe_object("SpecialMonth",0.6,POCOobject=self.poco("SpecialMonth"),swipeTye="y")

    def buy_ticket_step(self):
        """购买票的步骤"""
        MyData.getUsercurrency()
        increment = MyData.UserData_dir["ticket"]
        self.click_ticket_enter()
        self.click_buy_ticket()
        time.sleep(10)
        if self.android_tryfind("android.widget.RadioButton",description="购买身份验证",waitTime=2):
            androidpoco=self.androidpoco("android.widget.RadioButton")[0]
            self.findClick_childobject(androidpoco,description="一律启用",waitTime=1,sleeptime=1)
        self.click_pay()
        time.sleep(20)
        self.click_claim_shop()
        self.click_top_back()
        # 购买完后展示用户信息
        MyData.getUsercurrency()
        # mylog.info("用户信息【{}】".format(MyData.UserData_dir))
        print("票",MyData.UserData_dir["ticket"])
        MyData.UserData_dir["increment"] = MyData.UserData_dir["ticket"] - increment
        self.Shopmodule_info["ticket"] = MyData.UserData_dir["ticket"]
        self.Shopmodule_info["increment"] = MyData.UserData_dir["increment"]
        return self.Shopmodule_info

    def buy_diamond_step(self):
        """购买钻石步骤"""
        MyData.getUsercurrency()
        increment = MyData.UserData_dir["diamond"]
        self.click_ticket_enter()
        self.click_buy_diamond()
        time.sleep(10)
        self.click_pay()
        time.sleep(20)
        self.click_claim_shop()
        self.click_top_back()
        # 购买完后展示用户信息
        MyData.getUsercurrency()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))
        print("钻石",MyData.UserData_dir["diamond"])
        MyData.UserData_dir["increment"] = MyData.UserData_dir["diamond"] - increment
        self.Shopmodule_info["diamond"] = MyData.UserData_dir["diamond"]
        self.Shopmodule_info["increment"] = MyData.UserData_dir["increment"]
        return self.Shopmodule_info

    def buy_member_step(self):
        """购买会员步骤"""
        self.click_ticket_enter()
        MyData.getUsermemberinfo()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))
        MyData.UserData_dir["member_type_old"] = MyData.UserData_dir["member_type"]
        self.swipe_diamonds()
        self.click_buy_member()
        if self.find_try("TopTip"):
            self.click_subs()#点击订阅会员按钮
            time.sleep(2)
            boolis = True
            clock()
            while boolis:
                self.click_pay()
                time.sleep(3)
                try:
                    self.poco("CloseBtn").click()
                    boolis=False
                    print("订阅后点击返回按钮")
                    mylog.info("订阅后点击返回按钮")
                except:
                    pass
                mytime = float(clock("stop"))
                if mytime>30:
                    mylog.error("未发现订阅返回按钮")
                    log(Exception("未发现订阅返回按钮"))
            try:
                self.click_top_back()
            except:
                pass
            try:
                self.click_top_back()
            except:
                pass            # 购买完后的用户数据
            MyData.getUsermemberinfo()
            mylog.info("用户会员状态：【{}】".format(MyData.UserData_dir))
            self.Shopmodule_info["member_type"] = MyData.UserData_dir["member_type"]
            self.Shopmodule_info["member_type_old"] = MyData.UserData_dir["member_type_old"]
            return self.Shopmodule_info
        else:
            self.click_topbackbtn()
            self.click_top_back()
            MyData.getUsermemberinfo()
            mylog.info("用户会员状态：【{}】".format(MyData.UserData_dir))
            self.Shopmodule_info["member_type"] = MyData.UserData_dir["member_type"]
            self.Shopmodule_info["member_type_old"] = MyData.UserData_dir["member_type_old"]
            return self.Shopmodule_info

    def shop_buy_member(self):
        """点击订阅会员"""
        self.buy_member_step()
        return True

    def shop_buy_diamondcard(self):
        """购买钻卡"""
        MyData.getUsercurrency()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))
        self.click_buy_diamondcard()
        time.sleep(10)
        self.click_pay()
        time.sleep(20)
        self.click_claim_shop()
        #购买完后的用户数据
        MyData.getUsercurrency()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))

    def shop_buy_packages1(self):
        """购买4.99礼包"""
        MyData.getUsercurrency()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))
        self.click_buy_packges1()
        time.sleep(10)
        self.click_pay()
        time.sleep(20)
        self.click_claim_shop()
        #购买完后的用户数据
        MyData.getUsercurrency()
        mylog.info("用户信息【{}】".format(MyData.UserData_dir))

    def shop_buy_diamond(self):
        """点击购买20钻石"""
        self.buy_diamond_step()
        return True

    def shop_buy_ticket(self):
        """点击购买5票"""
        self.buy_ticket_step()
        return True

# tt=Shopmodule()
# poco1 = AndroidUiautomationPoco()
# tt.buy_ticket_step()
