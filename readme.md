# PythonとMySQLを試してみる（普通にアクセス＋SQLAlchemy）

## 試した環境
Python3.8 (Ubuntu)　と　MySQL(mysql:latest)

## 1) MySQLのコンテナを作る
参考ページ：https://qiita.com/ponsuke0531/items/cbd5f3fe9461792c2279

1) コンテナ作成＆開始
    ```
    docker-compose up -d --build
    ```
    MySQLのデフォルトポートは3306だけどコンテナは3304を使うので注意

    - memo
        [docker-entrypoint-initdb.d](logdb/init/docker-entrypoint-initdb.d)に作成するテーブルとか書いておくとビルド時に作ってくれるらしい
        
        その他、アクセスユーザは[docker-compose.yml](docker-compose.yml)参照


2) コンテナにログインしてMySQLにアクセスする
    
    ```
    docker exec -it logdb bash
    ```

    MySQLにログイン（コンテナ開始時に作ってるデータベース logdb　にユーザ log でアクセス）
    ```
    mysql -u log -D logdb -p
    ```

    自由にテーブル作ったりする場合はrootが便利
    ```
    mysql -u root -D logdb -p
    ```

    **SQL実行時末尾に ; 忘れずに！**

    これでMySQL側準備OK

## 2) Pythonからアクセス（普通にアクセス）
Ubuntuの3.8のPythonを利用

1) 仮想環境の準備

    参考：https://qiita.com/komoto2020/items/9837455f8549e06016d8

    仮想環境を使いたかったので以下ページを参考に仮想環境を使うための準備

    ```
    sudo apt-get update
    sudo apt-get install python3.8-venv
    ```

    この後、好きなディレクトリを作って（仮想環境にしたい場所）以下実行
    ```
    python3 -m venv .venv
    ```

    仮想環境にログイン
    ```
    source .venv/bin/activate
    (.venv) isjedu@ubuntu:~/containertest/mysql/pytest$
    ```
    後はこの状態で pip3 install ** したらOK

    MySQLからアクセスするためにパッケージインストール
    ```
    pip install mysql-connector-python
    ```

2) スクリプトの記述

    参考：https://xminatolog.com/post/2145

    mysql.connectorを使ったサンプル：[Person.py](pytest/Person.py)


## 3) Pythonからアクセス（SQLAlchemy使用）

参考：https://xminatolog.com/post/2145　真ん中以降

1) SQLAlchemyに必要なパッケージのインポート

    ```
    pip install SQLAlchemy
    pip install PyMySQL
    ```
    参考ページにあるように後は、example_db2データベースをrootで作成してスクリプトからアクセス
    (以下、MySQLのコンテナ内で実行)
    ```
    mysql -u root -D example_db2 -p
    create database example_db2;
    ```


2) スクリプト例

    echo=True でアクセスしてるのでいっぱいログ出る
    ```
    engine = create_engine('mysql+pymysql://root:password@localhost:3304/example_db2', echo=True)
    ```

    PythonのEmployeeクラスからテーブルにマッピングする例 [alchemytest1.py](pytest/alchemytest1.py)

    ```
    (.venv) isjedu@ubuntu:~/containertest/mysql/pytest$ python3 alchemytest1.py
    2022-03-30 17:11:21,195 INFO sqlalchemy.engine.Engine SELECT DATABASE()
    2022-03-30 17:11:21,196 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:11:21,199 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
    2022-03-30 17:11:21,199 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:11:21,201 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
    2022-03-30 17:11:21,201 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:11:21,204 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-03-30 17:11:21,206 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
    2022-03-30 17:11:21,206 INFO sqlalchemy.engine.Engine [generated in 0.00034s] {'table_schema': 'example_db2', 'table_name': 'Employee'}
    2022-03-30 17:11:21,211 INFO sqlalchemy.engine.Engine
    CREATE TABLE `Employee` (
            `EmpID` INTEGER NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(20),
            `Email` VARCHAR(20),
            `Location` VARCHAR(40),
            `Dept` VARCHAR(40),
            PRIMARY KEY (`EmpID`)
    )

    2022-03-30 17:11:21,211 INFO sqlalchemy.engine.Engine [no key 0.00039s] {}
    2022-03-30 17:11:21,241 INFO sqlalchemy.engine.Engine COMMIT
    ```

    以下2つの例 [alchemytest2.py](pytest/alchemytest2.py)

    - PythonのEmployeeクラスのインスタンスを作ってSQLalchemyのセッションに追加してコミット
    - PythonのEmployeeクラスの検索

    ```
    (.venv) isjedu@ubuntu:~/containertest/mysql/pytest$ python3
    Python 3.8.10 (default, Mar 15 2022, 12:22:08)
    [GCC 9.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys
    >>> sys.path +=['/home/isjedu/containertest/mysql/pytest']
    >>> import alchemytest2
    >>> alchemytest2.createdata()
    2022-03-30 17:23:30,680 INFO sqlalchemy.engine.Engine SELECT DATABASE()
    2022-03-30 17:23:30,680 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:23:30,681 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
    2022-03-30 17:23:30,682 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:23:30,682 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
    2022-03-30 17:23:30,683 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-03-30 17:23:30,685 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-03-30 17:23:30,687 INFO sqlalchemy.engine.Engine INSERT INTO `Employee` (`EmpID`, `Name`, `Email`, `Location`, `Dept`) VALUES (%(EmpID)s, %(Name)s, %(Email)s, %(Location)s, %(Dept)s)
    2022-03-30 17:23:30,689 INFO sqlalchemy.engine.Engine [generated in 0.00180s] ({'EmpID': 'EMP001', 'Name': '山田太郎', 'Email': 'taro@mail.com', 'Location': '東京都', 'Dept': '営業部'}, {'EmpID': 'EMP002', 'Name': '羽田花子', 'Email': 'hane@mail.com', 'Location': ' 北海道', 'Dept': '人事部'})
    2022-03-30 17:23:30,692 INFO sqlalchemy.engine.Engine COMMIT
    >>> alchemytest2.alldata()
    2022-03-30 17:23:49,348 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-03-30 17:23:49,350 INFO sqlalchemy.engine.Engine SELECT `Employee`.`EmpID` AS `Employee_EmpID`, `Employee`.`Name` AS `Employee_Name`, `Employee`.`Email` AS `Employee_Email`, `Employee`.`Location` AS `Employee_Location`, `Employee`.`Dept` AS `Employee_Dept`
    FROM `Employee`
    2022-03-30 17:23:49,351 INFO sqlalchemy.engine.Engine [generated in 0.00034s] {}
    EMP001,山田太郎,東京都,営業部
    EMP002,羽田花子,北海道,人事部
    >>> alchemytest2.onedata("EMP001")
    2022-03-30 17:24:04,312 INFO sqlalchemy.engine.Engine SELECT `Employee`.`EmpID` AS `Employee_EmpID`, `Employee`.`Name` AS `Employee_Name`, `Employee`.`Email` AS `Employee_Email`, `Employee`.`Location` AS `Employee_Location`, `Employee`.`Dept` AS `Employee_Dept`
    FROM `Employee`
    WHERE `Employee`.`EmpID` = %(EmpID_1)s
    LIMIT %(param_1)s
    2022-03-30 17:24:04,312 INFO sqlalchemy.engine.Engine [generated in 0.00040s] {'EmpID_1': 'EMP001', 'param_1': 1}
    EMP001,山田太郎,東京都,営業部
    >>>
    ```

## 4) 1対多

参考：https://qiita.com/ktamido/items/ebdbe5a85dbc3e6004ae

参考：https://bokepro.blog.fc2.com/blog-entry-18.html

- 1) 実行前準備

    Pythonシェルに移動して、onetomany.pyのパスを sys.pathに追加する
    ```
    import sys
    sys.path +=['/home/isjedu/containertest/mysql/pytest']
    ```

- 2) 1対多のテーブル作成（1:Receipt , 多:Item）

    [onetomany.py](pytest/onetomany.py)のcreatetable()を実行

    ```
    import onetomany
    onetomany.createtable()
    ```
    この後、MySQLで show tables;　するとReceiptとItemテーブルができている事を確認できる
    ```
    mysql> show tables;
    +-----------------------+
    | Tables_in_example_db2 |
    +-----------------------+
    | Employee              |
    | Item                  |
    | Receipt               |
    +-----------------------+
    3 rows in set (0.00 sec)
    ```

3) データの登録

    [onetomany.py](pytest/onetomany.py)のcreatedata()を実行

    ```
    onetomany.createtable()
    ```
    1から多のインスタンスの追加は以下の感じ
    ```
    it1=Item(ItemId=1,ItemName="豆腐",Prise=150)
    it2=Item(ItemId=2,ItemName="卵",Prise=198)
    receipt=Receipt(ShopId="S0001",ShopName="オーケー国分寺店")
    receipt.Items.append(it1)
    receipt.Items.append(it2)
    session.add(receipt)
    ```

    sessionに作成した1側インスタンスを登録したら多側も一緒に更新される。ここはIRISと一緒

4) データの参照

    [onetomany.py](pytest/onetomany.py)のall()かfind(id)を実行 

    SQLAlchemyのfilterを使って欲しい情報を取得する。（filter_by()を使ってSELECTのようなことができるので、IRISよりもオブジェクトを取ってきやすいイメージがある。取得した結果から、1対多の関連がそのまま使えるので便利）

    - 1側を取得した場合、多側はリストで取れるので関連を辿れる
        ```
        result=session.query(Receipt).all()
        for r in result:
            print(f"*** 店舗情報 *** {r.ShopId} - {r.ShopName}")
            # ReceiptのItems（多）はリストで取れる
            for i in r.Items:
                print(f" ** {i.ItemId} - {i.ItemName} - {i.Prise}")
        ```

    - 多側を取得した場合、1側を辿れる
        ```
        result=session.query(Item).filter_by(ItemId=id).first()
        print(f"** 詳細項目 ** {result.ItemId} - {result.ItemName} - {result.Prise}")
        print(f"** 店舗情報 ** {result.Receipt.ShopName}")
        ```
