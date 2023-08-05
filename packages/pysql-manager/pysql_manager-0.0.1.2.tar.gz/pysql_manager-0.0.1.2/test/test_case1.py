from pysql_manager.types import Column, StringType, IntegerType
from pysql_manager import PySql
from pysql_manager.functions import col


class User:
    name = Column(col_type=StringType(25))
    age = Column(col_type=IntegerType())
    id = Column(col_type=StringType(25))
    __table__ = "Users"


USER_NAME = "root"
PASSWORD = "password"
HOST = "localhost"
DB = "Test"

user = PySql(host=HOST, username=USER_NAME, password=PASSWORD, dbname=DB, meta_class=User)

print(user.fetch_all.select(["age", "name"]))
user.fetch_all.show()