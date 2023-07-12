from __future__ import annotations

import asyncio
import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL_ASYNC="sqlite+aiosqlite:///cte2.sqlite"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC,

    )

async_session = async_sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession, autoflush=True
    )

# engine = create_engine("sqlite+pysqlite:///cte2.sqlite")
from sqlalchemy import Table, Column, Integer, String
# session=Session(engine)
Base = declarative_base()


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
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List
async def func():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    except:
        print("Tables already created")
# Base.metadata.create_all(async_engine)
func()

db = async_session()
async def func1():
    try:
        db.execute(text("delete from folder"))
        await db.commit()
    except:
        print("Table already deleted")


import asyncio

async def get_db_async():
    try:
        db = async_session()
        yield db
    finally:
        await db.close()

async def fun2():
    async with get_db_async() as db:
        e1 = Folder(id=1, name="root", parent_id=None)
        e2 = Folder(id=2, name="folder1", parent_id=1)
        e3 = Folder(id=3, name="folder2", parent_id=1)
        e4 = Folder(id=4, name="folder3", parent_id=2)
        e5 = Folder(id=5, name="folder4", parent_id=2)
        e6 = Folder(id=6, name="folder5", parent_id=4)
        e7 = Folder(id=7, name="folder6", parent_id=6)

        db.add_all([e1, e2, e3, e4, e5, e6, e7])
        await db.commit()

async def main():
    await func1()
    await fun2()

asyncio.run(main())

# i want to create a recursive CTE to get all the sub folders in the database for a given folder id using async sqlalchemy

# lets create a async session

