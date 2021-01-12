import json
import shutil

from common.COM_path import *
import yaml
from common.COM_utilities import *
from common.COM_path import *
from common.my_log import mylog
from common.COM_API import APiClass


# TODO:书架需要考虑新手手书架情况

class UserData(APiClass):
    _instance = None

    def __init__(self):
        self.UserData_dir = {}  # 0.device_id 1.uuid 2.LoginStatus
        self.Bookshelf__dir = {}  # readprogressList 书籍列表
        self.ConfData_dir = {}
        self.Story_cfg_chapter_dir = {}  # 章节总信息表
        self.Element_dir = {}
        self.readprogressList_dir = {}  # {'chapterProgress': 10108001, 'chatProgress': 10006}
        self.Stroy_data_dir = {}  # 书籍和ID对应关系
        self.popup_dir = {}
        self.getdata()
        self.clear()
        self.DeviceData_dir = {}
        self.DeviceData_dir["poco"] = None
        self.DeviceData_dir["androidpoco"] = None
        mylog.info("完成数据初始化")
        print("导入用户数据成功")

    def getdata(self):
        self.yamldata_conf()
        self.get_story_cfg_chapter()
        self.getbookData()
        self.stroy_data()
        print(self.Bookshelf__dir)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def yamldata_conf(self):  # 读取yaml数据
        data = None
        path = os.path.join(path_YAML_FILES, "conf.yml")
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f.read(), Loader=yaml.Loader)
            uuid = data["UserData"]["uuid"]
            channel_id = data["UserData"]["channel_id"]
            device_platform = data["UserData"]["device_platform"]
            device_id = data["UserData"]["device_id"]
            self.UserData_dir["device_id"] = device_id
            self.UserData_dir["uuid"] = uuid
            loginInfo = {}
            loginInfo["loginGuide"] = data["UserData"]["loginGuide"]
            loginInfo["loginemail"] = data["UserData"]["loginemail"]
            loginInfo["loginpassword"] = data["UserData"]["loginpassword"]
            self.UserData_dir["loginInfo"] = loginInfo
            self.ConfData_dir["packagepath"] = os.path.join(path_resource, data["ConfData"]["APKpackage"])
            print("ConfData_dir:", self.ConfData_dir["packagepath"])
            self.ConfData_dir["packageName"] = data["ConfData"]["packageName"]
            self.ConfData_dir["ADBdevice"] = data["ConfData"]["ADBdevice"]
            self.ConfData_dir["ADBip"] = data["ConfData"]["ADBip"]
            self.ConfData_dir["device"] = data["ConfData"]["device"]
            self.ConfData_dir["method"] = data["ConfData"]["method"]
            self.ConfData_dir["sleepLevel"] = data["ConfData"]["sleepLevel"]
            if self.UserData_dir["uuid"] is None:
                self.UserData_dir["uuid"] = self.registerApi5(channel_id, device_id, device_platform)["uuid"]
            print("用户ID：", self.UserData_dir["uuid"])
            f.close()
            assert_equal(True, True, "接口获取用户ID：{0}".format(self.UserData_dir["uuid"]))

    def getbookData(self):
        """大厅书架信息"""
        # Weekly Update
        bookData = self.summaryApi3(self.UserData_dir["uuid"])
        areadata = bookData["area_data"]
        bannerdata = bookData["banner_data"]
        story_ids = bannerdata["story_ids"]
        self.Bookshelf__dir["banner_data"] = story_ids
        # 获得大厅Weekly Update书籍列表
        for i in areadata:
            for k, v in i.items():
                if v == "Weekly Update":
                    story_ids = i["story_ids"]
                    self.Bookshelf__dir[v] = story_ids

    def getreadprogress(self, bookid):
        """获取用户阅读进度返回chapterProgress和chatProgress"""
        datalist = self.getCommonDataApi(self.UserData_dir["uuid"])  # 调用通用接口0.章节进度，1.对话进度
        readprogress = datalist["data"]["readprogress"][bookid]
        # self.readprogressList_dir = readprogress
        return readprogress

    def getLoginStatus(self):
        """获取用户登陆状态"""
        LoginStatus = self.LoginStatusApi(self.UserData_dir["uuid"], self.UserData_dir["device_id"])
        self.UserData_dir["LoginStatus"] = LoginStatus
        return LoginStatus

    def yaml_case(self):
        bookdetailpaths = os.path.join(path_YAML_FILES, "yamlCase\\bookdetail.yml")
        bookdetailData = read_yaml(bookdetailpaths)
        self.Element_dir["bookdetailData"] = bookdetailData

    def get_story_cfg_chapter(self):
        """获取章节详情"""
        data = None
        path = os.path.join(path_resource, "data_s\story_cfg_chapter.txt")
        with open(path, "r", encoding='utf-8') as f:  # 设置文件对象
            data = f.read()  # 可以是随便对文件的操作
        data = eval(data)
        self.Story_cfg_chapter_dir = data
        return self.Story_cfg_chapter_dir

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

    def clear(self):
        """清空之前的报告和文件"""
        fileNamelist = [path_LOG_DIR, path_REPORT_DIR, path_RES_DIR]
        for fileName in fileNamelist:
            filelist = os.listdir(fileName)
            for f in filelist:
                filepath = os.path.join(fileName, f)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                # elif os.path.isdir(filepath):
                #     shutil.rmtree(filepath, True)
        path = os.path.join(path_LOG_MY, "logging.log")
        with open(path, 'w') as f1:
            f1.seek(0)
            f1.truncate()
            f1.close()
        mylog.info("完成文件清空")


MyData = UserData()
