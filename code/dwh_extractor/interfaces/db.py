from abc import ABC, abstractmethod
from typing import Generator, Tuple, Any
import pandas as pd
from extractors.logger import logger
from extractors.config import CHUNK_SIZE, ROWS_PER_BATCH

class BaseDbExtractor(ABC):
    def __init__(self, origin: str):
        self.origin = origin
        self.conn = None
        self.schema = None

    @abstractmethod
    def connect(self) -> Any:
        """Establish database connection"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass

    @abstractmethod
    def build_query(self, table_name: str) -> str:
        """Build database-specific query"""
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def get_yielded_table_data(self, table_name: str) -> Generator[pd.DataFrame, None, None]:
        """Yield DataFrame chunks from specified table"""
        try:
            query = self.build_query(table_name)
            for chunk in pd.read_sql(
                query,
                self.conn,
                chunksize=ROWS_PER_BATCH
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Failed to query table {table_name}: {e}")
            raise

def extract_data(extractor_class: BaseDbExtractor, origin: str, table: str) -> Generator[Tuple[pd.DataFrame, str, int], None, None]:
    """Generic extraction function for all databases"""
    logger.info(f"Processing Extractor: {extractor_class.__name__}, Origin: {origin}, Target: {table}")

    with extractor_class(origin) as extractor:
        data_generator = extractor.get_yielded_table_data(table)

        total_rows = 0
        chunk_number = 0
        accumulated_chunks = []

        for df_chunk in data_generator:
            chunk_rows = len(df_chunk)
            total_rows += chunk_rows
            accumulated_chunks.append(df_chunk)
            logger.info(f"Extraction progress: {total_rows} rows processed from '{table}'")

            if (len(accumulated_chunks) >= CHUNK_SIZE) or (chunk_rows < ROWS_PER_BATCH):
                combined_df = pd.concat(accumulated_chunks, ignore_index=True)
                logger.info(f"Yielding chunk {chunk_number} with {len(combined_df)} rows (Total: {total_rows} rows)")
                yield combined_df, table, chunk_number
                chunk_number += 1
                accumulated_chunks = []

        if accumulated_chunks:
            combined_df = pd.concat(accumulated_chunks, ignore_index=True)
            logger.info(f"Yielding final chunk {chunk_number} with {len(combined_df)} rows (Total: {total_rows} rows)")
            yield combined_df, table, chunk_number
