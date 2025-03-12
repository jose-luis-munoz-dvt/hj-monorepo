import oracledb
from extractors.logger import logger
from extractors.config import ORACLE_ORIGINS
from interfaces.db import BaseDbExtractor

class OracleExtractor(BaseDbExtractor):
    def connect(self):
        try:
            self.conn = oracledb.connect(
                user=ORACLE_ORIGINS[self.origin]['user'],
                password=ORACLE_ORIGINS[self.origin]['pwd'],
                host=ORACLE_ORIGINS[self.origin]['host'],
                port=ORACLE_ORIGINS[self.origin]['port'],
                service_name=ORACLE_ORIGINS[self.origin]['db_name']
            )
            self.schema = ORACLE_ORIGINS[self.origin].get('schema')
        except Exception as e:
            logger.error(f"Failed to connect to Oracle DB ({self.origin}): {e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def build_query(self, table_name: str) -> str:
        qualified_table = f"{self.schema}.{table_name}" if self.schema else table_name
        return f"SELECT * FROM {qualified_table}"
