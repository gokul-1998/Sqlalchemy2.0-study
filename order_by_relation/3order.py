import time
from datetime import datetime
from sqlalchemy import (Column, ForeignKey, Integer,  create_engine,
                         select, text)
from sqlalchemy.orm import (DeclarativeBase,  Session,
                            joinedload, relationship,
)
engine = create_engine("sqlite+pysqlite:///cte2.sqlite")
from sqlalchemy import Column, Integer, String
session=Session(engine)
class Base(DeclarativeBase):
    pass
class Folder(Base):
    __tablename__ = "folder"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(30))
    parent_id = Column(Integer, ForeignKey("folder.id"))
    is_deleted = Column(Integer,default=0)
    created_time=Column(String(30))
    parent = relationship("Folder",back_populates="folders" ,remote_side=[id])
    folders = relationship("Folder", back_populates="parent")
    privilege=relationship("Folder_share",back_populates="folder")
    def __repr__(self) -> str:
        return f"Folder(id={self.id!r})"

class Folder_share(Base):
    __tablename__ = "folder_share"
    id = Column(Integer, primary_key=True,autoincrement=True)
    created_time=Column(String(30)) 
    folder_id = Column(Integer, ForeignKey("folder.id"))
    is_delete=Column(Integer,default=0)
    is_share=Column(Integer,default=0)
    is_comment=Column(Integer,default=0)
    folder = relationship("Folder", back_populates="privilege")
    def __repr__(self) -> str:
        return f"Folder_share(id={self.id!r}, created_time={self.created_time!r}, folder_id={self.folder_id!r})"

Base.metadata.create_all(engine)

session.execute(text("delete from folder"))
session.execute(text("delete from folder_share"))
session.commit()

fs2=Folder_share(id=2,created_time=datetime.now(),folder_id=2,is_delete=0,is_share=0,is_comment=0)
e3=Folder(id=3,name="folder2",parent_id=1,is_deleted=0,created_time=datetime.now())
time.sleep(2)
e1=Folder(id=1,name="root",parent_id=1,is_deleted=0)

fs1=Folder_share(id=1,created_time=datetime.now(),folder_id=1,is_delete=0,is_share=0,is_comment=0)
e2=Folder(id=2,name="folder1",parent_id=1,is_deleted=0,created_time=datetime.now())
time.sleep(2)

fs3=Folder_share(id=3,created_time=datetime.now(),folder_id=3,is_delete=0,is_share=0,is_comment=0)
e4=Folder(id=4,name="folder3",parent_id=2,is_deleted=1,created_time=datetime.now())
time.sleep(2)
e6=Folder(id=6,name="folder5",parent_id=5,is_deleted=1,created_time=datetime.now())
fs6=Folder_share(id=6,created_time=datetime.now(),folder_id=6,is_delete=0,is_share=0,is_comment=0)
time.sleep(2)
fs4=Folder_share(id=4,created_time=datetime.now(),folder_id=4,is_delete=0,is_share=0,is_comment=0)
e5=Folder(id=5,name="folder4",parent_id=4,is_deleted=1,created_time=datetime.now())
time.sleep(2)
fs5=Folder_share(id=5,created_time=datetime.now(),folder_id=5,is_delete=0,is_share=0,is_comment=0)
e8=Folder(id=8,name="folder7",parent_id=7,is_deleted=0,created_time=datetime.now())
fs8=Folder_share(id=8,created_time=datetime.now(),folder_id=8,is_delete=0,is_share=0,is_comment=0)
time.sleep(2)

e7=Folder(id=7,name="folder6",parent_id=1,is_deleted=0,created_time=datetime.now())
fs7=Folder_share(id=7,created_time=datetime.now(),folder_id=7,is_delete=0,is_share=0,is_comment=0)
time.sleep(2)

e9=Folder(id=9,name="folder8",parent_id=8,is_deleted=1,created_time=datetime.now())
fs9=Folder_share(id=9,created_time=datetime.now(),folder_id=9,is_delete=0,is_share=0,is_comment=0)

session.add_all([e1,e2,e3,e4,e5,e6,e7,e8,e9,fs1,fs2,fs3,fs4,fs5,fs6,fs7,fs8,fs9])
session.commit()

query=select(Folder).options(
    joinedload(Folder.privilege).load_only(Folder_share.created_time,Folder_share.is_delete,Folder_share.is_share,Folder_share.is_comment)
)
query=query.join(Folder.privilege)
query=query.order_by(Folder_share.created_time.desc())
result=session.execute(query).scalars().unique().all()
for item in result:
    print(item,item.privilege[0])