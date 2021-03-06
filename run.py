import logging

from common.COM_path import *
from common.COM_findobject import FindObject
from airtest.report import report
from airtest.report.report import simple_report
from case.test_case import *
# from importlib_metadata.docs import conf
import shutil
from common.COM_analysis import MyAnalysis
from common.COM_devices import CommonDevices
from common.my_log import mylog
from common.COM_utilities import *


# from  airtest.core.android.adb import *
class Run(MyAnalysis):
    logging.DEBUG = 0  # 20

    def __init__(self):
        MyAnalysis.__init__(self)
        print(path_BASE_DIR)
        self.adbpath = os.path.join(path_BASE_DIR, MyData.UserPath_dir["adbpath"])
        print("path_BASE_DIR",self.adbpath)
        self.logpath = os.path.join(path_LOG_DIR, "log.txt")
        print(self.logpath)
        self.logspath = os.path.join(path_LOG_DIR, "logs.txt")
        self.alllogspath = os.path.join(path_LOG_DIR, "alllogs.txt")
        self.errorLogpath = os.path.join(path_LOG_MY, "errorlog.txt")

    def initialize(self):
        """初始化"""
        try:
            print("adb" in os.popen('tasklist /FI "IMAGENAME eq adb.exe"').read())
            print(os.system('TASKKILL /F /IM adb.exe'))  # 杀死进程
            sleep(3)
        except:
            pass
        self.clear()
        CommonDevices()

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
        print("当前执行用例列表:", runlist)
        for i in runlist:
            self.get_eval_value(i["args"], i["func_name"])

    def writelogs(self):
        """转存log到logs"""
        try:
            log_file= open(self.logpath, "r")
            logs_file=open(self.logspath, "a")
            lines = log_file.readlines()
            for val in range(len(lines)):
                # alllog_file = open(alllogspath, "a")
                # alllog_file.write(lines[val])
                # if "assert_equal" in lines[val] or "traceback" in lines[val]:
                logs_file.write(lines[val])
        except Exception as e:
            print("转存log到logs失败",e)
            mylog.error("转存log到logs失败",e)
        else:
            print("转存log到logs成功")
            mylog.info("转存log到logs成功")
        finally:
            log_file.close()
            logs_file.close()

    def pull_errorLog(self):
        """输出errorlog日志转化到log.txt中"""
        print(path_BASE_DIR)
        print(self.adbpath)
        pull = self.adbpath + " pull " + MyData.UserPath_dir["errorLogpath"] + " " + self.errorLogpath
        connected = self.adbpath + " connect " + MyData.EnvData_dir["ADBdevice"]
        print(pull)
        print(connected)
        with open(self.errorLogpath, "w") as errorLog_file:
            pass
        try:
            print(os.system(self.adbpath + " devices"))
            sleep(3)
            print(os.system(connected))
            sleep(3)
            print(os.popen(pull))
            print("完成读取errorlog")
            # if errorLog_file:
            #     lines = errorLog_file.readlines()
            #     print("存在错误日志", errorLog_file.read())
            #     # text_file = open(errorLogpath, "r")
            #     for val in range(len(lines)):
            #         time = 1612407756.9300864 + int(val)
            #         print(type(time))
            #         print("val", val)
            #         print(lines[val])
            #         log(Exception("Unity异常" + lines[val]), timestamp=time)
            # errorLog_file.close()
            # # auto_setup(logdir=path_LOG_DIR)
            # print("输出errorlog日志转化到log.txt中成功")
        except BaseException as e:
            print("输出errorlog日志转化到log.txt中失败",e)

    def togetherReport(self):
        """生成最后的合成日志"""
        htmlname = self.Case_info["casename"] + ".html"
        htmlpath = os.path.join(path_REPORT_DIR, htmlname)
        logspath = os.path.join(path_LOG_DIR, "logs.txt")
        logpath = os.path.join(path_LOG_DIR, "log.txt")
        try:
            with open(logspath, 'r') as f1:
                with open(logpath, 'w') as f2:
                    f2.write(f1.read())
            simple_report(__file__, logpath=path_LOG_DIR, output=htmlpath, MY_DEFAULT_LOG_FILE="logs.txt")
        except:
            print("未发现logs日志")

    def partReport(self, htmlname, k, __title__):
        """分步报告"""
        mylog.info("-------------------------【{0}】执行完毕-----------------".format(__title__))
        print("-----执行完毕-----")
        outputpath = os.path.join(path_REPORT_DIR, htmlname)
        self.writelogs()
        simple_report(__file__, logpath=path_LOG_DIR, output=outputpath)
        self.Case_info[k]["repeattime"] = self.Case_info[k]["repeattime"] - 1
        auto_setup(logdir=path_LOG_DIR)
        mylog.info("完成html测试报告，等待生产录制文件需要一定时间")

    def resetEnv(self, k):
        print(self.Runlist_dir[k])
        if "登陆" in self.Case_info[k]["casename"]:
            pass
        else:
            mylog.info("----------正在进行异常重启------")
            test_startgame(0)
            test_discoverPopup()
        mylog.info("--------完成异常重启------")

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
        mylog.info("完成文件清空")

    def runing(self):
        for k, v in self.Runlist_dir.items():
            repeattime = self.Case_info[k]["repeattime"]
            while (self.Case_info[k]["repeattime"] > 0):
                __author__ = self.Case_info[k]["caseauthor"]
                __title__ = self.Case_info[k]["casename"] + str(repeattime - (self.Case_info[k]["repeattime"] - 1))
                __desc__ = self.Case_info[k]["casedec"]
                recordfile = __title__ + ".mp4"
                htmlname = self.Case_info[k]["reportname"] + str(
                    repeattime - (self.Case_info[k]["repeattime"] - 1)) + ".html"
                # logname = self.Case_info[k]["reportname"] + str(repeattime - (self.Case_info[k]["repeattime"] - 1)) + "log.txt"
                try:
                    start_record()
                    mylog.info("【{0}】启动录制成功".format(__title__))
                except:
                    mylog.info("【{0}】启动录制失败".format(__title__))
                try:
                    self.runcase(self.Runlist_dir[k])
                    self.Case_info[k]["repeattime"] = 0
                except Exception as e:
                    sleep(1)
                    mylog.error("------第出现异常", e)
                    log(e, "------出现异常----------")
                    self.resetEnv(k)
                finally:
                    self.partReport(htmlname=htmlname, __title__=__title__, k=k)
                    try:
                        stop_record(recordfile)
                        mylog.info("【{0}】生成录制文件成功".format(__title__))
                    except:
                        mylog.info("【{0}】生成录制文件失败".format(__title__))


if __name__ == '__main__':
    try:
        myRun = Run()
        myRun.initialize()
        myRun.runing()
    except Exception as e:
        mylog.error("------出现异常{}", e)
        log(e, "------出现异常--------")
    # myRun.pull_errorLog()
    # myRun.writelogs()
    myRun.togetherReport()
