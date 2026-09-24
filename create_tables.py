from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from models import Base

for table in Base.metadata.sorted_tables:
    print(str(CreateTable(table).compile(dialect = postgresql.dialect())))
    
    print(":\n")