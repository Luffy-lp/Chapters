import poco.utils.six as six
class MyException(Exception):
    """
    Base class for errors and exceptions of MY. It is Python3 compatible.
    """
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage
    def __str__(self):
        print("自定义异常" + str(self.errorMessage))
# try:
#     if 1<4:
#         raise MyException("爹爹当当")
# except MyException as e_result:
#     print("打印异常信息：",e_result)