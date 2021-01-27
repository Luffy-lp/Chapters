from time import perf_counter, sleep
from airtest.core.api import *
import re
from common.COM_path import *
import yaml
import types
from airtest.core.android.recorder import *
# from common.COM_data import MyData
spendtime = None


def screenshot(loc_desc):
    date_decs = time.strftime("%Y-%m-%d_%H_%M_%S")
    filename = date_decs + loc_desc + ".png"
    file_path = os.path.join("ERROR_IMAGE", filename)
    try:
        # 获取当前时间，并转换为指定格式的字符串
        date_decs = time.strftime("%Y-%m-%d_%H_%M_%S")
        filename = date_decs + loc_desc + ".png"
        print(filename)
        file_path = os.path.join("D://ERROR_IMAGE/", filename)
        print(file_path)
        snapshot(filename=file_path, msg=loc_desc)
    except Exception as e:
        print(e)
        raise e


def PosTurn(pos):  # 坐标转化
    width = G.DEVICE.display_info['width']
    height = G.DEVICE.display_info['height']
    POS = [pos[0] * width, pos[1] * height]
    return POS


def read_yaml(filepath):
    with open(filepath, encoding='utf-8') as file:
        value = yaml.safe_load(file)
    return value


def clock(type=None):  # 计时器
    """stop结束返回时间"""
    global start_time
    if type == "stop":
        spendtime = '%.2f' % (perf_counter() - start_time)
        print("spendtime:", spendtime)
        return spendtime
    else:
        start_time = perf_counter()


def start_record(maxtime=3600):
    """录屏功能，start,stop"""
    G.DEVICE.start_recording(max_time=maxtime)
    # print(MyData.ConfData_dir)
    # Recorder(MyData.DeviceData_dir["ADB"]).start_recording()
    print("启动录制")
    # maxtime = maxtime

def stop_record(filename):
    file_path = os.path.join(path_RES_DIR, filename)
    print("file_path",file_path)
    G.DEVICE.stop_recording(output=file_path)
    # G.DEVICE.stop_recording(output=file_path)
