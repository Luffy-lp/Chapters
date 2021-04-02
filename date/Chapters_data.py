import yaml
from common.COM_path import *
from common.my_log import mylog
from date.Chapters_API import APiClass


# TODO:书架需要考虑新手手书架情况
class UserData(APiClass):
    _instance = None
    storyoptions_dir = {}
    bookread_result = {}

    def __init__(self):
        self.DeviceData_dir = {}  # 设备信息配置表
        self.DeviceData_dir["poco"] = None
        self.DeviceData_dir["androidpoco"] = None
        self.EnvData_dir = {}  # 环境配置表
        self.UserData_dir = {}  # 用户基本数据表
        self.UserData_dir["bookDetailInfo"] = {}
        self.UserData_dir["bookDetailInfo"]["BookID"] = None
        self.UserData_dir["当前语言"] = None
        self.UserPath_dir = {}  # 用户自定义路径
        self.Bookshelf__dir = {}  # readprogressList 书籍列表
        self.Story_cfg_chapter_dir = {}  # 章节总信息表
        self.Stroy_data_dir = {}  # 书籍和ID对应关系
        self.readprogressList_dir = {}  # {'chapterProgress': 10108001, 'chatProgress': 10006} 书籍进度表
        self.chat_type_dir = {}  # 对话类型配置表
        self.popup_dir = {}  # 弹框配置表
        self.chat_type_dir = {}  # 对话类型配置表
        self.Element_dir = {}
        self.language_dir = {}
        self.newPoP_dir=[]
        self.book_list=[]
        self.bookresult_dir={}
        self.getdata()
        self.downloadbook_sign = {}
        mylog.info("完成数据初始化")
        print("导入用户数据成功")

    def getdata(self):
        self.yamldata_conf()
        # self.stroy_data()
        self.yaml_stroy()
        self.yaml_chattype()
        self.yaml_mobileconf()
        self.yaml_language()
        self.getbookData()
        self.yaml_bookinfo()
        self.yaml_newpopup()
        self.yaml_bookread_result()
        print(self.Bookshelf__dir)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def read_yaml(self, filepath):
        with open(filepath, encoding='utf-8') as file:
            value = yaml.safe_load(file)
        return value

    def yaml_case(self):
        bookdetailpaths = os.path.join(path_YAML_FILES, "yamlCase\\bookdetail.yml")
        bookdetailData = self.read_yaml(bookdetailpaths)
        self.Element_dir["bookdetailData"] = bookdetailData

    def yaml_stroy(self):
        storyoptionspath = os.path.join(path_YAML_FILES, "yamlGame/storyoptions.yml")
        self.storyoptions_dir = self.read_yaml(storyoptionspath)

    def yaml_chattype(self):
        chattype = os.path.join(path_YAML_FILES, "yamlGame/chat_type.yml")
        self.chat_type_dir = self.read_yaml(chattype)
        return self.chat_type_dir

    def yaml_mobileconf(self):
        mobileconfpath = os.path.join(path_YAML_FILES, "mobileconf.yml")
        self.mobileconf_dir = self.read_yaml(mobileconfpath)
        print(self.mobileconf_dir)
        return self.mobileconf_dir

    def yaml_language(self):
        yamllanguagepath = os.path.join(path_YAML_FILES, "yamllanguage/language_basics.yml")
        self.language_dir = self.read_yaml(yamllanguagepath)
        return self.language_dir

    def yaml_bookinfo(self):
        yamlbook_listpath = os.path.join(path_YAML_FILES, "bookread_result.yml")
        self.book_list = self.read_yaml(yamlbook_listpath)
        return self.book_list

    def yaml_newpopup(self):
        yamlnewpopup_path = os.path.join(path_YAML_FILES, "yamlGame/newpopup.yml")
        with open(yamlnewpopup_path, encoding='utf-8') as file:
            self.newPoP_dir = yaml.safe_load(file)
        return self.newPoP_dir

    def yaml_bookread_result(self):
        file_path=os.path.join(path_YAML_FILES, "bookread_result.yml")
        with open(file_path, encoding='utf-8') as file:
            self.bookresult_dir = yaml.safe_load(file)
        return self.bookresult_dir

    def set_yaml(self,chapter,result):
        file_path=os.path.join(path_YAML_FILES, "bookread_result.yml")
        # mybool=self.bookresult_dir.__contains__(chapter)
        # self.bookresult_dir= dict(self.bookresult_dir)
        if type(self.bookresult_dir)!=dict:
            self.bookresult_dir={}
        self.bookresult_dir[chapter]=result
        with open(file_path, 'w+', encoding="utf-8") as f:
            # allow_unicode不加此参数，写入中文会出现乱码
            yaml.dump(self.bookresult_dir, f, allow_unicode=True)
        print("self.bookresult_dir", self.bookresult_dir)
        return self.bookresult_dir

    def yamldata_conf(self):
        # 读取yamlconf数据
        data = None
        loginInfo = {}
        path = os.path.join(path_YAML_FILES, "conf.yml")
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f.read(), Loader=yaml.Loader)
        uuid = data["UserData"]["uuid"]
        channel_id = data["UserData"]["channel_id"]
        device_platform = data["UserData"]["device_platform"]
        device_id = data["UserData"]["device_id"]
        self.UserData_dir["device_id"] = device_id
        self.UserData_dir["uuid"] = uuid
        loginInfo["loginGuide"] = data["UserData"]["loginGuide"]
        loginInfo["loginemail"] = data["UserData"]["loginemail"]
        loginInfo["loginpassword"] = data["UserData"]["loginpassword"]
        self.UserData_dir["loginInfo"] = loginInfo
        self.EnvData_dir["packagepath"] = os.path.join(path_resource, data["EnvData"]["APKpackage"])
        print("EnvData_dir:", self.EnvData_dir["packagepath"])
        self.EnvData_dir["packageName"] = data["EnvData"]["packageName"]
        self.EnvData_dir["ADBdevice"] = data["EnvData"]["ADBdevice"]
        self.EnvData_dir["ADBip"] = data["EnvData"]["ADBip"]
        self.EnvData_dir["device"] = data["EnvData"]["device"]
        self.EnvData_dir["method"] = data["EnvData"]["method"]
        self.EnvData_dir["simulator"] = data["EnvData"]["simulator"]
        self.EnvData_dir["sleepLevel"] = data["EnvData"]["sleepLevel"]
        self.UserPath_dir["errorLogpath"] = data["PathData"]["errorLogpath"]
        self.UserPath_dir["adbpath"] = data["PathData"]["adbpath"]
        if not self.UserData_dir["uuid"]:
            uuid=self.registerApi5(channel_id, device_id, device_platform)["user"]["uuid"]
            self.UserData_dir["uuid"] = uuid
        print("用户ID：", self.UserData_dir["uuid"])

    def getbookData(self, language="en-US"):
        """大厅书架信息"""
        # self.UserData_dir["当前语言"]="Spanish"
        # language = self.UserData_dir["当前语言"]
        for i in self.language_dir:
            if i == language:
                language = self.language_dir[i]["formatName"]
        bookData = self.summaryApi3(self.UserData_dir["uuid"], language)  # es-ES,en-US
        areaData = bookData["area_data"]
        discover_data = bookData["discover_data"]
        bannerData = bookData["banner_data"]
        story_ids = bannerData["story_ids"]
        self.Bookshelf__dir["banner_data"] = story_ids
        # 获得大厅Weekly Update书籍列表
        for i in areaData:
            for k, v in i.items():
                if v == "Weekly Update":
                    story_ids = i["story_ids"]
                    self.Bookshelf__dir[v] = story_ids
        for i in areaData:
            for k, v in i.items():
                if v == "Weekly Update":
                    story_ids = i["story_ids"]
                    self.Bookshelf__dir[v] = story_ids
        # 获得大厅banner_data书籍列表

    def getreadprogress(self, bookid):
        """获取用户阅读进度返回chapterProgress和chatProgress"""
        datalist = self.getCommonDataApi(self.UserData_dir["uuid"])  # 调用通用接口0.章节进度，1.对话进度
        try:
            readprogress = datalist["data"]["readprogress"]
        except:
            raise Exception("请检查存档是否使用新存档，目前仅支持新存档")
        # chapter_id = datalist["data"]["readprogress"][bookid]["chatProgress"]
        # self.readprogressList_dir = readprogress
        return readprogress


    def download_bookresource(self, bookid):
        """拉取书籍资源"""
        if bookid not in self.downloadbook_sign:
            self.avgcontentApi(bookid)
            self.downloadbook_sign[bookid] = True
            print("下载书籍资源成功")
        else:
            print("书籍资源已经下载")

    def read_story_cfg_chapter(self, bookid, chapter_id):
        """读取当前章节信息txt"""
        bookpath = bookid + "\\data_s\\" + chapter_id + "_chat.txt"
        path = os.path.join(path_resource, bookpath)
        print("path", path)
        with open(path, "r", encoding='utf-8') as f:  # 设置文件对象
            data = f.read()  # 可以是随便对文件的操作
        data = eval(data)
        self.Story_cfg_chapter_dir = data
        self.Story_cfg_chapter_dir["length"] = len(data)
        return self.Story_cfg_chapter_dir

    def getLoginStatus(self):
        """获取用户登陆状态"""
        LoginStatus = self.LoginStatusApi(self.UserData_dir["uuid"], self.UserData_dir["device_id"])
        self.UserData_dir["LoginStatus"] = LoginStatus
        return LoginStatus

    def stroy_data(self):
        """存在书籍和ID对应关系"""
        path = os.path.join(path_resource, "story_data.json")
        data = None
        with open(path, "r", encoding='utf-8') as f:  # 设置文件对象
            data = f.read()
        data = eval(data)["data"]
        for i in data:
            for j in i:
                self.Stroy_data_dir[i["story_id"]] = i["title"]
        return self.Stroy_data_dir

    def getAllStoryInfo(self, story_id):
        """获取书籍信息"""
        data = self.getAllStoryInfoApi(self.UserData_dir["uuid"])
        list = data["data"]["list"]
        for i in list:
            if i["story_id"] == story_id:
                print(i["title"])

    def getUsercurrency(self):
        """	虚拟币类型currency"""
        diamond = self.syncValueApi(self.UserData_dir["uuid"], value_type="diamond")["value"]
        ticket = self.syncValueApi(self.UserData_dir["uuid"], value_type="ticket")["value"]
        credit = self.memberInfoApi(self.UserData_dir["uuid"])["data"]["credit"]
        self.UserData_dir["diamond"] = diamond
        self.UserData_dir["ticket"] = ticket
        self.UserData_dir["credit"] = credit
        return self.UserData_dir

    def getUsermemberinfo(self):
        """获取会员相关信息"""
        member_type = self.memberInfoApi(self.UserData_dir["uuid"])["data"]["member_type"]
        self.UserData_dir["member_type"] = member_type

    def getstoryoptions(self, stroyID, stroychapter):
        for k in self.storyoptions_dir.keys():
            if stroyID == k:
                try:
                    stroyoptionlist = self.storyoptions_dir[k][stroychapter]
                    print("stroyoptionlist", stroyoptionlist)
                    return stroyoptionlist
                except:
                    print("无特殊选项")
                    return None
            else:
                return None


MyData = UserData()