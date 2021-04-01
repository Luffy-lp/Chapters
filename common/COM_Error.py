import poco.utils.six as six
class MYError(Exception):
    """
    Base class for errors and exceptions of MY. It is Python3 compatible.
    """
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
    def __str__(self):
      return f"资源异常"

class ResourceError(MYError):
    """
    书籍资源类异常
    """
    def __init__(self):
        ResourceError.__init__(self)
    def __init__(self,errorMessage,bookid=None,chapterProgress=None,chatProgress=None,type=None):
        self.errorMessage = errorMessage
        self.booid=bookid
        self.chapterProgress=chapterProgress
        self.chatProgress=chatProgress
        self.type=type
    def __str__(self):
      return f"书籍资源异常"
# try:
#     if 1 < 4:
        # raise ResourceError("ddddd", "11111", "10003", "10003002", "10dfasf")
# except ResourceError as e:
#     print(e.booid)
#     print(e)
