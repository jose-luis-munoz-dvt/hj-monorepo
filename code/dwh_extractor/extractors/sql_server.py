import pyodbc
import sqlserverport
import struct
from extractors.logger import logger
from extractors.config import SQL_SERVER_ORIGINS
from interfaces.db import BaseDbExtractor

class SQLServerExtractor(BaseDbExtractor):
    def connect(self):
        try:
            port = 1433
            instance_name = SQL_SERVER_ORIGINS[self.origin].get('instance_name')
            if instance_name:
                port = sqlserverport.lookup(
                    SQL_SERVER_ORIGINS[self.origin]['host'],
                    instance_name
                )

            self.conn = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={SQL_SERVER_ORIGINS[self.origin]['host']},{port};"
                f"Database={SQL_SERVER_ORIGINS[self.origin]['db_name']};"
                f"uid={SQL_SERVER_ORIGINS[self.origin]['user']};"
                f"pwd={SQL_SERVER_ORIGINS[self.origin]['pwd']};"
                "TrustServerCertificate=yes;"
            )
            self.conn.add_output_converter(-155, self.handle_datetimeoffset)
            self.schema = SQL_SERVER_ORIGINS[self.origin].get('schema')
        except Exception as e:
            logger.error(f"Failed to connect to SQL Server ({self.origin}): {e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def build_query(self, table_name: str) -> str:
        qualified_table = f"{self.schema}.{table_name}" if self.schema else table_name
        return f"SELECT * FROM {qualified_table}"

    @staticmethod
    def handle_datetimeoffset(dto_value: bytes) -> str:
        tup = struct.unpack("<6hI2h", dto_value)
        tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)
