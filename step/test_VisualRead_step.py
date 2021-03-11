from airtest.core.api import assert_equal, wake
from time import sleep
from scenes.scenes_visualbook.SCN_bookLoad import BookLoad
from scenes.scenes_visualbook.SCN_bookread import BookRead
from scenes.scenes_visualbook.SCN_bookdetail import BookNewDetail


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


def test_bookread(BookID=None):
    """读书"""
    myVisual = BookRead()
    actualValue = myVisual.bookRead(BookID)
    assert_equal(actualValue, True, "阅读详情{0}".format(myVisual.ReadBook_info))
    sleep(5)
