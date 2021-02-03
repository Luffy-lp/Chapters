# -*- encoding=utf8 -*-
from time import sleep
from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException, PocoException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from common.COM_utilities import clock
from common.my_log import mylog
from common.COM_devices import CommonDevices
from common.COM_path import *
from common.COM_data import MyData
from poco.drivers.unity3d import UnityPoco
class FindObject(CommonDevices):
    poco: UnityPoco = None
    androidpoco:AndroidUiautomationPoco = None
    globals()
    Popuplist = []
    AlterTxt = {
        "Please Update Latest Chapter": "CenterBtn",
        "Attention": "LeftBtn",
        "TRIGGER WARNING": "CenterBtn",
        "Info": "CenterBtn"
    }

    def __init__(self):
        CommonDevices.__init__(self)
        if MyData.DeviceData_dir["poco"] == None:
            MyData.DeviceData_dir["poco"] = UnityPoco()
            mylog.info("完成Unity元素定位方法初始化【{}】".format(MyData.DeviceData_dir["poco"]))
            print("完成Unity元素定位方法初始化【{}】".format(MyData.DeviceData_dir["poco"]))
        self.poco = MyData.DeviceData_dir["poco"]
        self.androidpoco = MyData.DeviceData_dir["androidpoco"]
    def find_object(self, findName, description="", waitTime=1, tryTime=1, sleeptime=0):
        """寻找目标"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        print("正在寻找{0}".format(description))
        if self.poco(findName).wait(waitTime).exists():
            print("发现{0}".format(description))
            sleep(sleeptime)
            mylog.info("等待元素-【{}】--加载成功".format(description))
            return True
        log(PocoNoSuchNodeException("等待-【{}】-元素超时".format(description)), desc="等待元素超时")
        raise PocoNoSuchNodeException("等待-【{}】-元素超时".format(description))

    def findClick_object(self, findName, ClickName, description="", waitTime=1, tryTime=1, sleeptime=0):
        """用寻找目标，后并点击"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        print("正在寻找{0}".format(description))
        if self.poco(ClickName).wait(waitTime).exists():
            print("发现{0}元素，并点击".format(description))
            mylog.info("查找点击-【{}】--元素成功".format(description))
            self.poco(ClickName).click()
            mylog.info("点击元素-【{}】--成功".format(description))
            print("点击元素-【{}】--成功".format(description))
            sleep(sleeptime)
            return True
        else:
            print("查找{0}失败".format(description))
            mylog.error("查找点击元素-【{}】--失败".format(findName))
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def find_childobject(self, findPoco:poco, description="", waitTime=1, tryTime=3, sleeptime=0):
        """用于关联父级才能找到的元素"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        if findPoco.wait(waitTime).exists():
            print("发现{0}".format(description))
            mylog.info("查找点击元素-【{}】--成功".format(description))
            return True
        else:
            mylog.error("查找-【{}】-元素失败".format(description))
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def findClick_childobject(self, ClickPoco:poco, description="", waitTime=1, tryTime=1, sleeptime=0.1):
        """用于关联父级才能点击到的元素"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        if ClickPoco.wait(waitTime).exists():
            print("发现{0}".format(description))
            mylog.info("查找点击元素-【{}】--成功".format(description))
            ClickPoco.click()
            sleep(sleeptime)
            mylog.info("点击元素-【{}】--成功".format(description))
            return True
        else:
            mylog.error("查找-【{}】-元素失败".format(description))
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def click_object(self, clickName, waitTime=1, description="", sleeptime=0):
        """直接点击，不存在会报错"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        try:
            self.poco(clickName).wait(waitTime).click()
            mylog.info("点击元素-【{}】--成功".format(description))
            print("点击元素-【{}】--成功".format(description))
            sleep(sleeptime)
            return True
        except Exception as e:
            mylog.error("点击【{0}】出现未知错误，{1}".format(description, e))
            return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def findchildobject_try(self, findPoco:poco, description="", waitTime=0.2, tryTime=1, sleeptime=0):
        """尝试寻找，不一定存在"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                gameobject = findPoco
                print("尝试寻找{0}".format(description))
                mylog.info("尝试寻找-【{}】--".format(description))
                if gameobject.wait(waitTime).exists():
                    print("发现{0}".format(description))
                    sleep(sleeptime)
                    mylog.info("尝试寻找-【{}】-元素成功".format(description))
                    return True
            except:
                return False

    def find_try(self, findName, description="", waitTime=0.2, tryTime=1, sleeptime=0):
        """尝试寻找，不一定存在"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("尝试寻找{0}".format(description))
                mylog.info("尝试寻找-【{}】--".format(description))
                if self.poco(findName).wait(waitTime).exists():
                    print("发现{0}".format(description))
                    sleep(sleeptime)
                    self.Popuplist.append(description)
                    mylog.info("尝试寻找-【{}】-元素成功".format(description))
                    return True
            except:
                return False

    def android_tryfind(self, findName, description="", waitTime=0.2, tryTime=1, sleeptime=0):
        """尝试寻找原生，不一定存在"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("尝试寻找{0}".format(description))
                mylog.info("尝试寻找-【{}】--".format(description))
                if self.androidpoco(findName).wait(waitTime).exists():
                    print("发现{0}".format(description))
                    sleep(sleeptime)
                    self.Popuplist.append(description)
                    mylog.info("尝试寻找-【{}】-元素成功".format(description))
                    return True
            except:
                return False

    def android_findClick(self, findName, ClickName, description="", waitTime=1, tryTime=1, sleeptime=0):
        """用寻找目标，后并点击"""
        waitTime=waitTime+float(MyData.ConfData_dir["sleepLevel"])
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("正在寻找{0}".format(description))
                gameobject = self.androidpoco(findName)
                if gameobject.wait(waitTime).exists():
                    mylog.info("查找元素-【{}】--成功".format(findName))
                    if self.androidpoco(ClickName).exists():
                        print("发现{0}点击元素，并点击".format(description))
                        mylog.info("查找点击-【{}】--元素成功".format(description))
                        self.androidpoco(ClickName).click()
                        mylog.info("点击元素-【{}】--成功".format(description))
                        sleep(sleeptime)
                        return True
                    else:
                        print("查找{0}失败".format(description))
                        mylog.error("查找点击元素-【{}】--失败".format(findName))
                else:
                    mylog.error("查找元素-【{}】--失败".format(findName))
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def findClick_try(self, findName, ClickName, description="", waitTime=0.5, tryTime=1, sleeptime=0, log=True,pocotype=None):
        """尝试寻找并点击，不一定存在"""
        if pocotype=="Androidpoco":
            poco=self.androidpoco
        else:poco=self.poco
        try:
            print("尝试寻找{0}".format(description))
            # gameobject = self.poco(findName)
            if poco(findName).wait(waitTime).exists():
                print("发现{0}".format(description))
                if poco(ClickName).wait(waitTime+1).exists():
                    print("发现{0}按钮，并点击".format(ClickName))
                    poco(ClickName).click()
                    sleep(sleeptime)
                    self.Popuplist.append(description)
                    mylog.info("尝试点击-【{}】-元素成功并加入弹框列表".format(description))
                    return True
                else:
                    mylog.info("尝试点击-【{}】-元素失败".format(description))
                    print("未触发点击")
        except:
            log(Exception("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
            mylog.error("尝试点击-【{}】-元素失败".format(description))
            return False

    def up_use_render__Click_try(self, findName, ClickName, description="", waitTime=0.5, tryTime=1, sleeptime=0, log=True,POCOtype=None):
        """解决上部分黑屏问题，更改渲染"""
        if POCOtype=="Androidpoco":
            poco=self.androidpoco
        else:
            poco=self.poco
            ADBdevice=MyData.ConfData_dir["ADBdevice"]
            if ADBdevice in MyData.mobileconf_dir["up_use_render"]:
                poco.use_render_resolution(True, MyData.mobileconf_dir["up_use_render"][ADBdevice])
        try:
            print("尝试寻找{0}".format(description))
            # gameobject = self.poco(findName)
            if poco(findName).wait(waitTime).exists():
                print("发现{0}".format(description))
                if poco(ClickName).wait(waitTime+1).exists():
                    print("发现{0}按钮，并点击".format(ClickName))
                    poco(ClickName).click()
                    sleep(sleeptime)
                    self.Popuplist.append(description)
                    mylog.info("尝试点击-【{}】-元素成功并加入弹框列表".format(description))
                    return True
                else:
                    mylog.info("尝试点击-【{}】-元素失败".format(description))
                    print("未触发点击")
        except:
            log(Exception("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
            mylog.error("尝试点击-【{}】-元素失败".format(description))
            return False
        poco.use_render_resolution(False, MyData.mobileconf_dir["up_use_render"][ADBdevice])

    def findClick_Image(self, filename, record_pos, description="图片", resolution=(1600, 2560), tryTime=1,waitTime=5):
        """点击图片"""
        width = G.DEVICE.display_info['width']
        height = G.DEVICE.display_info['height']
        file_path = os.path.join(path_RESOURCE_IMAGE, filename)  # 1080, 1920
        # record_pos = (0.432, 0.068),
        try:
            pos=wait(Template((file_path), resolution=resolution),timeout=3)
            touch(pos)
            mylog.info("点击-【{}】-元素成功".format(description))
            print("点击-【{}】-元素成功".format(description))
            return True
        except:return False
    def findSwipe_object(self, objectName, stopPos, POCOobject, swipeTye="y", beginPos=[0.5, 0.5]):
        """滑动元素，stopPos，swipeTye，beginPos"""
        find_element = POCOobject.wait(5)
        swipe_time = 0
        clock()  # 插入计时器
        if swipeTye == "y":
            # snapshot(msg="找到目标元素结果: " + str(find_element.exists()))
            while True:
                print(clock("stop"))
                if float(clock("stop")) > 30:
                    log(Exception("滑动-【{0}】-元素超时".format(objectName)), desc="点击元素失败")
                    raise Exception("滑动{0}超时{1}".format(objectName, clock("stop")))
                if find_element.exists():
                    # 将元素滚动到屏幕中间
                    position1 = find_element.get_position()
                    x, y = position1
                    print("x:", x)
                    print("y:", y)
                    if y < stopPos + 0.1 and y > stopPos - 0.1:
                        return True
                    if y < stopPos:
                        # 元素在上半页面，向下滑动到中间
                        print("元素在上半页面")
                        Pos = beginPos[1] + (stopPos - y)
                        Pos = 1.5 if Pos > 1.5 else Pos
                        self.poco.swipe([beginPos[0], beginPos[1]], [beginPos[0], Pos], duration=2.0)
                    else:
                        print("元素在下半页面")
                        self.poco.swipe([beginPos[0], beginPos[1]], [beginPos[0], beginPos[1] - (y - stopPos)],
                                        duration=2.0)
                    # snapshot(msg="滑动元素到页面中间： " + str(text) + str(textMatches) )
                    find_ele = True
                elif swipe_time < 30:
                    self.poco.swipe([0.5, 0.8], [0.5, 0.4], duration=2.0)
                    # poco.swipe((50, 800), (50, 200), duration=500)
                    swipe_time = swipe_time + 1
                else:
                    log(Exception("查找滑动-【{0}】-元素超时".format(objectName)), desc="查找元素失败")
                    raise Exception("查找滑动-【{0}】-元素超时".format(objectName))
        else:
            while True:
                print(clock("stop"))
                if float(clock("stop")) > 30:
                    log(Exception("滑动-【{0}】-元素超时".format(objectName)), desc="点击元素失败")
                    raise Exception("滑动{0}超时{1}".format(objectName, clock("stop")))
                if find_element.exists():
                    # 将元素滚动到屏幕中间
                    position1 = find_element.get_position()
                    x, y = position1
                    print("x:", x)
                    print("y:", y)
                    if x < stopPos + 0.1 and x > stopPos - 0.1:
                        return True
                    if x < stopPos:
                        # 元素在左半页面，向右滑动到中间
                        print("元素在左半页面")
                        Pos = beginPos[0] + (stopPos - x)
                        Pos = -0.5 if Pos < -0.5 else Pos
                        self.poco.swipe([beginPos[0], beginPos[1]], [Pos, beginPos[1]], duration=2.0)
                    else:
                        print("元素在右半页面")
                        self.poco.swipe([beginPos[0], beginPos[1]], [beginPos[0] - (x - stopPos), beginPos[1]],
                                        duration=2.0)
                    # snapshot(msg="滑动元素到页面中间： " + str(text) + str(textMatches) )
                    find_ele = True
                elif swipe_time < 30:
                    self.poco.swipe([0.5, 0.8], [0.5, 0.4], duration=2.0)
                    # poco.swipe((50, 800), (50, 200), duration=500)
                    swipe_time = swipe_time + 1
                else:
                    log(Exception("查找滑动-【{0}】-元素超时".format(objectName)), desc="查找元素失败")
                    raise Exception("查找滑动-【{0}】-元素超时".format(objectName))
    def mysleep(self, sleeptime:float):
        """会根据设备或其他情况延迟睡眠时间方法"""
        mytime = float(MyData.ConfData_dir["sleepLevel"]) + sleeptime
        sleep(mytime)
    def UIAlterPoP(self):
        if self.find_try("AlterView",description="文本弹框"):
            txt = self.poco("UIAlter").child("AlterView").child("Title").get_TMPtext()
            print("弹框类型：", txt)
            mylog.info("发现-【{}】-类型弹框".format(txt))
            Btn = self.AlterTxt.get(txt)
            self.Popuplist.append(txt)
            print("准备点击按钮", Btn)
            try:
                self.poco(Btn).click()
                print("点击按钮", Btn)
                sleep(2)
            except:
                print("未成功点击按钮")
                return False
# FindObject1=FindObject()
# FindObject1.up_use_render__Click_try("GuideViewBackBtn", "GuideViewBackBtn", description="点击返回箭头", waitTime=5,sleeptime=2)