from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import cast, Integer, Text, Column, ForeignKey, literal, null
from sqlalchemy.sql import column, label


from typing import List
from sqlalchemy.types import DATE, DATETIME
from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///cte2.sqlite")
from sqlalchemy import Table, Column, Integer, String,JSON
session=Session(engine)
class Base(DeclarativeBase):
    pass



# i am going to use sqlalchemy 2.0 syntax for this file
# i am going to make user of recursive CTEs
# lets create a folder table with parent_id as foreign key to folder_id
# lets create a table for folder with only 3 columns id, name, parent_id which is a foreign key to folder_id

class Folder(Base):
    __tablename__ = "folder"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(30))
    parent_id = Column(Integer, ForeignKey("folder.id"))
    creator_id = Column(Integer, ForeignKey("user_details.id"))
    parent = relationship("Folder",back_populates="folders" ,remote_side=[id])
    folders = relationship("Folder", back_populates="parent")
    privilege = relationship('FolderShare', back_populates='folder_share') 
    def __repr__(self) -> str:
        return f"Folder(id={self.id!r}, name={self.name!r}, parent_id={self.parent_id!r})"

class UserDetails(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(30))

    def __repr__(self) -> str:
        return f"UserDetails(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class FolderShare(Base):
    __tablename__  = "folder_share"
    # __table_args__ = {"schema" : schema_name}
    id = Column(Integer, primary_key = True, index= True)
    shared_from = Column(Integer, ForeignKey("user_details.id")) # foregin key of any user table
    folder_id = Column(Integer, ForeignKey("folder.id")) #foregin key of 'folder_id'
    is_edit = Column(Integer)
    is_comment = Column(Integer)
    is_delete = Column(Integer)
    is_share= Column(Integer)
    shared_to = Column(Integer, ForeignKey("user_details.id")) # foregin key of any user table
    # user_details = relationship('UserDetails', back_populates='privilege')
    folder_share = relationship('Folder', back_populates='privilege')
    user_details = relationship('UserDetails')
    # here we have two user_details relationship backpopul
    # backpopulates is used to tell the relationship between two tables 


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List


Base.metadata.create_all(engine)


    
# this will create an error because of the recursive relationship between manager and employees 

# Base.metadata.create_all(engine)

# another simple table for employee 

# lets start inserting some data into the employee table

# this query will remove all previous data from the employee table

session.execute(text("delete from folder"))
session.commit()

u1=UserDetails(id=1,name="user1")
u2=UserDetails(id=2,name="user2")
u3=UserDetails(id=3,name="user3")

session.add_all([u1,u2,u3])
session.commit()

e1=Folder(id=1,name="folder0",parent_id=1,creator_id=1)
e2=Folder(id=2,name="folder1",parent_id=1,creator_id=1)
e3=Folder(id=3,name="folder2",parent_id=1,creator_id=1)
e4=Folder(id=4,name="folder3",parent_id=2,creator_id=1)
e5=Folder(id=5,name="folder4",parent_id=2,creator_id=1)
e6=Folder(id=6,name="folder5",parent_id=4,creator_id=1)
e7=Folder(id=7,name="folder6",parent_id=6,creator_id=1)
e8=Folder(id=8,name="folder7",parent_id=6,creator_id=1)
e9=Folder(id=9,name="folder8",parent_id=6,creator_id=1)

session.add_all([e1,e2,e3,e4,e5,e6])
session.commit()