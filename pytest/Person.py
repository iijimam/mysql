import mysql.connector

def createTable():
    conn = mysql.connector.connect(host='127.0.0.1', port=3304 ,user='root', password='password',database='logdb')
    cursor = conn.cursor()

    cursor.execute(
        'CREATE TABLE Person(Name VARCHAR(50),Email VARCHAR(50));'
    )

    cursor.close()
    conn.close()

def run(sql):
    conn = mysql.connector.connect(host='127.0.0.1', port=3304 ,user='root', password='password',database='logdb')
    cursor = conn.cursor()

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def search(sql):
    conn = mysql.connector.connect(host='127.0.0.1', port=3304 ,user='root', password='password',database='logdb')
    cursor = conn.cursor()

    cursor.execute(sql)

    for row in cursor:
        print(row)

    cursor.close()
    conn.close()
