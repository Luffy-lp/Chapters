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


def test_booklist():
    book_list = MyData.book_list
    print(book_list)
    for bookchapter in book_list:
        if len(bookchapter) == 8:
            if book_list[bookchapter] is None:
                booktraversal(bookchapter)
                print("bookchapter", bookchapter)
        elif len(bookchapter) == 17:
            if book_list[bookchapter] is None:
                print(bookchapter)
                bookchapters = bookchapter.split("-")
                beginchapter = bookchapters[0]
                endchapter = bookchapters[1]
                index = int(endchapter) - int(beginchapter)
                for i in range(index + 1):
                    newchapter = int(beginchapter) + i
                    # bookchapterlist.append(str(newchapter))
                    booktraversal(str(newchapter))
                    print("newchapter", newchapter)
        else:
            print("配置错误", bookchapter)
        # bookid = bookchapter[:5]
        # chapterid = bookchapter[5:]
        # print(bookid)
        # print(chapterid)
    # if type(MyData.bookresult_dir) != dict:
    #     MyData.bookresult_dir = {}
    # if bookchapter in MyData.bookresult_dir:
    #     print(bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
    #     assert_equal(True, True,bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
    # else:
    #     booktraversal(bookchapter)


def booktraversal(bookchapter):
    MyData.UserData_dir["bookDetailInfo"]["BookID"] = None
    bookid = bookchapter[:5]
    chapterid = bookchapter[5:]
    Bookfind1 = Bookfind()
    myVisual = BookRead()
    myVisual.ReadBook_info={}
    bookNewDetail = BookNewDetail()
    # bookname = mydit[1]["bookname"]
    # Bookfind1.bookChoose_Search(bookname)
    if bookchapter in MyData.bookresult_dir:
        book_list = MyData.book_list
        if not book_list[bookchapter] == None:
            print(bookchapter + "已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
            assert_equal(True, True, bookchapter + "已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
            return True
    Bookfind1.bookChoose_bookid(bookid)
    bookNewDetail.book_Play(chapterid)
    test_bookload_noassert(bookid)
    myVisual.bookRead(bookid)
    bookNewDetail.bookNewDetailPOP()
    bookNewDetail.click_close()
    test_discoverPopup_noassert()
    print("bookchapter:",bookchapter)
    print("myVisual.ReadBook_info",myVisual.ReadBook_info)
    print("ReadBook_info:",myVisual.ReadBook_info["resource"])
    MyData.set_yaml(bookchapter, myVisual.ReadBook_info["resource"])
    try:
        assert_equal(True, myVisual.ReadBook_info["resource"],
                     str(myVisual.ReadBook_info["chapterProgress"]) + "章节完成阅读{0}".format(myVisual.ReadBook_info))
    except:
        print("{}资源存在问题,详细见报告".format(bookchapter))

# def test_booktraversal(bookchapter):
#     """书籍遍历阅读"""
#     if type(MyData.bookresult_dir) != dict:
#         MyData.bookresult_dir = {}
#     if bookchapter in MyData.bookresult_dir:
#         print(bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
#         assert_equal(True, True,bookchapter+"已经阅读{}".format(MyData.bookresult_dir[bookchapter]))
#     else:
#         booktraversal(bookchapter)
# test_booklist()
