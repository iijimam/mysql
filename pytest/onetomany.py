from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,ForeignKey

# テーブルとのマッピングを定義
Base = declarative_base()
#  mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
engine = create_engine('mysql+pymysql://root:password@localhost:3304/example_db2', echo=True)

class Receipt(Base):
    __tablename__ = "Receipt"
    ShopId =Column(String(10), primary_key=True,index=True)
    ShopName = Column(String(30), nullable=False, index=True, unique=True)
    # リレーション: ItemクラスのRecepitプロパティに関連付ける
    Items = relationship("Item", back_populates="Receipt")

class Item(Base):
    __tablename__ = 'Item'
    ItemId = Column(Integer,primary_key=True)
    ItemName = Column(String(30), nullable=False, index=True, unique=True)
    Prise = Column(Integer)
    # 外部キー
    ShopId = Column(String(10), ForeignKey('Receipt.ShopId'),index=True) # ForeignKeyには "テーブル名.カラム名" を指定
    # ReceiptクラスのItemsプロパティに関連付ける
    Receipt = relationship("Receipt", back_populates="Items")



def createtable():
    #実行
    Base.metadata.create_all(engine)

def droptable():
    #実行
    Base.metadata.drop_all(engine)

def createdata():
    #sessionを作成
    Session=sessionmaker(bind=engine)

    with Session() as session:
        session.begin()
        try:
            it1=Item(ItemId=1,ItemName="豆腐",Prise=150)
            it2=Item(ItemId=2,ItemName="卵",Prise=198)
            receipt=Receipt(ShopId="S0001",ShopName="オーケー国分寺店")
            receipt.Items.append(it1)
            receipt.Items.append(it2)
            session.add(receipt)
        except:
            session.rollback()
            raise
        else:
            session.commit()

def all():
    #sessionを作成
    Session=sessionmaker(bind=engine)
    session=Session()
    result=session.query(Receipt).all()
    for r in result:
        print(f"*** 店舗情報 *** {r.ShopId} - {r.ShopName}")
        # ReceiptのItems（多）はリストで取れる
        for i in r.Items:
            print(f" ** {i.ItemId} - {i.ItemName} - {i.Prise}")

#ItemからReceiptを取得
def find(id):
    #sessionを作成
    Session=sessionmaker(bind=engine)
    session=Session()
    result=session.query(Item).filter_by(ItemId=id).first()
    print(f"** 詳細項目 ** {result.ItemId} - {result.ItemName} - {result.Prise}")
    print(f"** 店舗情報 ** {result.Receipt.ShopName}")
  
