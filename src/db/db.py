import pymssql
from src.db.config import DB_CONFIG


class MySQLDatabase:
    config = DB_CONFIG
    def get_connection(self) -> pymssql.Connection:
        return pymssql.connect(**self.config)

db = MySQLDatabase()