from common.COM_data import MyData
from scenes.scenes_SidePanel.SCN_SidePanel import SidePanel

class LanguagePanel(SidePanel):
    def __init__(self):
        self.LanguagePanel_info = {}
        SidePanel.__init__(self)
    def chooseLanguage(self,language="English"):
        """SidePanel,English,Spanish,German,French,Korean,Portuguese,Russian,Italian,Japanese"""
        name=self.checkLanguageChoose(language)
        if name==language:
            print("不需要切换:",language)
            self.LanguagePanel_info["switch"]=False
            return True
        self.findClick_object(language,language,description="选择切换到"+language)
        self.findClick_object("LeftBtn","LeftBtn",description="切换语言")
        self.LanguagePanel_info["切换语言"] = language
        self.LanguagePanel_info["switch"] = True
        # MyData.DeviceData_dir["poco"] = None
        return True
    def checkLanguageChoose(self,language):
        """检查当前的语言"""
        name = self.poco("icon", texture="dagou-icon").parent().get_name()
        self.LanguagePanel_info["当前语言"] = name
        print("当前语言:", name)
        return name


