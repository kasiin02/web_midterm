import csv
import json
import sqlite3


def create_database(db_path: str):
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


def read_users_file(csv_file_path: str, db_path: str):
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


def read_books_file(json_file_path: str, db_path: str):
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


def show_menu():
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


def menu_function(choice, db_path):
    '''
        選單功能
    Args：
        choice：選項

        db_path：資料庫位置
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if choice == '1':
        title = input('請輸入要新增的標題：')
        author = input('請輸入要新增的作者：')
        publisher = input('請輸入要新增的出版社：')
        year = input('請輸入要新增的年份：')
        try:
            add_record(cursor, title, author, publisher, year)

            print('異動 1 記錄')
            list_records(cursor)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '2':
        book_id = input('請問要刪除哪一本書？')
        try:
            delete_record(cursor, book_id)

            print('異動 1 記錄')
            list_records(cursor)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '3':
        list_records(cursor)

        book_id = input('請問要修改哪一本書的標題？')
        title = input('請輸入要更改的標題：')
        author = input('請輸入要更改的作者：')
        publisher = input('請輸入要更改的出版社：')
        year = input('請輸入要更改的年份：')
        try:
            update_record(cursor, book_id, title, author, publisher, year)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '4':
        key_word = input('請輸入想查詢的關鍵字：')
        try:
            search_record(cursor, key_word)

        except ValueError as e:
            print(f"=>:{e}")

    elif choice == '5':
        try:
            list_records(cursor)

        except ValueError as e:
            print(f"=>:{e}")

    else:
        print('=>無效的選擇')
    # 更新數據
    conn.commit()


def add_record(cursor: any, title: str, author: str, publisher: str, year: str):
    '''
        新增紀錄
    Args：
        cursor：資料庫連結

        title：書名

        authot：作者

        publisher：出版社

        year：年份
    '''
    if title == "" or author == "" or publisher == "" or year == "":
        raise ValueError("給定的條件不足，無法進行新增作業")

    query = '''INSERT INTO books (title, author, publisher, year)
            VALUES (?, ?, ?, ?);'''
    cursor.execute(query, (title, author, publisher, year))


def delete_record(cursor: any, title: str):
    '''
        刪除紀錄
    Args:
        cursor: 資料庫連結

        title: 書名
    '''
    if title == "":
        raise ValueError("給定的條件不足，無法進行刪除作業")

    query = '''DELETE FROM books WHERE title = ?;'''
    cursor.execute(query, (title,))


def update_record(cursor: any, id: str, title: str, author: str, publisher: str, year: str):
    '''
        修改資料
    Args：
        cursor: 資料庫連結

        id: 修改書名

        title：新書名

        authot：新作者

        publisher：新出版社

        year：新年份
    '''
    if id == "" or title == "" or author == "" or publisher == "" or year == "":
        raise ValueError("給定的條件不足，無法進行修改作業")

    query = '''UPDATE books SET title = ?, author = ?, publisher = ?, year = ?
            WHERE title = ?;'''
    cursor.execute(query, (title, author, publisher, year, id))
    print('異動 1 記錄')
    list_records(cursor)


def search_record(cursor: any, key_word: str):
    '''
        搜尋紀錄
    Args:
        cousor: 資料庫連結

        key_word: 關鍵字
    '''

    if key_word == "":
        raise ValueError("給定的條件不足，無法進行查詢作業")

    query = '''SELECT * FROM books WHERE title = ? OR author = ? OR publisher = ? OR year = ?;'''
    cursor.execute(query, (key_word, key_word, key_word, key_word))
    book = cursor.fetchone()
    if book:
        formatted_str = "| {:<10} | {:<10} | {:<15} | {:<6} |".format(book[1], book[2], book[3], book[4])
        print(formatted_str)
    else:
        raise ValueError("查無此關鍵字")


def list_records(cursor: any):
    '''
        顯示書籍資料庫
    Args:
        cursor: 資料庫連結
    '''

    query = '''SELECT * FROM books;'''
    cursor.execute(query)
    books = cursor.fetchall()
    if books:
        print("|{:^9}|{:^12}|{:^13}|{:^9}|".format("title", "author", "publisher", "year"))
        for book in books:
            formatted_str = "|{:<8}|{:<7}|{:<8}|{:<9}|".format(book[1], book[2], book[3], book[4])
            print(formatted_str)

    else:
        raise ValueError("資料表為空")
