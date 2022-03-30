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

#sessionを作成
Session=sessionmaker(bind=engine)
session=Session()

def createdata():
    #Employeeオブジェクト作成
    e1=Employee(EmpID="EMP001",Name="山田太郎",Email="taro@mail.com",Location="東京都",Dept="営業部")
    session.add(e1)
    e2=Employee(EmpID="EMP002",Name="羽田花子",Email="hane@mail.com",Location="北海道",Dept="人事部")
    session.add(e2)

    session.commit()


def alldata():
    #全部持ってくる
    emps=session.query(Employee).all()

    for emp in emps:
        print(f"{emp.EmpID},{emp.Name},{emp.Location},{emp.Dept}")
    

def onedata(id):
    emp=session.query(Employee).filter_by(EmpID=id).first()
    print(f"{emp.EmpID},{emp.Name},{emp.Location},{emp.Dept}")
