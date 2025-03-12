from hdbcli import dbapi
from extractors.logger import logger
from extractors.config import SAP_HOST, SAP_PORT, SAP_USER, SAP_PWD, SAP_DB_NAME, LOAD_MODE, INCREMENTAL_TIMESTAMP_SOURCE, INCREMENTAL_FIELD
from interfaces.db import BaseDbExtractor


class SapExtractor(BaseDbExtractor):
    def connect(self):
        try:
            self.conn = dbapi.connect(
                address=SAP_HOST,
                port=SAP_PORT,
                user=SAP_USER,
                password=SAP_PWD,
                databaseName=SAP_DB_NAME
            )
        except Exception as e:
            logger.error(f"Failed to connect to SAP: {e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def build_query(self, table_name: str) -> str:
        if LOAD_MODE == "INCREMENTAL":
            from google.cloud import bigquery
            client = bigquery.Client(project=f'{INCREMENTAL_TIMESTAMP_SOURCE.split(".")[0]}')
            query = f"SELECT MAX({INCREMENTAL_FIELD}) FROM `{INCREMENTAL_TIMESTAMP_SOURCE}`"
            rows = list(client.query_and_wait(query))
            global timestamp
            timestamp = rows[0][0]
            logger.info(f"Extract data from {table_name} since {timestamp}.")
            query = f"SELECT * FROM SAPABAP1.{table_name} WHERE {INCREMENTAL_FIELD} >= {timestamp} "
            return query
        else:
            return f"SELECT * FROM SAPABAP1.{table_name}"
        
