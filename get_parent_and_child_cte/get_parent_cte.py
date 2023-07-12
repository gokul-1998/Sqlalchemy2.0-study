from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import cast, Integer, Text, Column, ForeignKey, literal, null
from sqlalchemy.sql import column, label


from typing import List
    
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
from sqlalchemy import Table, Column, Integer, String
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
    parent = relationship("Folder",back_populates="folders" ,remote_side=[id])
    folders = relationship("Folder", back_populates="parent")
    def __repr__(self) -> str:
        return f"Folder(id={self.id!r}, name={self.name!r}, parent_id={self.parent_id!r})"

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

e1=Folder(id=1,name="root",parent_id=None)
e2=Folder(id=2,name="folder1",parent_id=1)
e3=Folder(id=3,name="folder2",parent_id=1)
e4=Folder(id=4,name="folder3",parent_id=2)
e5=Folder(id=5,name="folder4",parent_id=2)
e6=Folder(id=6,name="folder5",parent_id=4)
e7=Folder(id=7,name="folder6",parent_id=6)


session.add_all([e1,e2,e3,e4,e5,e6,e7])
session.commit()

# lets create a recursive CTE to get all the folders in the folder table for a given folder id 

with_recursive_cte = select(Folder).where(Folder.parent_id == 2).cte(recursive=True)
with_recursive_cte = with_recursive_cte.union_all(select(Folder).join(with_recursive_cte, Folder.parent_id == with_recursive_cte.c.id))

query = select(with_recursive_cte)
result = session.execute(query)
folders = result.fetchall()  # Fetch all rows as tuples

# for folder in folders:
#     print(folder)

# lets create a recursive CTE to get all the parent folders in the folder table for a given folder id
#
with_recursive_cte = select(Folder).where(Folder.id == 7).cte(recursive=True) # this is the anchor member
with_recursive_cte = with_recursive_cte.union_all(select(Folder).join(with_recursive_cte, Folder.id == with_recursive_cte.c.parent_id)) # this is the recursive member
# termination_condition = select(Folder).where(Folder.parent_id==Folder.id)  # Assuming parent_id is NULL for the root folder
# 
# Create the recursive CTE
# recursive_cte = select(Folder).where(Folder.id == 7).cte(recursive=True)
# recursive_cte = recursive_cte.union_all(select(Folder).join(recursive_cte, Folder.id == recursive_cte.c.parent_id))

# Combine the recursive CTE and termination condition
# subquery = select(recursive_cte).union_all(termination_condition).alias()

# Construct the final query
# query = select(subquery.c)

# query = recursive_cte.union_all(termination_condition)

query = select(with_recursive_cte)
result = session.execute(query)
folders = result.fetchall()  # Fetch all rows as tuples

for folder in folders:
    print(folder)