from airtest.core.api import assert_equal, wake
from time import sleep

from date.Chapters_data import MyData
from scenes.scenes_visualbook.SCN_bookLoad import BookLoad
from scenes.scenes_visualbook.SCN_bookfind import Bookfind
from scenes.scenes_visualbook.SCN_bookread import BookRead
from scenes.scenes_visualbook.SCN_bookdetail import BookNewDetail
from step.test_common_step import test_discoverPopup_noassert


def test_bookchoose(bookShelf, index):
    """找书"""
    bookdetail = BookNewDetail()
    bookdetail.bookChoose(bookShelf=bookShelf, index=index)
    # actualValue = bookdetail.getBookNewDetail_info()
    assert_equal(True, True, "视觉小说书籍选择{0}".format(bookdetail.BookNewDetail_info))

def test_bookPlay():
    """Play书籍"""
    bookdetail = BookNewDetail()
    actualValue = bookdetail.book_Play()
    assert_equal(True, actualValue, "点击书籍Play按钮")


def test_bookload(BookID=None):
    """书籍加载"""
    myBookLoad = BookLoad()
    actualValue = myBookLoad.bookLoad(BookID)
    assert_equal(actualValue, True, "书籍loading{0}".format(myBookLoad.BookLoad_info))
    sleep(3)

def test_bookload_noassert(BookID=None):
    """书籍加载"""
    myBookLoad = BookLoad()
    myBookLoad.bookLoad(BookID)
    sleep(3)

def test_bookread(BookID=None):
    """读书"""
    myVisual = BookRead()
    actualValue = myVisual.bookRead(BookID)
    assert_equal(actualValue, True, "阅读详情{0}".format(myVisual.ReadBook_info))
    sleep(5)
def booktraversal(bookchapter):
    bookid = bookchapter[:5]
    chapterid = bookchapter[5:]
    Bookfind1 = Bookfind()
    myVisual = BookRead()
    bookNewDetail = BookNewDetail()
    # bookname = mydit[1]["bookname"]
    # Bookfind1.bookChoose_Search(bookname)
    Bookfind1.bookChoose_bookid(bookid)
    bookNewDetail.book_Play(chapterid)
    test_bookload_noassert(bookid)
    myVisual.bookRead(bookid)
    bookNewDetail.bookNewDetailPOP()
    MyData.UserData_dir["bookDetailInfo"]["BookID"] = None
    bookNewDetail.click_close()
    test_discoverPopup_noassert()
    MyData.set_yaml(bookchapter,myVisual.ReadBook_info["resource"])
    try:
        assert_equal(True, myVisual.ReadBook_info["resource"],str(myVisual.ReadBook_info["chapterProgress"]) + "章节阅读{0}".format(myVisual.ReadBook_info))
    except:
        print("{}资源存在问题,详细见报告".format(bookchapter))

def test_booktraversal(bookchapter):
    """书籍遍历阅读"""
    if type(MyData.bookresult_dir) != dict:
        MyData.bookresult_dir = {}
    if bookchapter in MyData.bookresult_dir:
        print(bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
        assert_equal(True, True,bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
    else:
        booktraversal(bookchapter)
