from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import with_expression

# Define the SQLAlchemy ORM model
Base = declarative_base()

class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    parent_id = Column(Integer)

# Create the SQLAlchemy engine and session
engine = create_engine('sqlite+pysqlite:///get_parent.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# Define the recursive CTE query using SQLAlchemy
nodes_cte = (
    session.query(
        Node.id,
        Node.label,
        Node.parent_id,
        func.cast(1, Integer).label('depth'),
        func.cast(Node.id, String).label('path'),
        func.false().label('is_circular')
    )
    .filter(Node.parent_id == Node.id)
    .cte(recursive=True)
)

nodes_cte_alias = with_expression(nodes_cte.alias())

nodes_cte = (
    nodes_cte.union_all(
        session.query(
            Node.id,
            Node.label,
            Node.parent_id,
            (nodes_cte_alias.c.depth + 1).label('depth'),
            (nodes_cte_alias.c.path + '->' + func.cast(Node.id, String)).label('path'),
            (Node.id == func.any(func.string_to_array(nodes_cte_alias.c.path, '->'))).label('is_circular')
        )
        .join(nodes_cte_alias, Node.parent_id == nodes_cte_alias.c.id)
        .filter(~nodes_cte_alias.c.is_circular)
    )
)

# Execute the query and retrieve the results
result = session.query(nodes_cte).order_by(nodes_cte.c.id.asc()).all()

# Output the results
for row in result:
    print(row.id, row.label, row.parent_id, row.depth, row.path, row.is_circular)
