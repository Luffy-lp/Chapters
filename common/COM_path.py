import os
def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print
        path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print
        path + ' 目录已存在'
        return False
# 项目的根路径
path_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 资源路径
path_resource = os.path.join(path_BASE_DIR, "resource")

# 资源图片路径
path_RESOURCE_IMAGE = os.path.join(path_BASE_DIR, "resource/IMAGE")

# yamlfiles路径
path_YAML_FILES = os.path.join(path_BASE_DIR, "yamlfiles")

# 测试用例的目录路径
path_CASE_DIR = os.path.join(path_BASE_DIR, "step/testcases")

# 测试结果的目录路径
path_REPORT_DIR = os.path.join(path_BASE_DIR, "result")

# 测试报告的目录路径
path_REPORT_DIR = os.path.join(path_BASE_DIR, "result/report")

# 测试报告录屏的目录路径
path_RES_DIR = os.path.join(path_BASE_DIR, "result/res")

# airtest日志目录的项目路径
path_LOG_DIR = os.path.join(path_BASE_DIR, "result/log")

# 自定义日志目录的项目路径
path_LOG_MY = os.path.join(path_BASE_DIR, "result/report/mylog")

# 用例数据的项目路径
path_DATA_DIR = os.path.join(path_BASE_DIR, "casedatas")

# 配置文件目录的路径
path_CONF_DIR = os.path.join(path_BASE_DIR, "conf")

# 错误截图存放的路径
path_ERROR_IMAGE = os.path.join(path_BASE_DIR, "result/error_images")


file=os.getcwd()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mkdir(path_REPORT_DIR)#测试结果
mkdir(path_REPORT_DIR)#测试报告
mkdir(path_LOG_MY)#mylog日志
mkdir(path_LOG_DIR)#log日志
mkdir(path_resource)#资源路径
mkdir(path_RESOURCE_IMAGE)#图片资源路径
mkdir(path_RES_DIR)#测试报告录屏的目录路径



