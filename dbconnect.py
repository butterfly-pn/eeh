import pymysql

def connection():
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="",
                           db="eeh",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    return c, conn
