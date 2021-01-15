import logging
from airtest.cli.parser import cli_setup
from airtest.core.android.adb import ADB
from airtest.core.api import *
from common.COM_data import MyData
from common.COM_path import *
from common.my_log import mylog

class CommonDevices():
    def __init__(self):
        if G.DEVICE == None:
            if not cli_setup():
                conf = MyData.ConfData_dir["device"] + "://" + MyData.ConfData_dir["ADBip"] + "/" + MyData.ConfData_dir[
                    "ADBdevice"]
                method = MyData.ConfData_dir["method"]
                auto_setup(__file__, logdir=path_LOG_DIR, devices=[conf + method,], project_root=path_BASE_DIR)
                print("__file__",__file__)
                logging.DEBUG = 0
                self.getADBdevice()
                # mylog.info("完成DEVICE初始化",G.DEVICE)
                print("DEVIEC:", G.DEVICE)
    def getADBdevice(self):
        adb = ADB(serialno=MyData.ConfData_dir["ADBdevice"])
        MyData.DeviceData_dir["ADB"] = adb

    def getdevlist(self):
        devlist = []
        connectfile = os.popen('adb devices')
        list = connectfile.readlines()
        # print(list)
        for i in range(len(list)):
            if list[i].find('\tdevice') != -1:
                temp = list[i].split('\t')
                devlist.append(temp[0])
        return devlist

    def checkAdbConnectability(self,flag=0):
        '''
        flag =0时，当连接正常时返回True(default)
        flag!=0时，直接打印出结果
        '''
        connectstring = '''ADB连接失败, 请check以下项:
        1. 是否有连接上手机？请连接上手机选并重新check连接性!
        2. 是否有开启"开发者选项\\USB调试模式"?\n'''
        connectinfolist = self.getdevlist()

        if len(connectinfolist) == 0:
            return False
        if len(connectinfolist) == 1:
            if flag != 0:
                print('连接正常')
                print(f'设备SN: {connectinfolist[0]}')
            else:
                return True
        if len(connectinfolist) >= 2:
            print('连接正常，当前有连接多台设备. ')
            for i in range(len(connectinfolist)):
                print(f'设备{i + 1} SN: {connectinfolist[i]}')
            return True
# CommonDevices1=CommonDevices()
# # print("dddd:",os.getenv('com.mars.avgchapters'))
