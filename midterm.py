import pack.modu as lib
import sqlite3
import os


# 設定常數
DB_NAME = os.path.abspath('library.db')
# 指定 CSV 檔案的路徑
csv_file_path = os.path.abspath('users.csv')
# 指定 JSON 檔案的路徑
json_file_path = os.path.abspath('books.json')

# 確保 db 檔案存在
if not os.path.isfile(DB_NAME):
    sf = True
else:
    sf = False

if sf is True:
    lib.create_database(DB_NAME)
    lib.read_users_file(csv_file_path, DB_NAME)
    lib.read_books_file(json_file_path, DB_NAME)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 重複要求使用者輸入帳號和密碼，直到正確
while True:
    # 要求使用者輸入帳號和密碼
    username = input("請輸入帳號: ")
    password = input("請輸入密碼: ")
    # 使用 SQL 查詢核對帳號和密碼
    cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = cursor.fetchone()
    if user:
        # 如果查詢到匹配的使用者，則顯示選單並退出循環
        while True:
            lib.show_menu()
            user_input = input("選擇要執行的功能(Enter離開)：")  # 接受用戶輸入
            if user_input == '':  # 檢查輸入是否為空字符串
                break  # 輸入為空，退出迴圈
            # 使用用戶輸入和 DB_NAME 作為參數調用 lib.menu_function
            lib.menu_function(user_input, DB_NAME)
        break

# 關閉 cursor 和連接
cursor.close()
conn.close()
