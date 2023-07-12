
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
class Base(DeclarativeBase):
    pass
from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///test11.db")

from sqlalchemy import text
from sqlalchemy import Table, Column, Integer, String
# Base = declarative_base()
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    # name: Mapped[str] = mapped_column(String(30))
    name = Column(VARCHAR(45))
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
    
from sqlalchemy import select
stmt = select(User).where(User.name == "spongebob")
# print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        # print(row)
        pass

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        # print(row)
        pass


# print(select(User["name", "fullname"]))
# # the above is equivalent to:
# print(select(User.name,fullname))
# # but it will raise an error:
from sqlalchemy import func, cast
stmt = select(
    ("Username: " + User.name).label("username"),
).order_by(User.name)
# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(row)
#         print(f"{row.username}")

from sqlalchemy import text
# stmt = select(text("'some phrase'"), User.name).order_by(User.name)
# with engine.connect() as conn:
#     print(conn.execute(stmt).all())

from sqlalchemy import literal_column
stmt = select(literal_column("'some phrase'").label("p"), User.name).order_by(
    User.name
)
# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(f"{row.p}, {row.name}")

stmt=select(Address.email_address).where(User.name == "sandy").where(Address.user_id == User.id)
# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(row)

from sqlalchemy.orm import aliased
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)
stmt=select(User).join_from(User, address_alias_1).where(address_alias_1.email_address == "sandy@squirrelpower.org").join_from(User, address_alias_2).where(address_alias_2.email_address == "sandy@aol.com")

stmt=select(User)

# with engine.connect() as conn:
#     print("assa")
#     for row in conn.execute(stmt):
#         print(row._asdict())

from sqlalchemy import select

username=User.name.label("username")
stmt = select(User, username)
# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(row._asdict())

from sqlalchemy import select
from sqlalchemy.orm import defer
# username=User.name.label("username")
# stmt = select(User,username).options(defer(User.name))


subq = select(func.count(Address.id).label("count"), Address.user_id).group_by(Address.user_id).subquery()
# print(subq)
stmt=select(subq.c.count)

subq = (
    select(func.count(Address.id).label("count"), Address.user_id)
    .group_by(Address.user_id)
    .cte()
)

stmt = select(User.name, User.fullname, subq.c.count).join_from(
    User, subq
)

# print(stmt)

subq = (
    select(func.count(Address.id).label("count"), Address.user_id)
    .group_by(Address.user_id)
    .cte()
)

stmt = select(User.name, User.fullname, subq.c.count).join_from(
    User, subq
)

# print(stmt)




# with engine.connect() as conn:
#     # print("assa") 
#     for row in conn.execute(stmt):
#         print(row._asdict())


subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
address_subq = aliased(Address, subq)
stmt = (
    select(User, address_subq)
    .join_from(User, address_subq)
    .order_by(User.id, address_subq.id)
)
# with Session(engine) as session:
#     for user in session.execute(stmt):
#         print(user)

cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
#the ~ operator is equivalent to the not_() function
address_cte = aliased(Address, cte_obj)
# here 
stmt = (
    select(User, address_cte)
    .join_from(User, address_cte)
    .order_by(User.id, address_cte.id)
)
with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")