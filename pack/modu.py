import csv
import json
import sqlite3


def create_database(db_path: str) -> None:
    '''
        建立資料庫
    Args：
        db_path：資料庫位置
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT  NOT NULL
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(30)  NOT NULL,
        publisher VARCHAR(30)  NOT NULL,
        year INTEGER  NOT NULL
    );
    ''')


def read_users_file(csv_file_path: str, db_path: str) -> None:
    '''
        建立使用者資料表
    Args：
        csv_file_path：使用者資料位置

        db_path：資料庫位置
    '''
    try:
        # 連接到 SQLite 資料庫
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # 打開 JSON 檔案並讀取資料
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                # 創建一個 CSV 讀取器
                csv_reader = csv.reader(file)
                # 假設第一行是標題行，跳過它
                next(csv_reader)
                # 迭代 CSV 檔案中的每一行
                for row in csv_reader:
                    # 構建插入語句
                    insert_query = '''INSERT INTO users (username, password)
                        VALUES (?, ?);'''
                    # 執行插入語句
                    cursor.execute(insert_query, (row[0], row[1]))
            # 提交變更（with語句自動提交並關閉連接）
        # print('數據處理完畢，已成功插入數據。')
    except FileNotFoundError:
        print('找不到檔案...')
    except sqlite3.DatabaseError as db_error:
        print(f'資料庫錯誤：{db_error}')
    except Exception as e:
        print('發生未知錯誤...')
        print(f'錯誤代碼為：{e}')


def read_books_file(json_file_path: str, db_path: str) -> None:
    '''
        建立書籍資料表
    Args：
        csv_file_path：書籍資料位置

        db_path：資料庫位置
    '''
    try:
        # 連接到 SQLite 資料庫
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # 打開 JSON 檔案並讀取資料
            with open(json_file_path, mode='r', encoding='utf-8') as file:
                # 讀取 JSON 資料
                books_data = json.load(file)
                # 構建插入語句
                insert_query = '''INSERT INTO books (title, author, publisher, year)
                            VALUES (?, ?, ?, ?);'''
                # 使用 executemany 批量插入
                cursor.executemany(insert_query, [(book['title'], book['author'], book['publisher'], book['year']) for book in books_data])
            # 提交變更（with語句自動提交並關閉連接）
        # print('數據處理完畢，已成功插入數據。')
    except FileNotFoundError:
        print('找不到檔案...')
    except sqlite3.DatabaseError as db_error:
        print(f'資料庫錯誤：{db_error}')
    except Exception as e:
        print('發生未知錯誤...')
        print(f'錯誤代碼為：{e}')


def show_menu() -> None:
    '''
        顯示選單
    '''
    print("\n")
    print("-"*19)
    print("  " + "資料表 CRUD")
    print("-"*19)
    print("  " + "1. 新增圖書")
    print("  " + "2. 刪除圖書")
    print("  " + "3. 修改圖書資訊")
    print("  " + "4. 查詢圖書")
    print("  " + "5. 圖書清單")
    print("-"*19)


def menu_function(choice: str, conn: sqlite3.Connection) -> None:
    '''
        選單功能
    Args：
        choice：選項

        conn：資料庫連結
    '''
    if choice == '1':
        title = input('請輸入要新增的標題：')
        author = input('請輸入要新增的作者：')
        publisher = input('請輸入要新增的出版社：')
        year = input('請輸入要新增的年份：')
        try:
            add_record(conn, title, author, publisher, year)

            print(f'異動 {conn.total_changes} 記錄')
            list_records(conn)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '2':
        book_id = input('請問要刪除哪一本書？')
        try:
            delete_record(conn, book_id)

            print(f'異動 {conn.total_changes} 記錄')
            list_records(conn)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '3':
        list_records(conn)

        book_id = input('請問要修改哪一本書的標題？')
        title = input('請輸入要更改的標題：')
        author = input('請輸入要更改的作者：')
        publisher = input('請輸入要更改的出版社：')
        year = input('請輸入要更改的年份：')
        try:
            update_record(conn, book_id, title, author, publisher, year)

            print(f'異動 {conn.total_changes} 記錄')
            list_records(conn)
        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '4':
        key_word = input('請輸入想查詢的關鍵字：')
        try:
            search_record(conn, key_word)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '5':
        try:
            list_records(conn)

        except ValueError as e:
            print(f"=>:{e}")

    else:
        print('=>無效的選擇')
    # 更新數據
    conn.commit()


def add_record(conn: sqlite3.Connection, title: str, author: str, publisher: str, year: str) -> None:
    '''
        新增紀錄
    Args：
        conn：資料庫連結

        title：書名

        authot：作者

        publisher：出版社

        year：年份
    Raises:
        ValueError: 給定參數為空字串。
    '''
    if title == "" or author == "" or publisher == "" or year == "":
        raise ValueError("給定的條件不足，無法進行新增作業")
    cursor = conn.cursor()
    query = '''INSERT INTO books (title, author, publisher, year)
            VALUES (?, ?, ?, ?);'''
    cursor.execute(query, (title, author, publisher, year))


def delete_record(conn: sqlite3.Connection, title: str) -> None:
    '''
        刪除紀錄
    Args:
        conn: 資料庫連結

        title: 書名
    Raises:
        ValueError: 給定參數為空字串。
    '''
    if title == "":
        raise ValueError("給定的條件不足，無法進行刪除作業")
    cursor = conn.cursor()
    query = '''DELETE FROM books WHERE title = ?;'''
    cursor.execute(query, (title,))


def update_record(conn: sqlite3.Connection, id: str, title: str, author: str, publisher: str, year: str) -> None:
    '''
        修改資料
    Args：
        conn: 資料庫連結

        id: 修改書名

        title：新書名

        authot：新作者

        publisher：新出版社

        year：新年份
    Raises:
        ValueError: 給定參數為空字串。
    '''
    if id == "" or title == "" or author == "" or publisher == "" or year == "":
        raise ValueError("給定的條件不足，無法進行修改作業")
    cursor = conn.cursor()
    query = '''UPDATE books SET title = ?, author = ?, publisher = ?, year = ?
            WHERE title = ?;'''
    cursor.execute(query, (title, author, publisher, year, id))


def search_record(conn: sqlite3.Connection, key_word: str) -> None:
    '''
        搜尋紀錄
    Args:
        conn: 資料庫連結

        key_word: 關鍵字
    Raises:
        ValueError: 給定參數為空字串或找不到參數。
    '''

    if key_word == "":
        raise ValueError("給定的條件不足，無法進行查詢作業")
    cursor = conn.cursor()
    query = '''SELECT title, author, publisher, year FROM books WHERE title = ? OR author = ? OR publisher = ? OR year = ?;'''
    cursor.execute(query, (key_word, key_word, key_word, key_word))
    book = cursor.fetchone()
    if book:
        formatted_str = f"|{book[0]:{chr(12288)}<5}|{book[1]:{chr(12288)}<8}|{book[2]:{chr(12288)}<10}|{book[3]:{chr(12288)}<6}|"
        print(formatted_str)
    else:
        raise ValueError("查無此關鍵字")


def list_records(conn: sqlite3.Connection) -> None:
    '''
        顯示書籍資料庫
    Args:
        conn: 資料庫連結
    Raises:
        ValueError: 不存在資料表。
    '''
    cursor = conn.cursor()
    query = '''SELECT * FROM books;'''
    cursor.execute(query)
    books = cursor.fetchall()
    if books:
        print(f"|{'書籍':{chr(12288)}^5}|{'作者':{chr(12288)}^8}|{'出版社':{chr(12288)}^10}|{'年份':{chr(12288)}^6}|")
        for book in books:
            formatted_str = f"|{book[1]:{chr(12288)}<5}|{book[2]:{chr(12288)}<8}|{book[3]:{chr(12288)}<10}|{book[4]:{chr(12288)}<8}|"
            print(formatted_str)

    else:
        raise ValueError("資料表為空")
