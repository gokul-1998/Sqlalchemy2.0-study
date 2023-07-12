from __future__ import annotations

import asyncio
import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.asyncio import async_session, create_async_engine
from sqlalchemy.orm import relationship, Session, declarative_base
from sqlalchemy import select

SQLALCHEMY_DATABASE_URL_ASYNC = "sqlite+aiosqlite:///cte2.sqlite"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)

async_session = async_session(async_engine)

Base = declarative_base()

class Folder(Base):
    __tablename__ = "folder"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    parent_id = Column(Integer, ForeignKey("folder.id"))
    parent = relationship("Folder", back_populates="folders", remote_side=[id])
    folders = relationship("Folder", back_populates="parent")

    def __repr__(self) -> str:
        return f"Folder(id={self.id!r}, name={self.name!r}, parent_id={self.parent_id!r})"

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

async def delete_table_data():
    async with async_session() as db:
        await db.execute(text("DELETE FROM folder"))
        await db.commit()

async def populate_folders():
    async with async_session() as db:
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
    await delete_table_data()
    await create_tables()
    await populate_folders()

asyncio.run(main())
