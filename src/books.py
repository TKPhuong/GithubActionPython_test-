import sqlite3


class Book:
    def __init__(self, book_id, title, author):
        # 本のID、タイトル、著者名を設定する
        self.book_id = book_id
        self.title = title
        self.author = author

    def __eq__(self, other):
        # 他の本と等価であるかどうかを判定する
        if isinstance(other, Book):
            return (
                self.book_id == other.book_id
                and self.title == other.title
                and self.author == other.author
            )
        return False

    def __repr__(self):
        # 本のタイトルと著者名を文字列として返す
        return f"{self.title} by {self.author}"


class BooksDB:
    def __init__(self, db_path):
        # SQLiteのデータベースとの接続を作成
        self.conn = sqlite3.connect(db_path)
        # booksテーブルが存在しない場合は作成する
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY, 
                title TEXT, 
                author TEXT
            )
        """
        )
        self.conn.commit()

    def add_book_by_id(self, book_id, title, author):
        # book_idをキーとして、bookテーブルから本の情報を検索
        cursor = self.conn.execute("SELECT id FROM books WHERE id=?", (book_id,))
        # book_idがすでにテーブルに存在する場合は、本の情報を更新
        if cursor.fetchone() is not None:
            self.conn.execute(
                """
                UPDATE books 
                SET title=?, 
                    author=? 
                WHERE id=?""",
                (title, author, book_id),
            )
        # book_idがテーブルに存在しない場合は、本の情報を追加
        else:
            self.conn.execute(
                """
                INSERT INTO books (id, title, author) 
                VALUES (?,?,?) """,
                (book_id, title, author),
            )
        self.conn.commit()

    def get_book_by_id(self, book_id):
        # book_idをキーとして、bookテーブルから本の情報を検索
        cursor = self.conn.execute(
            """SELECT id, title, author
                                     from books 
                                     where id=?""",
            (book_id,),
        )
        book = cursor.fetchone()
        # book_idがテーブルに存在しない場合はエラーを発生
        if book is None:
            raise ValueError("Book with id {} not found".format(book_id))
        return Book(*book)

    def delete_book(self, book_id):
        # booksテーブルからbook_idをキーとして、対象の本の情報を削除
        cursor = self.conn.execute("DELETE from books where id=?", (book_id,))
        # 削除された行数が0の場合は、book_idが見つからないことを示してエラーを発生
        if cursor.rowcount == 0:
            raise ValueError("Book with id {} not found".format(book_id))
        self.conn.commit()

    def get_books(self):
        # booksテーブルから全ての本の情報を取得
        cursor = self.conn.execute("SELECT id, title, author from books")
        # 取得した本の情報をBookオブジェクトに変換してリストとして返す
        return [Book(*row) for row in cursor]
