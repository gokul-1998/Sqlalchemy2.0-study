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
engine = create_engine("sqlite+pysqlite:///./cte2.sqlite")
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



with_recursive_cte = select(Folder).where(Folder.parent_id == 2).cte(recursive=True)
with_recursive_cte = with_recursive_cte.union_all(select(Folder).join(with_recursive_cte, Folder.parent_id == with_recursive_cte.c.id))

query = select(with_recursive_cte).order_by(with_recursive_cte.c.parent_id)
result = session.execute(query)
folders = result.fetchall()  # Fetch all rows as tuples

for folder in folders:
    print(folder)
folders.insert(0,(2,'folder1',1))
print(folders)
# to print the structure visibly
# lets create a function to print the structure of the folder
# def print_recursive_cte(folder: Folder, level: int = 0) -> None:
#     print(" " * level + f"{folder}")
#     for child in folder:
#         print_recursive_cte(child, level + 1)

# print_recursive_cte(folders[0])

def print_folder_tree(folders):
    folder_map = {}
    root_folders = []

    # Build a dictionary to map parent IDs to their respective folders
    for folder in folders:
        folder_id, name, parent_id = folder
        folder_map[folder_id] = {"name": name, "children": []}
        if parent_id is None:
            root_folders.append(folder_id)
        elif parent_id in folder_map:
            parent_folder = folder_map[parent_id]
            parent_folder["children"].append(folder_id)
        else:
            print(f"Skipping folder {folder_id} with unknown parent ID: {parent_id}")

    # Recursive function to print the tree structure
    def print_tree(folder_id, indentation=""):
        folder = folder_map[folder_id]
        print(f"{indentation}- {folder['name']} (ID: {folder_id}, Parent ID: {parent_id})")
        children = folder["children"]
        for child_id in children:
            print_tree(child_id, indentation + "  ")

    # Print the tree starting from root folders
    for root_id in root_folders:
        print_tree(root_id)
print_folder_tree(folders)

