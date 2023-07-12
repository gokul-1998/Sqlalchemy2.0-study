# import sqlalchemy
# print(sqlalchemy.__version__ )

from sqlalchemy import create_engine
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# here we use sqlite in memory database, echo=True means print the log
# engine = create_engine("sqlite+pysqlite:///./test.db", echo=True)
# here we use sqlite in file database, echo=True means print the log

# we dont want the log, so we set echo=False or just delete it
engine = create_engine("sqlite+pysqlite:///test.db")

from sqlalchemy import text

# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())

# with engine.connect() as conn:
#     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
#     )
#     conn.commit() 

# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
#     )

# the difference between conn.connect() and engine.begin() is that
# conn.connect() will not commit the transaction automatically,
# but engine.begin() will commit the transaction automatically


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

"""
another way to fetch
"""
# with engine.connect() as conn:
#     result = conn.execute(text("select x, y from some_table"))

#     for dict_row in result.mappings():
#         x = dict_row["x"]
#         y = dict_row["y"]
#         print(f"x: {x}  y: {y}")


# sending parameters
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

# with engine.connect() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
#     )
#     conn.commit()

# Executing with an ORM Session

from sqlalchemy.orm import Session

# stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
# with Session(engine) as session:
#     result = session.execute(stmt, {"y": 6})
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

# with Session(engine) as session:
#     result = session.execute(
#         text("UPDATE some_table SET y=:y WHERE x=:x"),
#         [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
#     )
#     session.commit()