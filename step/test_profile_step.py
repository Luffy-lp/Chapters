from airtest.core.api import assert_equal, wake
from scenes.scenes_profile.SCN_profilemodule import Profilemodule
from scenes.scenes_profile.SCN_achievementmodule import Achievementmodule

def test_ChangeUseravatar():
    """更换个人信息背景角色"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.ChangeUseravatar()
    assert_equal(actualValue, True, "更换背景角色情况{0}".format(myProfilemodule.Profilemodule_info))

def test_operationAchievement():
    """对成就进行操作"""
    myAchievementmodule = Achievementmodule()
    actualValue = myAchievementmodule.operationAchievememt()
    assert_equal(True, True, "进行操作的成就名字{0}".format(myAchievementmodule.Achievementmodule_info["name"]))


def test_ChangeUseremoticons(expression):
    """更换背景角色表情"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.ChangeUseremoticons(expression)
    assert_equal(actualValue, True, "更换角色的表情{0}".format((myProfilemodule.Profilemodule_info["emoticons"])))


def test_nameedit(name):
    """编辑名字"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.nameedit(name=name)
    assert_equal(actualValue, True, "编辑名字{0}".format((myProfilemodule.Profilemodule_info["name"])))


def test_showAchievement():
    """成就展示"""
    myProfilemodule = Profilemodule()
    actualValue = myProfilemodule.Change_showAchievement()
    assert_equal(actualValue, True, "成就展示变更的名字{0}".format(myProfilemodule.Profilemodule_info["name"]))