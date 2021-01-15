from common.COM_findobject import CommonPoco
from common.COM_utilities import *

class Shop(CommonPoco):
    Shop_info = {}

    def __init__(self):
        CommonPoco.__init__(self)
    #顶部进入商店
    def click_credit_enter(self):
        """点击枫叶币进入商店"""
        shopPOCO = self.poco("Upper").child("CreditBtn")
        self.findClick_childobject(shopPOCO, description="枫叶币数量", waitTime=1)

    def click_ticket_enter(self):
        """点击票进入商店"""
        shopPOCO = self.poco("Upper").child("TicketBtn")
        self.findClick_childobject(shopPOCO, description="票的数量", waitTime=1)

    def click_diamond_enter(self):
        """点击钻石进入商店"""
        shopPOCO = self.poco("Upper").child("DiamondBtn")
        self.findClick_childobject(shopPOCO, description="钻石的数量", waitTime=1)

    def click_top_back(self):
        """点击顶部返回"""
        topbackPOCO = self.poco("Top").child("BtnReturn")
        self.findClick_childobject(topbackPOCO, description="返回按钮", waitTime=1)

    def click_topclosebtn(self):
        """商城进入的Chapter Pass顶部返回按钮"""
        topPOCO = self.poco("UISubscribe_New").offspring("CloseBtn")
        self.findClick_childobject(topPOCO, description="商城的Chapter Pass返回按钮", waitTime=1)

    def click_topbackbtn(self):
        """点击Chapter Pass顶部返回"""
        # topbackPOCO = self.poco("UIMainMember").offspring("BackBtn")
        self.findClick_try("UIMainMember","BackBtn",description="个人信息进入的Chapter Pass的返回按钮",waitTime=1)
        # self.findClick_childobject(topbackPOCO, description="个人信息进入的Chapter Pass的返回按钮", waitTime=1)

    def click_shop_banner(self):
        """点击商城Banner，跳转订阅"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Scroll View")
        self.findClick_childobject(shopPOCO, description="商城的Banner", waitTime=1)

    #快捷支付弹窗
    #钻石不足，购买视觉小说卡片触发
    def xx(self):
        """点击快捷购买"""
        buyPOCO = self.poco("Item").child("Purchase")
        self.findClick_childobject(buyPOCO, description="购买", waitTime=1)

    #购买商品流程
    def click_buy_ticket(self,nString="30-1001"):
        """点击购买票"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring(nString)[0]
        self.findClick_childobject(shopPOCO, description="购买票卷按钮", waitTime=1)

    def click_buy_diamond(self,nString="29-1004"):
        """点击购买钻石"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring(nString)[0]
        self.findClick_childobject(shopPOCO, description="购买钻石按钮", waitTime=1)

    def click_buy_diamondcard(self):
        """点击购钻石月卡"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring("32-1013")
        self.findClick_childobject(shopPOCO, description="购买月卡", waitTime=1)

    def click_buy_member(self):
        """点击购会员"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring("32-3001")
        self.findClick_childobject(shopPOCO, description="购买会员", waitTime=1)

    def click_subs(self):
        """订阅会员"""
        subsPOCO = self.poco(nameMatches=".*SubBtn")
        self.findClick_childobject(subsPOCO, description="订阅按钮", waitTime=1)
    def click_buy_packges1(self,nString="31-2002"):
        """点击购礼包"""
        shopPOCO = self.poco("LuaUIShopFrame").offspring("Content1").offspring(nString)
        pos=shopPOCO.get_position()
        pos=PosTurn(pos)
        touch(pos)
        # self.findClick_childobject(shopPOCO,description="购买礼包",waitTime=1)

    def click_pay(self):
        """点击确认支付"""
        androidpoco=self.androidpoco("android.widget.LinearLayout").child("android.widget.FrameLayout").offspring("android:id/content").child("com.android.vending:id/0_resource_name_obfuscated").child("com.android.vending:id/0_resource_name_obfuscated").child("com.android.vending:id/0_resource_name_obfuscated")[0].child("com.android.vending:id/0_resource_name_obfuscated")[3].child("com.android.vending:id/0_resource_name_obfuscated").child("com.android.vending:id/0_resource_name_obfuscated").child("com.android.vending:id/0_resource_name_obfuscated").child("com.android.vending:id/0_resource_name_obfuscated").wait(5)
        self.findClick_childobject(androidpoco,description="一律购买/订阅",waitTime=3,sleeptime=1)
        # pos = [0.5, 0.96]
        # print("pos",pos)
        # pos = PosTurn(pos)
        # touch(pos)

    def click_claim_shop(self):
        """点击确认商品"""
        shopPOCO = self.poco("UIClaimReward").offspring("Txt").wait(5)
        self.findClick_childobject(shopPOCO, description="确认按钮", waitTime=1)

    def xxxx(self):
        """"""
        xxPOCO = self.poco("PerRoleItems(Clone)")[0].child("PerRoleItem")[0]
        print(xxPOCO.attr("_instanceId"))


# tt=Shop()
# tt.click_claim_shop()