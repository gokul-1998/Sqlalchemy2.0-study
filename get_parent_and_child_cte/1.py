from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
from sqlalchemy.orm import sessionmaker,declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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

session.execute(text("delete from node"))
session.commit()
# Insert test data
session.execute(text("INSERT INTO node (label, parent_id) VALUES ('n1',1),('n2',1),('n3',2),('n4',3);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage1',5),('garbage2',6), ('garbage3',7);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage4',6);"))
session.commit()

# Define the recursive CTE query using SQLAlchemy
nodes_cte = (
    session.query(
        Node.id,
        Node.label,
        Node.parent_id,
        func.cast(1, Integer).label('depth'),
        func.cast(Node.id, String).label('path'),
        func.cast(0, Boolean).label('is_circular')
    )
    .filter(Node.parent_id == Node.id)
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
            (nodes_cte.c.path + '->' + func.cast(Node.id, String)).label('path'),
            (nodes_cte.c.path + '->' + func.cast(Node.id, String)).like('%->' + func.cast(Node.id, String) + '->%').label('is_circular')
        )
        .join(child_alias, Node.id == child_alias.c.parent_id)
        .join(nodes_cte, child_alias.c.child_id == nodes_cte.c.id)
        .filter(~nodes_cte.c.is_circular)
    )
)

# Execute the query and retrieve the results
result = session.query(nodes_cte).order_by(nodes_cte.c.id.asc()).all()
print("result:",result)

# Output the results
for row in result:
    print(row.id, row.label, row.parent_id, row.depth, row.path, row.is_circular)
