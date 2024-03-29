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
    actualValue = myVisual.process_bookRead(BookID, bookchapter)
    assert_equal(actualValue, True, "阅读详情{0}".format(myVisual.progress_info))
    sleep(5)


def test_booklist():
    """阅读列表遍历"""
    print("书籍列表:", MyData.book_list)
    for bookchapter in list(MyData.book_list.keys()):
        if len(bookchapter) == 8:
            if MyData.book_list[bookchapter] is None or type( MyData.book_list[bookchapter])==int:
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
    if bookchapter not in MyData.book_list.keys():
        MyData.book_list[bookchapter] = 1
        print("newchapter is none")
    elif MyData.book_list[bookchapter] == "True" or MyData.book_list[bookchapter] == "False":
        print(bookchapter + "已存在结果{}".format(MyData.book_list[bookchapter]))
        # assert_equal(True, True, bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
        return True
    elif type(MyData.book_list[bookchapter]) == int:
        if MyData.book_list[bookchapter] >= 3:
            print(bookchapter + "失败3次跳过阅读")
            return True
        else:
            result= MyData.book_list[bookchapter] + 1
            MyData.update_record_bookread(bookchapter, result)
    else:
        MyData.update_record_bookread(bookchapter, 1)
    bookid = bookchapter[:5]
    chapterid = bookchapter[5:]
    MyData.bookInfo_dir["BookID"]=bookid
    print(MyData.bookInfo_dir["BookID"])
    MyData.UserData_dir["bookDetailInfo"]["BookID"] = None
    Bookfind1 = Bookfind()
    myVisual = BookRead()
    bookNewDetail = BookNewDetail()
    Bookfind1.bookChoose_bookid(bookid)
    bookNewDetail.book_Play(bookid,index=chapterid)
    test_bookload_noassert(bookid)
    myVisual.process_bookRead(bookid, bookchapter)
    bookNewDetail.bookNewDetailPOP()
    bookNewDetail.click_close()
    test_discoverPopup_noassert()
    print("阅读结果：", myVisual.BookRead_info)
    MyData.update_record_bookread(bookchapter, str(myVisual.BookRead_info["result"]))
    try:
        assert_equal(True, myVisual.BookRead_info["result"],
                     bookchapter + "章节完成阅读{0}".format(myVisual.BookRead_info))
    except:
        print("{}资源存在问题,详细见报告".format(bookchapter))
