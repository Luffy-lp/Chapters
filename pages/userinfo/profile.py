from airtest.core.api import touch
from airtest.core.cv import Template
from airtest.core.api import *
from common.COM_findobject import *
import random
import sys
from common.COM_utilities import *


class Profile(FindObject):
    Profile_info={}

    def __init__(self):
        FindObject.__init__(self)

    def click_profile_page(self):
        """跳转到个人信息页面"""
        #底部栏的操作
        perPOCO = self.poco("Bottom").child("4").wait(5)
        self.findClick_childobject(perPOCO, description="Profile按钮", waitTime=1)

    def click_profile(self):
        """点击个人信息的Profile"""
        perPOCO = self.poco("ToptGroup").child("Profile").wait(3)
        self.findClick_childobject(perPOCO, description="个人信息按钮", waitTime=1)

    def click_achievement(self):
        """点击个人信息的achievement"""
        AchievementPOCO=self.poco("ToptGroup").child("Achievement").child("Label").wait(3)
        self.findClick_childobject(AchievementPOCO, description="achievement按钮", waitTime=1)

    def click_Following(self):
        """点击Following按钮"""
        self.findClick_object("InfoBtnView","Following",description="Following按钮",waitTime=1)

    def click_Followers(self):
        """点击Followers按钮"""
        self.findClick_object("InfoBtnView","Follows",description="Followers按钮",waitTime=1)

    def viewfan(self):
        """点击查看关注对象"""
        fansPOCO = self.poco("Item(Clone)").child("IgHead")
        self.findClick_childobject(fansPOCO, description="粉丝", waitTime=1)

    def click_follow(self):
        """点击关注xx"""
        fansPOCO = self.poco("Btn").child("Follow")
        self.findClick_childobject(fansPOCO, description="关注粉丝", waitTime=1)

    def click_cancelfl(self):
        """取消关注"""
        fansPOCO = self.poco("Btn").child("Friends")
        self.findClick_childobject(fansPOCO, description="取消关注", waitTime=1)

    #关注相关的确认弹窗
    def click_sure(self):
        """点击确认"""
        fansPOCO = self.poco("AlterView").child("LeftBtn")
        self.findClick_childobject(fansPOCO, description="确认按钮", waitTime=1)

    def click_refuse(self):
        """点击拒绝"""
        fansPOCO = self.poco("AlterView").child("RightBtn")
        self.findClick_childobject(fansPOCO, description="拒绝按钮", waitTime=1)

    def click_Stories(self):
        """点击Stories按钮"""
        self.findClick_object("InfoBtnView","Read Books",description="Stories按钮",waitTime=1)

    def click_chapters(self):
        """点击Chapters"""
        fansPOCO = self.poco("Toggle").child("Chapter")
        self.findClick_childobject(fansPOCO, description="Chapters", waitTime=1)

    def click_taptales(self):
        """点击Tatales"""
        fansPOCO = self.poco("Toggle").child("Taptales")
        self.findClick_childobject(fansPOCO, description="Taptales按钮", waitTime=1)

    #个人信息的故事板


    #视觉小说的展示卡片
    def click_Card_button(self):
        """点击Card按钮"""
        AchievementPOCO = self.poco("Card").child("Button")
        self.findClick_childobject(AchievementPOCO, description="Card按钮", waitTime=1)

    def click_Card1(self):
        """点击展示Card1"""
        CardPOCO = self.poco("Card").child("Card1")
        self.findClick_childobject(CardPOCO, description="Card1", waitTime=1)

    def click_Card2(self):
        """点击展示Card2"""
        CardPOCO = self.poco("Card").child("Card2")
        self.findClick_childobject(CardPOCO, description="Card2", waitTime=1)

    def click_Card3(self):
        """点击展示Card3"""
        CardPOCO = self.poco("Card").child("Card3")
        self.findClick_childobject(CardPOCO, description="Card3", waitTime=1)

    def click_showcard1(self):
        """test"""
        cardPOCO = self.poco("Content").child("ShowCardItem(Clone)")[1].child("0")
        self.findClick_childobject(cardPOCO, description="试试", waitTime=1)

    #展示成就
    def click_Achievement_button(self):
        """点击Achievement的标题"""
        AMPOCO = self.poco("Achievement").child("Button")
        self.findClick_childobject(AMPOCO, description="Achievement按钮", waitTime=1)

    def click_Achiement1(self):
        """点击展示Achiement1"""
        AMPOCO = self.poco("Achievement").child("Achiement1")
        self.findClick_childobject(AMPOCO, description="Achiement1", waitTime=1)

    def click_Achiement2(self):
        """点击展示Achiement2"""
        AMPOCO = self.poco("Achievement").child("Achiement2")
        self.findClick_childobject(AMPOCO, description="Achiement2", waitTime=1)

    def click_Achiement3(self):
        """点击展示Achiement3"""
        AMPOCO = self.poco("Achievement").child("Achiement3")
        self.findClick_childobject(AMPOCO, description="Achiement3", waitTime=1)

    def click_showinfluencer(self):
        """点击展示Influencer成就，根据名字去点击成就"""
        object = None
        list = self.poco("Content").offspring("Text")
        for i in list:
            if i.get_TMPtext() == "Influencer":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        print("ccc:",object.parent().get_name())
        object.parent().click()

    def click_showloyalreader(self):
        """点击展示Loyal Reader成就，根据名字去点击成就"""
        object = None
        list = self.poco("Content").offspring("Text")
        for i in list:
            if i.get_TMPtext() == "Loyal Reader":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        print(object.get_name())
        self.Profile_info = object.get_TMPtext()
        print("ccc:",object.parent().get_name())
        object.parent().click()
        return self.Profile_info

    #返回关闭部分
    def click_guideback(self):
        """登录点击返回"""
        guidevbackPOCO = self.poco("Panel").child("GuideViewBackBtn")
        self.findClick_childobject(guidevbackPOCO, description="返回按钮", waitTime=1)

    def click_topback(self):
        """展示里点击顶部返回"""
        topbackPOCO = self.poco("Top").child("Back")
        self.findClick_childobject(topbackPOCO, description="返回按钮", waitTime=1)

    def click_topbackbtn(self):
        """点击顶部返回"""
        topbackPOCO = self.poco("Top").child("BackBtn")
        self.findClick_childobject(topbackPOCO, description="返回按钮", waitTime=1)

    def click_sign_in(self):
        """点击登录按钮"""
        self.click_object("TextMeshPro Text",description="点击Sign in按钮",waitTime=1)

    def click_acclause(self):
        """勾选同意条款"""
        perPOCO = self.poco("PolicyBtn").child("Image")
        self.findClick_childobject(perPOCO, description="勾选条款框", waitTime=1)

    def click_choosegg(self):
        """选择谷歌账号登录"""
        perPOCO = self.poco("GuideLoginBtnView").child("GoogleBtn")
        self.findClick_childobject(perPOCO, description="谷歌登录按钮", waitTime=1)

    def click_choosefb(self):
        """选择Fackbook账号登录"""
        perPOCO = self.poco("GuideLoginBtnView").child("FaceBookBtn")
        self.findClick_childobject(perPOCO, description="Fackbook登录按钮", waitTime=1)


    #登录后
    def click_background(self):
        """点击user背景"""
        bgroundPOCO = self.poco("View").child("UserBackground")
        self.findClick_childobject(bgroundPOCO, description="user background", waitTime=1,clickPos=[0.5,0.25])

    def refuse_member_renew(self):
        """检测是否提醒会员资格过期并取消续费"""
        if self.find_try("RenewBtn",description="检测是否有弹框提醒会员到期"):
            self.click_object("CancelBtn",description="取消会员续费")

    def accpet_member_renew(self):
        """检测是否提醒会员过期并接受续费"""
        if self.find_try("RenweBtn",description="检测是否有弹框提醒会员到期"):
            self.click_object("RenewBtn",description="对会员进行续费")

    #进入背景编辑
    def click_arrowsdown(self):
        """点击展示全身"""
        bgroundPOCO = self.poco("GameObject").child("ArrowsDown").child("ArrowsDown")
        self.findClick_childobject(bgroundPOCO, description="全身展示", waitTime=1)

    def click_closeadown(self):
        """关闭全身展示"""
        bgroundPOCO = self.poco("UIDressUpPanel").child("Show")
        self.findClick_childobject(bgroundPOCO, description="关闭全身展示", waitTime=1)
    def click_avatar(self):
        """选择Avatar页面"""
        bgroundPOCO = self.poco("Banner").child("Role").child("Label")
        self.findClick_childobject(bgroundPOCO, description="Avatar页面", waitTime=1)

    def click_choose_avatar(self):
        """初始进入默认展示，没有移动"""
        x = 0
        y = random.randint(0,2)
        print("选择背景角色",x,y)
        bgroundPOCO = self.poco("PerRoleItems(Clone)")[x].child("PerRoleItem")[y]
        self.findClick_childobject(bgroundPOCO, description="随机角色形象", waitTime=1)
        self.Profile_info["_instanceId"] = bgroundPOCO.attr("_instanceId")
        return self.Profile_info["_instanceId"]
        #采用图片来匹配方法
        #path="D:\ChaptersApp_Auto\IMG\\tpl1608198184519.png"
        #touch(Template((path), resolution=(1080, 1920)))

    def click_emoticons(self):
        """选择Emoticons页面"""
        bgroundPOCO = self.poco("Banner").child("Emoticons").child("Label")
        self.findClick_childobject(bgroundPOCO, description="Emoticons页面", waitTime=1)

    def click_expression(self,sTing=""):
        """进行点击选择表情"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == sTing:
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def swipe_expression_down(self,sTing=""):
        """对表情进行滑动（预留一下）"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == sTing:
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        self.findSwipe_object("xxx",0.89,object.parent(),swipeTye="y",beginPos=[0.5,0.85])
        return self.Profile_info

    def swipe_expression_up(self,sTing=""):
        """对表情进行滑动（预留一下）"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == sTing:
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        self.findSwipe_object("xxx",0.77,object.parent(),swipeTye="y",beginPos=[0.5,0.85])
        return self.Profile_info

    def click_angry(self):
        """选择表情--生气"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Angry":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_cry(self):
        """选择表情--哭泣"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Cry":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_laughing(self):
        """选择表情--开口笑"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Laughing":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_neutral(self):
        """选择面无表情"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Neutral":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_sad(self):
        """选择表情--伤心"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Sad":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_shock(self):
        """选择表情--震惊"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Shock":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_shy(self):
        """选择表情--害羞"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Shy":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_smile(self):
        """选择表情--微笑"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Smile":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_flirty(self):
        """选择表情--挑逗"""
        object = None
        list = self.poco("EmoticonsItem").child("Name")
        for i in list:
            if i.get_TMPtext() == "Flirty":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        self.Profile_info = object.get_TMPtext()
        object.parent().click()
        return self.Profile_info

    def click_avatar_round(self):
        """选择Background页面"""
        bgroundPOCO = self.poco("Banner").child("Background").child("Label")
        self.findClick_childobject(bgroundPOCO, description="Background页面", waitTime=1)

    def click_backdrop(self):
        """选择背景"""
        x = random.randint(0,1)
        y = random.randint(0,2)
        print(x,y)
        avatarPOCO = self.poco("PerBgItems(Clone)")[x].child("PerBgItem")[y]
        self.findClick_childobject(avatarPOCO, description="Background", waitTime=1)

    def click_save(self):
        """点击保存"""
        if self.find_try("Done",description="检测右上角是否有Save按钮点击进行保存"):
            self.findClick_object("Upper","Done",description="Save按钮",waitTime=1)
            return True

    def click_changn(self):
        """检测是否有提醒弹窗并进行选择-现在改变"""
        if self.find_try("LaterBtn",description="检测是否有弹框提醒解锁新物品"):
            self.click_object("UseBtn")

    def click_maybel(self):
        """检测是否有提醒弹窗并进行-稍后变换"""
        if self.find_try("LaterBtn",description="检测是否有弹框提醒解锁新物品"):
            self.click_object("LaterBtn")

    def click_back(self):
        """背景部分编辑的点击返回"""
        if self.find_try("Back",description="背景部分的返回按钮"):
            self.click_object("Back",waitTime=3,description="返回按钮")

    def click_accept_popups(self):
        """检测是否有弹窗提醒选择保存否--接受保存"""
        if self.find_try("LeftBtn",description="检测是否有弹框提醒保存"):
            self.click_object("LeftBtn",waitTime=3,description="接受保存")

    def click_refuse_popups(self):
        """检测是否有弹窗提醒选择保存否--拒绝保存"""
        if self.find_try("RightBtn2",description="检测是否有弹框提醒保存"):
            self.click_object("RightBtn2",waitTime=3,description="拒绝保存")

    def click_qipao(self):
        """点击气泡"""
        qipaoPOCO = self.poco("Qipao").child("BubbleHead")
        self.findClick_childobject(qipaoPOCO, description="气泡按钮", waitTime=3)

    #气泡界面
    def click_qpback(self):
        """在气泡界面点击返回"""
        qipaoPOCO = self.poco("BubbleView").child("Back")
        self.findClick_childobject(qipaoPOCO, description="返回按钮", waitTime=3)

    #进入订阅界面
    def click_homepage(self):
        """点击homepage按钮"""
        AchievementPOCO=self.poco("Free").child("Button")
        self.findClick_childobject(AchievementPOCO, description="homepage按钮", waitTime=3)
    #订阅界面
    def click_topq(self):
        """点击rules"""
        topbackPOCO = self.poco("Top").child("QBackBtn")
        self.findClick_childobject(topbackPOCO, description="Rules", waitTime=3)

    def click_mlcoin(self):
        """点击枫叶币"""
        coinbtnPOCO = self.poco("Viewport").offspring("Image")
        self.findClick_childobject(coinbtnPOCO, description="枫叶币", waitTime=3)

    def click_entersubs(self):
        """点击订阅"""
        subscribePOCO = self.poco("Viewport").offspring("SubscribeBtn")
        self.findClick_childobject(subscribePOCO, description="订阅按钮", waitTime=3)

    def click_subscribe(self):
        """点击订阅"""
        subsPOCO = self.poco("Main").child("SubBtn")
        self.findClick_childobject(subsPOCO, description="订阅按钮", waitTime=3)

    def click_firstsubs(self):
        """第一次订阅"""
        subsPOCO = self.poco("UISubscribe_New").offspring("FirstSubBtn")
        self.findClick_childobject(subsPOCO, description="订阅按钮", waitTime=3)

    def click_rulesclose(self):
        """Rules关闭"""
        closePOCO = self.poco("UIMemberExplain").child("CloseBtn")
        self.findClick_childobject(closePOCO, description="关闭按钮", waitTime=3)

    #进入编辑界面
    def click_edit(self):
        """点击Edit按钮"""
        editPOCO = self.poco("UserInfoVeiw").child("Edit").wait(3)
        self.findClick_childobject(editPOCO, description="Edit按钮", waitTime=3)
    #进入头像编辑界面
    def click_head(self):
        """编辑头像"""
        editPOCO = self.poco("Content").child("Head")
        self.findClick_childobject(editPOCO, description="head编辑按钮", waitTime=3)

    def click_resetbt(self):
        """点击重置按钮"""
        editPOCO = self.poco("UISetUserHead").child("Tip")
        self.findClick_childobject(editPOCO, description="重置按钮", waitTime=3)

    def click_game_avatar(self):
        """点击Game Avatar按钮"""
        editPOCO = self.poco("Toggle").child("Avatar")
        self.findClick_childobject(editPOCO, description="Game Avatar按钮", waitTime=3)

    def click_avatar_frame(self):
        """点击Avatar Frame按钮"""
        editPOCO = self.poco("Toggle").child("Frame")
        self.findClick_childobject(editPOCO, description="Avatar Frame按钮", waitTime=3)

    def click_headportrait(self):
        """点击头像1"""
        editPOCO = self.poco("AvatarView").offspring("dd474eb3d139375b83cd2b6da2acf189")
        self.findClick_childobject(editPOCO, description="头像1", waitTime=3)

    def click_headframe(self):
        """点击头像框1"""
        editPOCO = self.poco("FrameView").offspring("fab459563687245526e4b40490d53d70")
        self.findClick_childobject(editPOCO, description="头像框1", waitTime=3)

    def click_headback(self):
        """点击返回"""
        editPOCO = self.poco("UISetUserHead").offspring("Back")
        self.findClick_childobject(editPOCO, description="返回按钮", waitTime=3)

    def click_name(self):
        """编辑name"""
        editPOCO = self.poco("Content").child("Name")
        self.findClick_childobject(editPOCO, description="name编辑按钮", waitTime=3)

    def editNickname(self, Nickname):
        """编辑name文本"""
        self.click_object("NameInput", description="Name文本输入框")
        for i in range(10):
            keyevent("67")
        text(Nickname)
        self.Profile_info = Nickname
        return self.Profile_info

    def click_region(self):
        """编辑region信息"""
        editPOCO = self.poco("Content").child("Region")
        self.findClick_childobject(editPOCO, description="Region按钮", waitTime=3)

    def click_select_region(self):
        """选择Region"""
        object = None
        list = self.poco("Text")
        for i in list:
            print(i.get_TMPtext())
            if i.get_TMPtext() == "Aruba":
                print(i.get_TMPtext())
                object = i
                break
            else:print("failed")
        object.parent().click()

    def click_school(self):
        """编辑School信息"""
        editPOCO = self.poco("Content").child("School")
        self.findClick_childobject(editPOCO, description="编辑School按钮", waitTime=3)

    def editSchooltext(self, School):
        """编辑School文本"""
        self.click_object("SchoolInput", description="School文本输入框",sleeptime=1)
        for i in range(10):
            keyevent("67")
        text(School)

    def click_bio(self):
        """编辑Bio的信息"""
        editPOCO = self.poco("Content").child("Bio")
        self.findClick_childobject(editPOCO, description="编辑Bio按钮", waitTime=3)

    def editBiotext(self, Bio):
        """编辑Bio文本"""
        self.click_object("BioInput", description="Bio文本输入框",sleeptime=1)
        for i in range(10):
            keyevent("67")
        text(Bio)

    def click_confirm(self):
        """点击确认修改"""
        pos = [0.9, 0.55]
        print("pos",pos)
        pos = PosTurn(pos)
        touch(pos)

    def click_pricacy(self):
        """编辑Pricacy的相关设置"""
        editPOCO = self.poco("Content").child("Pricacy")
        self.findClick_childobject(editPOCO, description="编辑Pricacy设置按钮", waitTime=3)

    def click_pricacy_set1(self):
        """privacy的设置项一"""
        object = None
        list = self.poco("UIPrivacySettings").child("Region").child("Des")
        for i in list:
            if i.get_TMPtext() == "Who can see my region":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        object.parent().click()

    def click_pricacy_set2(self):
        """privacy的设置项二"""
        object = None
        list = self.poco("UIPrivacySettings").child("Follow").child("Des")
        for i in list:
            if i.get_TMPtext() == "Who can see my follows":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        object.parent().click()

    def click_pricacy_set3(self):
        """privacy的设置项三"""
        object = None
        list = self.poco("UIPrivacySettings").child("Comments").child("Des")
        for i in list:
            if i.get_TMPtext() == "Who can see my school":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        object.parent().click()

    def click_pricacy_set4(self):
        """privacy的设置项四"""
        object = None
        list = self.poco("UIPrivacySettings").child("ReadingHistory").child("Des")
        for i in list:
            if i.get_TMPtext() == "Who can see my stories":
                print(i.get_TMPtext())
                object = i
                break
            else:
                print("failed")
        object.parent().click()

    #弹窗选项：
    def click_everyone(self):
        """选择Everyone可以看见"""
        privacyPOCO = self.poco("Options").child("Button(Clone)")[0].child("Text")
        self.findClick_childobject(privacyPOCO, description="选项所有人可见", waitTime=3)

    def click_friends(self):
        """选择Friends可以看见"""
        privacyPOCO = self.poco("Options").child("Button(Clone)")[1].child("Text")
        self.findClick_childobject(privacyPOCO, description="选项朋友可见", waitTime=3)

    def click_off(self):
        """选择Off"""
        privacyPOCO = self.poco("Options").child("Button(Clone)")[2].child("Text")
        self.findClick_childobject(privacyPOCO, description="选项关闭", waitTime=3)

    def click_cancel(self):
        """选择取消"""
        privacyPOCO = self.poco("Buttons").child("Cancel")
        self.findClick_childobject(privacyPOCO, description="取消选项", waitTime=3)

    def click_logout(self):
        """点击退出登录"""
        editPOCO = self.poco("Content").child("LogOut")
        self.findClick_childobject(editPOCO, description="Logout按钮", waitTime=3)

    def click_editback(self):
        """编辑界面的back按钮"""
        editPOCO = self.poco("UIProfileEdit").offspring("Back")
        self.findClick_childobject(editPOCO, description="编辑面Back按钮", waitTime=3)

