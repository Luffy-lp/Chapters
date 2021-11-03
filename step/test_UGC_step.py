from airtest.core.api import assert_equal, wake
from time import sleep
from scenes.scenes_community.SCN_IntroduceEdit import IntroduceEdit
from scenes.scenes_community.SCN_creation import Creation
from scenes.scenes_community.SCN_chapteredit import ChapterEdit
from scenes.scenes_community.SCN_community import Community
from scenes.scenes_community.SCN_readUGCbook import ReadUGCBook
from scenes.scenes_community.SCN_mainstudio import MainStudio

def test_Creation():
    """创建书籍"""
    Community1 = Community()
    actualValueinto_workshop = Community1.into_workshop()
    assert_equal(actualValueinto_workshop, True, "进入工作室{0}")
    Creation1 = Creation()
    isCreation = Creation1.process_createNewBook()
    assert_equal(isCreation, True, "创建书籍")

# def test_ChapterEdit(storyName):
#     """编写小说"""
#     myChapterEdit = ChapterEdit()
#     actualValue = myChapterEdit.process_creationStoryFlow(storyName)
#     assert_equal(actualValue, True, "创作小说{0}".format(myChapterEdit.ChapterEdit_info))
#     sleep(5)

def test_ChapterEdit():
    """创作工作室流程"""
    MYMainStudio=MainStudio()
    txt = "abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghi" \
          "jklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz"
    MYMainStudio.LuaUIStudio()
    MYMainStudio.creatCharacter("lipeng", "main")
    MYMainStudio.creatCharacter("lilei")
    MYMainStudio.talk("Narration", "1")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    MYMainStudio.talk("Narration", "2")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    MYMainStudio.talk("Narration", "3")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    assert_equal(True, True, "创作工作室流程")
def test_branch():
    """分支创作选项流程"""
    MYMainStudio=MainStudio()
    # MYMainStudio.branchprocess()
    MYMainStudio.click_addChoice()  # 点击工具弹框添加选项按钮
    MYMainStudio.creat_Choice("OptionC", "这是C选项")  # 创建新选项
    MYMainStudio.editorOptionDES("OptionC", "这是C选项")  # 修改选项描述
    MYMainStudio.click_Paperplanebutton()  # 提交内容
    MYMainStudio.editorOptionDES("OptionA", "这是A选项")
    MYMainStudio.click_Paperplanebutton()
    MYMainStudio.editorOptionDES("OptionB", "这是B选项")
    MYMainStudio.click_Paperplanebutton()
    MYMainStudio.click_confirm()  # 点击confirm按钮
    # self.click_con()
    MYMainStudio.intoOption("OptionA")  # 选择进入的选项编辑
    txt = "abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghi" \
          "jklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz"
    # self.creatCharacter("lipeng", "main")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    MYMainStudio.toolBar("Jump")
    MYMainStudio.back_click()
    MYMainStudio.intoOption("OptionB")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    MYMainStudio.toolBar("Jump")
    MYMainStudio.back_click()
    MYMainStudio.intoOption("OptionC")
    MYMainStudio.talk("lipeng", txt)
    MYMainStudio.talk("lilei", txt)
    MYMainStudio.toolBar("Jump")
def test_IntroduceEdit(bookname):
    """书籍详情和审核"""
    ChapterEdit1=ChapterEdit()
    ChapterEdit1.into_IntroduceEdit()
    IntroduceEdit1=IntroduceEdit()
    actualValue=IntroduceEdit1.mainprocess(bookname)
    assert_equal(actualValue, True, "书籍详情和审核")
    actualValue=ChapterEdit1.getChapterEdit_info()
    assert_equal(actualValue, True, "书籍详情{0}".format((ChapterEdit1.ChapterEdit_info)))

def test_chooseUGCBook(index_x=0, index_y=0):
    """选择UGC书籍"""
    myReadUGCBook = ReadUGCBook()
    myReadUGCBook.choosebook()


def test_ReadUGCBook(time=2):
    """短信小说阅读"""
    myReadUGCBook = ReadUGCBook()
    myReadUGCBook.click_Read()
    actualValue = myReadUGCBook.bookRead(time)
    assert_equal(actualValue, True, "短信小说阅读{0}".format(myReadUGCBook.ReadUGCBook_info))