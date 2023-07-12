from sqlalchemy import Column, Integer, String, cast, create_engine, literal, select
from sqlalchemy.orm import Session,declarative_base
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
def get_parents(node_id):
    nodes_cte = (
        select(
            Node.id,
            Node.label,
            Node.parent_id,
            literal(1).label('depth'),
            cast(Node.id, String).label('path'),
            literal(False).label('is_circular')
        )
        .where(Node.id == node_id)
        .cte(name='nodes_cte', recursive=True)
    )

    nodes_alias = nodes_cte.alias()
    node_alias = Node.__table__.alias()

    nodes_cte = nodes_cte.union_all(
        select(
            node_alias.c.id,
            node_alias.c.label,
            node_alias.c.parent_id,
            (nodes_alias.c.depth + 1).label('depth'),
            (nodes_alias.c.path + '->' + cast(node_alias.c.id, String)).label('path'),
            (node_alias.c.id == nodes_alias.c.path).label('is_circular')
        )
        .where(node_alias.c.id == nodes_alias.c.parent_id)
        .where(~nodes_alias.c.is_circular)
    )

    stmt = select(nodes_cte).order_by(nodes_cte.c.depth.desc())

    result = session.execute(stmt).fetchall()
    return result

# Example usage
parents = get_parents(3)
for parent in parents:
    print(parent)
