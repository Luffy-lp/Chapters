import logging
from airtest.cli.parser import cli_setup
from airtest.core.android.adb import ADB
from airtest.core.api import *
from common.COM_data import MyData
from common.COM_path import *
from common.my_log import mylog

class CommonDevices():
    androidpoco = None
    def __init__(self):
        if G.DEVICE == None:
            if not cli_setup():
                conf = MyData.ConfData_dir["device"] + "://" + MyData.ConfData_dir["ADBip"] + "/" + MyData.ConfData_dir[
                    "ADBdevice"]
                print("conf:",conf)
                method = MyData.ConfData_dir["method"]
                auto_setup(__file__, logdir=path_LOG_DIR, devices=[conf + method,], project_root=path_BASE_DIR)
                adb = ADB(serialno=MyData.ConfData_dir["ADBdevice"])
                MyData.DeviceData_dir["ADB"] = adb
                logging.DEBUG = 0
                # mylog.info("完成DEVICE初始化",G.DEVICE)
                print("DEVIEC:", G.DEVICE)
