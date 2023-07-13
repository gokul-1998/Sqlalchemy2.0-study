from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///test11.db")

from sqlalchemy import text
from sqlalchemy import Table, Column, Integer, String

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
Base.metadata.create_all(engine)


from sqlalchemy import insert
# stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")
# compiled = stmt.compile()
# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()
# print(insert(User))

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(User),
#         [
#             {"name": "Gokul", "fullname": "Gokul Cheeks"},
#             {"name": "raja", "fullname": "raja Star"},
#         ],
#     )
#     conn.commit()

from sqlalchemy import select, bindparam
# scalar_subq = (
#     select(User.id)
#     .where(User.name == bindparam("username"))
#     .scalar_subquery()
# )

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(Address).values(user_id=scalar_subq),
#         [
#             {
#                 "username": "spongebob",
#                 "email_address": "spongebob@sqlalchemy.org",
#             },
#             {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
#             {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
#         ],
#     )
#     conn.commit()

# print(insert(User).values().compile(engine))
# insert_stmt = insert(Address).returning(
#     Address.id, Address.email_address
# )
# print(insert_stmt)

# from sqlalchemy import insert
# stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")
# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(User),
#         [
#             {"name": "sandy", "fullname": "Sandy Cheeks"},
#             {"name": "patrick", "fullname": "Patrick Star"},
#         ],
#     )
#     conn.commit()

from sqlalchemy import select, bindparam
# scalar_subq = (
#     select(User.id)
#     .where(User.name == bindparam("username"))
#     .scalar_subquery()
# )

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(Address).values(user_id=scalar_subq),
#         [
#             {
#                 "username": "spongebob",
#                 "email_address": "spongebob@sqlalchemy.org",
#             },
#             {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
#             {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
#         ],
#     )
#     conn.commit()

select_stmt = select(User.id, User.name + "@aol.com")
insert_stmt = insert(Address).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt)
with engine.connect() as conn:
    result = conn.execute(insert_stmt)
    conn.commit()