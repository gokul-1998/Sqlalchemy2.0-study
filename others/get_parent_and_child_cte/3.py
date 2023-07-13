from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func, select

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
Base.metadata.create_all(engine)

# Insert test data
session.execute(text("DELETE FROM node"))
session.commit()
session.execute(text("INSERT INTO node (label, parent_id) VALUES ('n1',1),('n2',1),('n3',2),('n4',3);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage1',5),('garbage2',6), ('garbage3',7);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage4',6);"))
session.commit()

node_id = 4  # Specify the node id for which to find the parents

# Define the recursive CTE query using SQLAlchemy
nodes_cte = (
    session.query(
        Node.id,
        Node.label,
        Node.parent_id,
        func.cast(1, Integer).label('depth'),
        func.cast(Node.id, String).label('path')
    )
    .filter(Node.id == node_id)  # Specify the starting node id
    .cte(recursive=True)
)

child_alias = session.query(Node.id.label('child_id'), Node.parent_id.label('parent_id')).subquery()

nodes_cte = (
    nodes_cte.union_all(
        session.query(
            Node.id,
            Node.label,
            Node.parent_id,
            (nodes_cte.c.depth + 1).label('depth'),
            (nodes_cte.c.path + '->' + func.cast(Node.id, String)).label('path')
        )
        .join(child_alias, Node.id == child_alias.c.parent_id)
        .join(nodes_cte, child_alias.c.child_id == nodes_cte.c.id)
        .filter(Node.id != node_id)  # Terminate recursion if the root node is reached
    )
)

# Retrieve all the parents using the CTE
parents = (
    session.query(Node)
    .join(nodes_cte, Node.id == nodes_cte.c.id)
    .order_by(nodes_cte.c.depth.desc())
    .all()
)

# Output the parents
for parent in parents:
    print(parent.id, parent.label, parent.parent_id)
