from airtest.core.api import assert_equal
from scenes.scenes_SidePanel.SCN_help import Help
def test_getuserID():
    """获取用户信息"""
    Help1=Help()
    Help1.get_userID()