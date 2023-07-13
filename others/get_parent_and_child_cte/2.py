from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
from sqlalchemy.orm import sessionmaker, declarative_base
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

# Insert test data
session.execute(text("delete from node"))
session.commit()
session.execute(text("INSERT INTO node (label, parent_id) VALUES ('n1',1),('n2',1),('n3',2),('n4',3);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage1',5),('garbage2',6), ('garbage3',7);"))
session.execute(text("INSERT INTO node (label,parent_id) VALUES ('garbage4',6);"))
session.commit()
print("data inserted")
# Function to retrieve all parents of a node in a tree structure
def get_parents(node_id):
    parents = []
    current_node = session.query(Node).filter(Node.id == node_id).first()

    while current_node.parent_id!=current_node.id:
        # print(current_node.id, current_node.label, current_node.parent_id)
        parents.insert(0, current_node)
        parent_id = current_node.parent_id
        current_node = session.query(Node).filter(Node.id == parent_id).first()

    return parents

# Example usage: Get parents of node with id 4
node_id = 4
print
parents = get_parents(node_id)

# Output the parents
for parent in parents:
    print(parent.id, parent.label, parent.parent_id)
