import pytest
from src.books import Book, BooksDB

# fixture 関数によって作成される `db` は各テスト関数に渡されます
@pytest.fixture
def db():
    # BooksDB インスタンスを作成します
    db = BooksDB("books.db")
    # テストが実行される前に yield します
    yield db
    # テストが完了した後にデータベース接続を閉じます
    db.conn.close()


# テストデータをパラメータとして持つテスト関数を定義します
@pytest.mark.parametrize(
    "book_id, title, author",
    [
        (1, "The Great Gatsby", "F. Scott Fitzgerald"),
        (2, "To Kill a Mockingbird", "Harper Lee"),
        (3, "Moby Dick", "Herman Melville"),
    ],
)
def test_add_book_by_id(db, book_id, title, author):
    # 書籍を追加します
    db.add_book_by_id(book_id, title, author)
    # 追加された書籍を取得します
    book = db.get_book_by_id(book_id)
    # 追加された書籍のタイトルと著者名が正しいことをアサートします
    assert book.title == title
    assert book.author == author


# テストデータをパラメータとして持つテスト関数を定義します
@pytest.mark.parametrize(
    "book_id, title, author",
    [
        (1, "The Great Gatsby", "F. Scott Fitzgerald"),
        (2, "To Kill a Mockingbird", "Harper Lee"),
        (3, "Moby Dick", "Herman Melville"),
    ],
)
def test_get_book_by_id(db, book_id, title, author):
    # 書籍を追加します
    db.add_book_by_id(book_id, title, author)
    # 追加された書籍を取得します
    book = db.get_book_by_id(book_id)
    # 追加された書籍のタイトルと著者名が正しいことをアサートします
    assert book.title == title
    assert book.author == author


def test_get_book_not_found(db):
    # 指定された本が存在しない場合に、ValueErrorが発生することを確認するテスト
    with pytest.raises(ValueError) as e:
        db.get_book_by_id(100)
    assert str(e.value) == "Book with id 100 not found"


@pytest.mark.parametrize("book_id", [1, 2, 3])
def test_delete_book(db, book_id):
    # 本の削除機能のテスト
    db.add_book_by_id(book_id, "title", "author")
    db.delete_book(book_id)
    with pytest.raises(ValueError) as e:
        db.get_book_by_id(book_id)
    assert str(e.value) == f"Book with id {book_id} not found"


@pytest.mark.xfail(raises=ValueError, reason="Book with id 5 not found")
def test_delete_book_not_found(db):
    # 存在しない本を削除する際に、ValueErrorが発生することを確認するテスト
    db.delete_book(5)


def test_get_books(db):
    # 全ての本の情報を取得するテスト
    books = [
        Book(1, "The Great Gatsby", "F. Scott Fitzgerald"),
        Book(2, "To Kill a Mockingbird", "Harper Lee"),
        Book(3, "Moby Dick", "Herman Melville"),
    ]

    for book in books:
        db.add_book_by_id(book.book_id, book.title, book.author)

    books_in_db = db.get_books()

    for book in books:
        print(book, books_in_db)
        assert book in books_in_db


@pytest.mark.skip(reason="まだ実装されていない")
def test_search_book(books_db):
    # 本の検索機能のテスト
    pass
