from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

#https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
#  mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
engine = create_engine('mysql+pymysql://root:password@localhost:3304/example_db2', echo=True)

# テーブルとのマッピングを定義
Base = declarative_base()

# テーブルとのマッピングを定義
class Employee(Base):
    __tablename__ = 'Employee'

    EmpID = Column(String(10), primary_key=True)
    Name = Column(String(20))
    Email = Column(String(20))
    Location = Column(String(40))
    Dept = Column(String(40))

#実行
Base.metadata.create_all(engine)
