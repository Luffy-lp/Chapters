from airtest.core.api import assert_equal, wake
from time import sleep
from scenes.scenes_community.SCN_creation import Creation
from scenes.scenes_community.SCN_chapteredit import ChapterEdit
from scenes.scenes_community.SCN_community import Community
from scenes.scenes_community.SCN_readUGCbook import ReadUGCBook

def test_Creation():
    """创建书籍"""
    Community1 = Community()
    actualValueinto_workshop = Community1.into_workshop()
    assert_equal(actualValueinto_workshop, True, "进入工作室{0}")
    Creation1 = Creation()
    isCreation = Creation1.process_createNewBook()
    assert_equal(isCreation, True, "创建书籍")


def test_ChapterEdit(storyName):
    """编写小说"""
    myChapterEdit = ChapterEdit()
    actualValue = myChapterEdit.process_creationStoryFlow(storyName)
    assert_equal(actualValue, True, "创作小说{0}".format(myChapterEdit.ChapterEdit_info))
    sleep(5)


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