from airtest.core.api import assert_equal
from scenes.scenes_shop.SCN_shop import Shopmodule

def test_shop_buy_member():
    """订阅会员"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_member()
    assert_equal(actualValue, True, "用户的会员状态信息{0}".format(myShopmodule.Shopmodule_info))


def test_shop_buy_ticket(num):
    """购买票卷"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_ticket(num)
    assert_equal(actualValue, True, "购买非双倍奖励的5票{0}".format(myShopmodule.Shopmodule_info))


def test_shop_buy_diamond(num):
    """购买钻石"""
    myShopmodule = Shopmodule()
    actualValue = myShopmodule.shop_buy_diamond(num)
    assert_equal(actualValue, True, "购买非双倍奖励的20钻石{0}".format(myShopmodule.Shopmodule_info))
