# -*- encoding=utf8 -*-
from time import perf_counter, sleep
from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException, PocoException
from common.COM_utilities import clock
from common.my_log import mylog
from common.COM_devices import CommonDevices
from common.COM_path import *
from common.COM_data import MyData
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


# TODO:截图分辨率需要补充
class CommonPoco(CommonDevices):
    poco = None
    androidpoco = None
    e = None
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
                self.androidpoco = MyData.DeviceData_dir["androidpoco"]
                mylog.info("完成Unity元素定位方法初始化【{}】".format(self.poco))
        if MyData.DeviceData_dir["androidpoco"] == None:
            MyData.DeviceData_dir["androidpoco"] = AndroidUiautomationPoco()
            self.androidpoco = MyData.DeviceData_dir["androidpoco"]
            mylog.info("完成android原生元素定位方法初始化【{}】".format(self.androidpoco))
        self.poco = MyData.DeviceData_dir["poco"]
        self.androidpoco=MyData.DeviceData_dir["androidpoco"]
        # if self.poco == None:
        #     self.poco = UnityPoco()
        #     mylog.info("完成Unity元素定位方法初始化【{}】".format(self.poco))
        # if self.androidpoco==None:
        #     self.androidpoco=AndroidUiautomationPoco()
        #     mylog.info("完成android原生元素定位方法初始化【{}】".format(self.poco))
        #     print("完成android原生元素定位方法初始化【{}】".format(self.poco))
    def find_object(self, findName, description="", waitTime=1, tryTime=1, sleeptime=0):
        """寻找目标"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("正在寻找{0}".format(description))
                if self.poco(findName).wait(waitTime).exists():
                    print("发现{0}".format(description))
                    sleep(sleeptime)
                    mylog.info("等待元素-【{}】--加载成功".format(description))
                    return True
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("等待-【{}】-元素超时".format(description)), desc="等待元素超时")
        raise PocoNoSuchNodeException("等待-【{}】-元素超时".format(description))

    def findClick_object(self, findName, ClickName, description="", waitTime=1, tryTime=1, sleeptime=0):
        """用寻找目标，后并点击"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("正在寻找{0}".format(description))
                gameobject = self.poco(findName)
                if gameobject.wait(waitTime).exists():
                    mylog.info("查找前提条件元素-【{}】--成功".format(findName))
                    if self.poco(ClickName).exists():
                        print("发现{0}点击元素，并点击".format(description))
                        mylog.info("查找点击-【{}】--元素成功".format(description))
                        self.poco(ClickName).click()
                        mylog.info("点击元素-【{}】--成功".format(description))
                        sleep(sleeptime)
                        return True
                    else:
                        print("查找{0}失败".format(description))
                        mylog.error("查找点击元素-【{}】--失败".format(findName))
                else:
                    mylog.error("查找前提条件元素-【{}】--失败".format(findName))
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def find_childobject(self, findPoco, description="", waitTime=1, tryTime=3, sleeptime=0):
        """用于关联父级才能找到的元素"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                gameobject = findPoco
                if gameobject.wait(waitTime).exists():
                    print("发现{0}".format(description))
                    mylog.info("查找点击元素-【{}】--成功".format(description))
                    return True
                else:
                    mylog.error("查找-【{}】-元素失败".format(description))
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def findClick_childobject(self, ClickPoco, description="", waitTime=1, tryTime=1, sleeptime=0.1):
        """用于关联父级才能点击到的元素"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                gameobject = ClickPoco
                if gameobject.wait(waitTime).exists():
                    print("发现{0}".format(description))
                    mylog.info("查找点击元素-【{}】--成功".format(description))
                    sleep(0.2)
                    gameobject.click()
                    sleep(sleeptime)
                    mylog.info("点击元素-【{}】--成功".format(description))
                    return True
                else:
                    mylog.error("查找-【{}】-元素失败".format(description))
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def click_object(self, clickName, waitTime=1, description="", sleeptime=0.3):
        """直接点击，不存在会报错"""
        try:
            self.poco(clickName).click()
            mylog.info("点击元素-【{}】--成功".format(description))
            sleep(sleeptime)
            return True
        except Exception as e:
            mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
            return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))

    def findchildobject_try(self, findPoco, description="", waitTime=0.2, tryTime=1, sleeptime=0):
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
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("正在寻找{0}".format(description))
                gameobject = self.androidpoco(findName)
                if gameobject.wait(waitTime).exists():
                    mylog.info("查找前提条件元素-【{}】--成功".format(findName))
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
                    mylog.error("查找前提条件元素-【{}】--失败".format(findName))
            except Exception as e:
                mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                return False
        log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败")
        raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))


    def findClick_try(self, findName, ClickName, description="", waitTime=0.5, tryTime=1, sleeptime=0, log=True):
        """尝试寻找并点击，不一定存在"""
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                print("尝试寻找{0}".format(description))
                gameobject = self.poco(findName)
                if gameobject.wait(waitTime).exists():
                    print("发现{0}".format(description))
                    if self.poco(ClickName).exists():
                        print("发现{0}按钮，并点击".format(ClickName))
                        self.poco(ClickName).click()
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

    def findClick_Image(self, filename, record_pos, description="", resolution=(1600, 2560), tryTime=1):
        width = G.DEVICE.display_info['width']
        height = G.DEVICE.display_info['height']
        scale = height / width
        if scale > 1.5 and scale < 2.0:
            resolution = (1600, 2560)
            filename = "16_9" + filename
        elif scale > 2.0:
            resolution = (1080, 2340)
            filename = "16_9" + filename
        else:
            resolution = (720, 1080)
            filename = "16_9" + filename
        file_path = os.path.join(path_RESOURCE_IMAGE, filename)  # 1080, 1920
        while (tryTime > 0):
            tryTime = tryTime - 1
            try:
                touch(Template((file_path), record_pos=record_pos, resolution=resolution))
                return True
            except:
                return False
                # mylog.error("查找【{0}】出现未知错误，{1}".format(description, e))
                mylog.error("未触发点击-【{}】-元素".format(description))
        # log(PocoNoSuchNodeException("点击-【{}】-图片失败".format(description)), desc="点击图片失败")
        # raise PocoNoSuchNodeException("点击-【{}】-图片失败".format(description))

    def findSwipe_object(self, objectName, stopPos, POCOobject, swipeTye="y", beginPos=[0.5, 0.5]):
        """滑动元素，stopPos，swipeTye，beginPos"""
        find_element = POCOobject.wait(1)
        swipe_time = 0
        clock()  # 插入计时器
        if swipeTye == "y":
            # snapshot(msg="找到目标元素结果: " + str(find_element.exists()))
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

    def heartBeat(self):
        print("文本框检查")
        sleep(5)
        self.updatePoP()

    def mysleep(self, sleeptime=0):
        """会根据设备或其他情况延迟睡眠时间方法"""
        mytime = float(MyData.ConfData_dir["sleepLevel"]) + sleeptime
        sleep(mytime)

    def updatePoP(self):
        try:
            if self.poco("UIAlter").wait(0.5).attr("visible"):
                print("发现UIAlter")
                if self.poco("AlterView").wait(0.5).attr("visible") == True:
                    print("发现提醒弹框")
                    txt = self.poco("UIAlter").child("AlterView").child("Title").get_TMPtext()
                    print("弹框类型：", txt)
                    mylog.info("发现-【{}】-类型弹框".format(txt))
                    Btn = self.AlterTxt.get(txt)
                    self.Popuplist.append(txt)
                    print("点击按钮", Btn)
                    try:
                        self.poco(Btn).click()
                    except:
                        print("未成功点击按钮")
                        return False
        except:
            pass
