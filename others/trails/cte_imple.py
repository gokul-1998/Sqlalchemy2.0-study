from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import cast, Integer, Text, Column, ForeignKey, literal, null
from sqlalchemy.sql import column, label


from typing import List
    
from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///cte1.db")
from sqlalchemy import Table, Column, Integer, String
session=Session(engine)
class Base(DeclarativeBase):
    pass

# i am going to use sqlalchemy 2.0 syntax for this file
# i am going to make user of recursive CTEs
# lets create a employee table with manager_id as foreign key to employee_id
# lets create a table for employee with only 3 columns id, name, manager_id which is a foreign key to employee_id
# class Employee(Base):
#     __tablename__ = "employee"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     manager_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
#     manager: Mapped["Employee"] = relationship("Employee", back_populates="employees")
#     employees: Mapped[List["Employee"]] = relationship("Employee", back_populates="manager")
#     def __repr__(self) -> str:
#         return f"Employee(id={self.id!r}, name={self.name!r}, manager_id={self.manager_id!r})"
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(30))
    manager_id = Column(Integer, ForeignKey("employee.id"))
    manager = relationship("Employee",back_populates="employees" ,remote_side=[id])
    employees = relationship("Employee", back_populates="manager")

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, name={self.name!r}, manager_id={self.manager_id!r})"

    
    # this will create an error because of the recursive relationship between manager and employees 

# Base.metadata.create_all(engine)

# another simple table for employee 

# lets start inserting some data into the employee table

# this query will remove all previous data from the employee table
session.execute(text("delete from employee"))
session.commit()

e1=Employee(id=1, name="e1", manager_id=None)
e2=Employee(id=2, name="e2", manager_id=1)
e3=Employee(id=3, name="e3", manager_id=1)
e4=Employee(id=4, name="e4", manager_id=2)
e5=Employee(id=5, name="e5", manager_id=2)
e6=Employee(id=6, name="e6", manager_id=4)
e7=Employee(id=7, name="e7", manager_id=6)

session.add_all([e1,e2,e3,e4,e5,e6,e7])
session.commit()

# lets try to get the all the employees who are managed by e1 till the last level
# to do this we need to use recursive CTEs
# lets create a recursive CTEs
# lets create a CTEs for the base case
# it will be the employee who has no manager
# lets create a CTEs for the recursive case
# select_stmt=select(Employee).where(Employee.manager_id==None)
# lets create a CTEs for the recursive case
# it will be the employee who has manager


# the follwing query will give all the employees who are managed by e1 till the last level
# we are using sqlalchemy 2.0 syntax for this query


# lets create a CTEs for the recursive case

with_recursive_cte=select(Employee).where(Employee.manager_id==None).cte(recursive=True)
with_recursive_cte=with_recursive_cte.union_all(select(Employee).join(with_recursive_cte, Employee.manager_id==with_recursive_cte.c.id))

# print(session.execute(with_recursive_cte).scalars().all())
# session.execute(with_recursive_cte).scalars().all()
# print(session.execute(with_recursive_cte).scalars().all())
#
with_recursive_cte = select(Employee).where(Employee.manager_id == 2).cte(recursive=True)
with_recursive_cte = with_recursive_cte.union_all(select(Employee).join(with_recursive_cte, Employee.manager_id == with_recursive_cte.c.id))

query = select(with_recursive_cte)
result = session.execute(query)
employees = result.scalars().all()

print(employees)

# to print the result in a tree format we need to use a recursive function
# lets create a recursive function to print the result in a tree format


with_recursive_cte = select(Employee).where(Employee.manager_id == 2).cte(recursive=True)
with_recursive_cte = with_recursive_cte.union_all(select(Employee).join(with_recursive_cte, Employee.manager_id == with_recursive_cte.c.id))

query = select(with_recursive_cte)
result = session.execute(query)
employees = result.fetchall()  # Fetch all rows as tuples

for i in employees:
    print(i)
    print(i._asdict())
    

print(employees)
# def print_tree(employees: List[Employee], level: int = 0) -> None:
#     for employee in employees:
#         print(employee)
#         print("    " * level + f"{employee.name}")
#         print_tree(employee.employees, level + 1)
# print_tree(employees)

with_recursive_cte = select(Employee).where(Employee.manager_id == 2).cte(recursive=True)
with_recursive_cte = with_recursive_cte.union_all(select(Employee).join(with_recursive_cte, Employee.manager_id == with_recursive_cte.c.id))

query = select(with_recursive_cte)
result = session.execute(query)
employees = result.fetchall()  # Fetch all rows as tuples

for employee in employees:
    print(employee)
    # print(employee.employees)


from sqlalchemy import select, func
from sqlalchemy.orm import with_expression

with_recursive_cte = select(Employee).where(Employee.manager_id == 2).cte(recursive=True)
with_recursive_cte_alias = with_recursive_cte.alias()
# the above line is for sqlalchemy 1.4
# to use the above line in sqlalchemy 2.0 we need to use the following line
#

# this is for sqlalchemy 2.
recursive_select = select(Employee).join(with_recursive_cte_alias, Employee.manager_id == with_recursive_cte_alias.c.id)
with_recursive_cte = with_recursive_cte.union_all(recursive_select)

cte_query = select(with_recursive_cte).add_columns(
    with_recursive_cte_alias.c.id.label('manager_id'),
    func.array_agg(with_recursive_cte_alias.c.id).label('employee_ids')
).group_by(with_recursive_cte_alias.c.id)

# result = session.execute(cte_query)
# for row in result:
#     manager_id = row.manager_id
#     employee_ids = row.employee_ids
#     print(f"Manager ID: {manager_id}")
#     print(f"Employee IDs: {employee_ids}")
#     print("-----")
from sqlalchemy import select, func
from sqlalchemy.orm import with_expression

with_recursive_cte = select(Employee).where(Employee.manager_id == 2).cte(recursive=True)
with_recursive_cte_alias = with_recursive_cte.alias()
recursive_select = select(Employee).join(with_recursive_cte_alias, Employee.manager_id == with_recursive_cte_alias.c.id)
with_recursive_cte = with_recursive_cte.union_all(recursive_select)

cte_query = select(with_recursive_cte).add_columns(
    with_recursive_cte_alias.c.id.label('manager_id'),
    func.array_agg(with_recursive_cte_alias.c.id).label('employee_ids')
).group_by(with_recursive_cte_alias.c.id)

query = select(Employee).join(with_recursive_cte_alias, Employee.id == with_recursive_cte_alias.c.id)

result = session.execute(query)
for row in result:
    manager_id = row
    # employee_ids = row.employee_ids
    print(f"Manager ID: {manager_id}")
    # print(f"Employee IDs: {employee_ids}")
    print("-----")
