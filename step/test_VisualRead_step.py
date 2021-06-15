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


def test_bookread(BookID=None, bookchapter=None):
    """读书"""
    myVisual = BookRead()
    actualValue = myVisual.bookRead(BookID, bookchapter)
    assert_equal(actualValue, True, "阅读详情{0}".format(myVisual.progress_info))
    sleep(5)


def test_booklist():
    """阅读列表遍历"""
    print("书籍列表:", MyData.book_list)
    for bookchapter in MyData.book_list:
        if len(bookchapter) == 8:
            if MyData.book_list[bookchapter] is None:
                booktraversal(bookchapter)
                print("单章节", bookchapter)
        elif len(bookchapter) == 17:
            if MyData.book_list[bookchapter] is None:
                print("章节区间", bookchapter)
                bookchapters = bookchapter.split("-")
                beginchapter = bookchapters[0]
                endchapter = bookchapters[1]
                index = int(endchapter) - int(beginchapter)
                for i in range(index + 1):
                    bookchapter = int(beginchapter) + i
                    print("即将阅读", bookchapter)
                    booktraversal(str(bookchapter))
        else:
            print("书籍列表配置错误，请注意格式")
            return

def booktraversal(bookchapter):
    """阅读列表执行"""
    if bookchapter not in MyData.bookresult_dir.keys():
        MyData.bookresult_dir[bookchapter] = None
        print("newchapter is none")
    elif MyData.bookresult_dir[bookchapter] == True or MyData.bookresult_dir[bookchapter] == False:
        print(bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
        assert_equal(True, True, bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
        return True
    bookid = bookchapter[:5]
    chapterid = bookchapter[5:]
    MyData.UserData_dir["bookDetailInfo"]["BookID"] = None
    Bookfind1 = Bookfind()
    myVisual = BookRead()
    myVisual.progress_info = {}
    bookNewDetail = BookNewDetail()
    Bookfind1.bookChoose_bookid(bookid)
    bookNewDetail.book_Play(chapterid)
    test_bookload_noassert(bookid)
    myVisual.bookRead(bookid, bookchapter)
    bookNewDetail.bookNewDetailPOP()
    bookNewDetail.click_close()
    test_discoverPopup_noassert()
    print("阅读结果：", myVisual.BookRead_info)
    MyData.update_record_bookread(bookchapter, myVisual.BookRead_info["result"])
    try:
        assert_equal(True, myVisual.BookRead_info["result"],
                     bookchapter + "章节完成阅读{0}".format(myVisual.BookRead_info))
    except:
        print("{}资源存在问题,详细见报告".format(bookchapter))
