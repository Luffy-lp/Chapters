from common.COM_path import *
from common.COM_findobject import CommonPoco
from airtest.report import report
from airtest.report.report import simple_report
from case.test_case import *
from importlib_metadata.docs import conf
import shutil
from common.COM_analysis import MyAnalysis
from common.COM_devices import CommonDevices
from common.my_log import mylog
from common.COM_utilities import *


class Run(MyAnalysis):
    def __init__(self):
        MyAnalysis.__init__(self)

    def get_eval_value(self, args, func_name):

        if not args:
            func_name = func_name + "()"
            eval(func_name)
            print("func_name not args:", func_name)
            return
        if isinstance(args[0], int):
            for i in args:
                if isinstance(i, int):
                    func_name = func_name + i + ", "
        elif isinstance(args[0], str):
            func_name = func_name + "(" + "\"" + '", "'.join(args) + "\"" + ")"
        print("func_name have args:", func_name)
        eval(func_name)
        return func_name

    def runcase(self, runlist):
        print("Runlist:", runlist)
        for i in runlist:
            self.get_eval_value(i["args"], i["func_name"])

    def runing(self):
        CommonDevices1 = CommonDevices()
        for k, v in self.Runlist_dir.items():
            repeattime = self.Case_info[k]["repeattime"]
            while (self.Case_info[k]["repeattime"] > 0):
                htmlname = self.Case_info[k]["reportname"] + str(
                    repeattime - (self.Case_info[k]["repeattime"] - 1)) + ".html"
                logname=self.Case_info[k]["reportname"] + str(
                    repeattime - (self.Case_info[k]["repeattime"] - 1)) + "log.txt"
                __author__ = self.Case_info[k]["caseauthor"]
                __title__ = self.Case_info[k]["casename"] + str(repeattime - (self.Case_info[k]["repeattime"] - 1))
                recordfile = __title__ + ".mp4"
                print("__title__:", __title__)
                __desc__ = self.Case_info[k]["casedec"]
                try:
                    start_record()
                except:mylog.info("【{0}】启动录制失败".format(__title__))
                try:
                    self.runcase(self.Runlist_dir[k])
                    self.Case_info[k]["repeattime"] = 0
                except:
                    mylog.error("------出现异常{}")
                    MyData.DeviceData_dir["poco"]=None
                    test_startgame()
                    test_newUserGuide()
                    test_discoverPopup()
                finally:
                    outputpath = os.path.join(path_REPORT_DIR, htmlname)
                    logpath=os.path.join(path_LOG_DIR, logname)
                    simple_report(__file__, logpath=path_LOG_DIR, output=outputpath)
                    self.Case_info[k]["repeattime"] = self.Case_info[k]["repeattime"] - 1
                    mylog.info("完成html测试报告，等待生产录制文件需要一定时间")
                    try:
                        stop_record(recordfile)
                    except:
                        mylog.info("【{0}】生成录制文件失败".format(__title__))
                    auto_setup(logdir=path_LOG_DIR)
                    mylog.info("-------------------------【{0}】执行完毕-----------------".format(__title__))
                    print("-----执行完毕-----")


if __name__ == '__main__':
    print("adb" in os.popen('tasklist /FI "IMAGENAME eq adb.exe"').read())
    # 杀死进程
    print(os.system('TASKKILL /F /IM adb.exe'))
    sleep(3)
    myRun = Run()
    myRun.runing()