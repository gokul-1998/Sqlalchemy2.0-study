from sqlalchemy import Column, Integer, String, cast, create_engine, literal, select
from sqlalchemy.orm import Session,declarative_base
# # 
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    parent_id = Column(Integer)

engine = create_engine('sqlite+pysqlite:///get_parent.sqlite')
Base.metadata.create_all(engine)
session = Session(engine)

# Recursive CTE
nodes_cte = (
    select(
        Node.id,
        Node.parent_id,
        cast(Node.id, String).label('path'),
        literal(False).label('is_circular')
    )
    .where(Node.parent_id == Node.id)
    .cte(name='nodes_cte', recursive=True)
)

nodes_alias = nodes_cte.alias()
node_alias = Node.__table__.alias()

nodes_cte = nodes_cte.union_all(
    select(
        node_alias.c.id,
        node_alias.c.parent_id,
        (nodes_alias.c.path + ',' + cast(node_alias.c.id, String)).label('path'),
        (node_alias.c.id == nodes_alias.c.path).label('is_circular')
    )
    .where(node_alias.c.parent_id == nodes_alias.c.id)
    .where(~nodes_alias.c.is_circular)
)

stmt = select(nodes_cte.c.path).order_by(nodes_cte.c.id).filter(nodes_cte.c.id == 3)

result = session.execute(stmt).fetchone()

print(result[0])
