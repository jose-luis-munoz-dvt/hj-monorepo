import datetime
from google.cloud import storage
from io import BytesIO
import concurrent.futures
import pyarrow as pa
import pyarrow.parquet as pq

from extractors.logger import logger
from extractors.config import GCP_PROJECT_ID, GCS_BUCKET_ID, LOAD_MODE


CURRENT_DATE = datetime.date.today() .strftime("%Y%m%d")
storage_client = storage.Client(project=GCP_PROJECT_ID)
bucket = storage_client.get_bucket(GCS_BUCKET_ID)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)  # Limited concurrency


def upload_to_storage(extractor: str, origin: str, table: str, df: any, chunk_number: int) -> None:
    bucket = storage_client.get_bucket(GCS_BUCKET_ID)

    if extractor in ["SAP", "SQL_SERVER", "ORACLE"]:
        if table == "AUSP":
            df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
            df.to_csv(f'gs://{GCS_BUCKET_ID}/{extractor}/{origin}/{table}/{table}_chunk_{chunk_number}.csv', index=False, compression='gzip', sep='^') # sep='^'
            return
        if LOAD_MODE == "INCREMENTAL":
            from extractors.sap import timestamp
            df.to_parquet(f'gs://{GCS_BUCKET_ID}/{extractor}/{origin}/{table}/{table}_chunk_{chunk_number}_timestamp_{timestamp}.parquet', compression='gzip') # sep='^'
            return
        try:
            if df.empty:
                logger.warning(f"Skipping empty chunk {chunk_number} for {table}")
                return

            buffer = BytesIO()
            pa_table = pa.Table.from_pandas(df)
            pq.write_table(
                pa_table,
                buffer,
                compression='SNAPPY',
                use_dictionary=True
            )
            buffer_size = buffer.tell()
            buffer.seek(0)

            blob_path = f"{extractor}/{origin}/{table}/{table}_chunk_{chunk_number}.parquet"
            blob = bucket.blob(blob_path)

            future = executor.submit(
                _upload_buffer,
                blob,
                buffer,
                buffer_size
            )

            future.add_done_callback(
                lambda f: logger.info(f"Upload completed for {blob_path} ({buffer_size/1e6:.1f}MB)")
            )

        except Exception as e:
            logger.error(f"Upload failed for chunk {chunk_number}: {str(e)}")
            raise
        finally:
            # Do NOT close buffer here - it's handled in the callback
            del df
    elif extractor in ["GOOGLE_DRIVE", "SHAREPOINT_LISTS"]:
        if not df.empty:
            df.to_csv(f'gs://{GCS_BUCKET_ID}/{extractor}/{origin}/{table}/{table}_chunk_{chunk_number}.csv', index=False)
    elif extractor == 'SHAREPOINT_FILES':
        blob_name = f'{extractor}/{origin}/{table}'.replace(' ', '_')
        blob = bucket.blob(blob_name)
        blob.upload_from_file(df, content_type='application/vnd.ms-excel')

def _upload_buffer(blob, buffer, buffer_size):
    """Handle actual upload with retries and resource cleanup"""
    try:
        blob.upload_from_file(
            buffer,
            content_type='application/parquet',
            timeout=300,
            retry=storage.retry.DEFAULT_RETRY.with_deadline(600)
        )
        return True
    finally:
        buffer.close()


def backup_old_objects(extractor:str, origin: str, table: str):
    logger.info("Backing up existing data in Cloud Storage...")

    if extractor in ["SAP", "SQL_SERVER", "ORACLE"]:
        prefix = f"{extractor}/{origin}/{table}/"
        backup_prefix = f"backup/{extractor}/{origin}/{table}/"
        delimiter = "/"
        include_folders = True
    else:
        prefix = f"{extractor}/{origin}/"
        backup_prefix = f"backup/{extractor}/{origin}/"
        delimiter = None
        include_folders = False

    # delete existing backup if exists
    blobs = bucket.list_blobs(prefix=backup_prefix)
    for blob in blobs:
        generation_match_precondition = None
        blob.reload()
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)
        logger.info(f"Deleted {blob.name}")
    del blobs

    # move to backup directory
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter , include_folders_as_prefixes=include_folders)
    for blob in blobs:
        backup_blob_path = f"{backup_prefix}{blob.name[len(prefix):]}"
        bucket.rename_blob(blob, backup_blob_path)
        logger.info(f"Moved {blob.name} to {backup_prefix} directory")


def restore_backup_objects(extractor:str, origin: str, table: str):
    logger.info(f"Restoring {origin}/{table}/ data in Cloud Storage...")

    if extractor in ["SAP", "SQL_SERVER", "ORACLE"]:
        prefix = f"{extractor}/{origin}/{table}/"
        backup_prefix = f"backup/{extractor}/{origin}/{table}/"
        delimiter = "/"
        include_folders = True
    else:
        prefix = f"{extractor}/{origin}/"
        backup_prefix = f"backup/{extractor}/{origin}/"
        delimiter = None
        include_folders = False

    # delete temp files if exist
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        generation_match_precondition = None
        blob.reload()
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)
        logger.info(f"Deleted {blob.name}")
    del blobs

    blobs = bucket.list_blobs(prefix=backup_prefix, delimiter=delimiter , include_folders_as_prefixes=include_folders)
    for blob in blobs:
        blob_path = blob.name[len("backup/"):]
        bucket.rename_blob(blob, blob_path)
        logger.info(f"Moved {blob.name} to {prefix} directory")
