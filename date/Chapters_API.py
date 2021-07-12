import json
import time
from time import sleep
import traceback
import requests
import sys, os, zipfile
# from keras.utils.data_utils import get_file
# from common.COM_utilities import *
from common.COM_path import *


class APiClass():
    _response = None
    Header = {"TIMECLOSE": "1"}
    url = "http://testitf.stardustgod.com/"

    def __init__(self):
        print("调用接口类")

    def try_APIlink(self, url, headers, body, name, trytime=100, timeout=10):
        """requests公共方法"""
        while (trytime >= 0):
            trytime = trytime - 1
            try:
                print("拉取{0}接口".format(name))  # 补充正则截取
                self._response = requests.post(url=url, headers=headers, data=body, timeout=10)

            except:
                # traceback.print_exc()
                print("拉取{0}接口失败，重试".format(name))
                sleep(1)
            else:
                dir = eval(self._response.text)
                # print(self._response.text)
                # my_re=\n[\s\S]*
                print("拉取{0}接口成功".format(name))
                return dir

    def registerApi5(self, bind_type="device", channel_id="AVG10005", device_id="490000000326402",
                     device_platform="android"):
        """游戏用户登录注册接口v3"""
        url = self.url + 'registerApi5.Class.php?DEBUG=true'
        body = {"device_platform": device_platform,
                "channel_id": channel_id,
                "app_version": "605.0.0",
                "base_code_version": "605.0.0",
                "device_id": device_id,
                "code_version": "605.0.0",
                "bind_id": device_id,
                "bind_type": bind_type,
                "account_id": "tourists",
                "account_type": "tourists"
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="registerApi5")
        return data

    def LoginStatusApi(self, UUID, deviceId):
        """获取登录状态接口"""
        url = self.url + "LoginStatusApi.Class.php?DEBUG=true"
        body = {"action": "getStatus",
                "uuid": UUID,
                "deviceId": deviceId,
                }
        response = requests.post(url=url, headers=self.Header, data=body, timeout=10)
        dir = eval(response.text)
        return dir["data"]["status"]

    def summaryApi3(self, UUID, language="en-US"):
        """获取书架信息接口"""
        url = self.url + "summaryApi3.Class.php?DEBUG=true"
        Header = {"TIMECLOSE": "1",
                  "language": language}
        body = {"channel_id": "AVG10005",
                "uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=Header, body=body, trytime=10, name="summaryApi3")
        return data

    def story_v1_hall(self, UUID, language="en-US"):
        """获取书架信息接口ja-JP  en-US"""
        UUID=43090
        url = "http://dev-chapters-int.stardustgod.com" + "/na/story/v1/hall?debug=true"
        # url = self.url + "/na/story/v1/hall?debug=true"
        print(url)
        Header = {"platform":"android",
                  "Accept":"application/json",
                  "language": language}
        body = {"channel_id": "AVG50005",
                "uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=Header, body=body, trytime=10, name="story_v1_hall")
        data=1
        return data

    def getStoryAllChapterInfoApi(self, UUID, story_id):
        """获取书籍章节信息,query_type=2（作废）"""
        print("拉取获取书籍章节信息接口")
        url = self.url + "getStoryAllChapterInfoApi.Class.php?DEBUG=true"
        body = {"story_id": story_id,
                "uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=self.Header, data=body, timeout=10, name="getStoryAllChapterInfoApi")
        print(data)

    def getCommonDataApi(self, UUID):
        """拉取存档通用数据接口"""
        time = 1603505085
        url = self.url + "Controllers/archive/GetCommonDataApi.php?DEBUG=true"
        body = {"uuid": UUID,
                "need_common_data": 1,
                "day_pass_updated_at": time,
                "buy_chapter_updated_at": time,
                "my_book_updated_at": time,
                "read_progress_updated_at": time,
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, trytime=10, timeout=1, name="getCommonDataApi")
        return data
    def readApi(self, UUID,storyId):
        """记录短信阅读进度"""
        url = self.url + "readApi.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                "storyId": storyId,
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, trytime=10, timeout=1, name="readApi")
        return data

    def getAllStoryInfoApi(self, UUID):
        """所有章节信息接口"""
        url = self.url + "getAllStoryInfoApi.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=self.Header, data=body, timeout=10, name="getAllStoryInfoApi")
        story_info = data["data"]["list"][0]
        return story_info

    def heartbeatsApi3(self, UUID, device_id="490000000326402", channel_id="AVG10005"):
        """心跳接口"""
        url = self.url + "heartbeatsApi3.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                "channel_id": channel_id,
                "device_id": device_id,
                "big_version": "991"
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="heartbeatsApi3")
        return data

    def getAllStoryInfoApi(self, UUID):
        """获取所有书籍信息"""
        url = self.url + "getAllStoryInfoApi.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="getAllStoryInfoApi")
        return data

    def syncValueApi(self, UUID, value_type, channel_id="AVG10005", valuechange=0):
        """虚拟币类型，值有：diamond，ticket"""
        url = self.url + "syncValueApi.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                "channel_id": channel_id,
                "random_id": str(time.time()),
                "tag": "charge",
                "value_type": value_type,
                "value_all": "",
                "value_change": valuechange
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="syncValueApi")
        print(data)
        return data

    def todayCheckNewPushApi(self, UUID):
        """检查有无新推送"""
        url = self.url + "TodayCheckNewPushApi.Class.php?DEBUG=true"
        body = {"uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="todayCheckNewPushApi")
        print(data)
        return data

    def memberInfoApi(self, UUID):
        """diamond，ticket"""
        url = self.url + "Controllers/member/GetMemberInfoApi.php?DEBUG=true"
        body = {"uuid": UUID,
                }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="memberInfoApi")
        return data

    def unzip_file(self, fz_name, path):
        """
        解压缩文件
        :param fz_name: zip文件
        :param path: 解压缩路径
        :return:
        """
        flag = False

        if zipfile.is_zipfile(fz_name):  # 检查是否为zip文件
            with zipfile.ZipFile(fz_name, 'r') as zipf:
                zipf.extractall(path)
                # for p in zipf.namelist():
                #     # 使用cp437对文件名进行解码还原， win下一般使用的是gbk编码
                #     p = p.encode('cp437').decode('gbk')  # 解决中文乱码
                #     print(fz_name, p,path)
                flag = True

        return {'file_name': fz_name, 'flag': flag}
        source_dir = os.getcwd() + "\\10009001"
        dest_dir = os.getcwd()
        print(source_dir)

    def downloardurl(self, address):
        # zp = None
        # source_dir = os.getcwd()
        path = "/resource"
        try:
            r = requests.get(address, stream=True)
            print("下载成功")
        except:
            print("下载失败")
        zip_file = zipfile.ZipFile('gamecfg_0805test_20201217_Q5yEz1.zip')
        zip_list = zip_file.namelist()
        folder_abs = path
        for f in zip_list:
            zip_file.extract(f, folder_abs)
        zip_file.close()

    def avgcontentApi(self, bookid):
        """获取章节资源下载地址"""
        url = self.url + "avgcontentApi.Class.php?DEBUG=true"
        body = {"chapter_id": bookid,
                "source_type": "t0"
                }
        response = self.try_APIlink(url=url, headers=self.Header, body=body, name="avgcontentApi")
        address: str = response["address"]
        addresslist = address.split('/')
        print(address)
        address = address.replace("\\", "")
        print(address)
        print(type(address))
        time = 5
        while (time > 1):
            time = time - 1
            try:
                r = requests.get(address)
                path = os.path.join(path_resource, addresslist[len(addresslist) - 1])
                print("path", path)
                pathbook = os.path.join(path_resource, bookid)
                print("pathbook", pathbook)
                with open(path, "wb") as code:
                    code.write(r.content)
                    print("打开书籍资源")
                sleep(5)
                code.close()
                file_zip = zipfile.ZipFile(path, 'r')
                sleep(2)
                file_zip.extractall(pathbook)
                file_zip.close()
                os.remove(path)
                return
            except BaseException as e:
                sleep(2)
                print("书籍资源读取失败,重试", e)
            else:
                print("书籍资源读取成功")
        # raise Exception("下载书籍资源失败")

# APiClass1=APiClass()
# data=APiClass1.getCommonDataApi("46776")
# print("data111111",data)
