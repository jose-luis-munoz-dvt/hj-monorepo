from storage import upload_to_storage, backup_old_objects, restore_backup_objects
from extractors.logger import logger
from extractors.sap import SapExtractor
from extractors.sql_server import SQLServerExtractor
from extractors.oracle import OracleExtractor
from extractors.sharepoint import SharepointFileExtractor
from extractors.sharepoint_lists import SharepointListExtractor
from extractors.drive import GoogleDriveExtractor
from interfaces.db import extract_data
from interfaces.api import extract_api_data

import os
from datetime import timedelta
from timeit import default_timer as timer

EXTRACTOR_DISPATCHER = {
    "SAP":              lambda origin, target: extract_data(SapExtractor, origin, target),
    "SQL_SERVER":       lambda origin, target: extract_data(SQLServerExtractor, origin, target),
    "ORACLE":           lambda origin, target: extract_data(OracleExtractor, origin, target),
    "SHAREPOINT_FILES": lambda origin, target: extract_api_data(SharepointFileExtractor, origin, target),
    "SHAREPOINT_LISTS": lambda origin, target: extract_api_data(SharepointListExtractor, origin, target),
    "GOOGLE_DRIVE":     lambda origin, target: extract_api_data(GoogleDriveExtractor, origin, target),
}

EXTRACTOR = os.environ.get("EXTRACTOR")
ORIGIN    = os.environ.get("ORIGIN")
TARGET    = os.environ.get("TARGET")

start = timer()

try:
    if EXTRACTOR:
        backup_old_objects(extractor=EXTRACTOR, origin=ORIGIN, table=TARGET)

        raw_data = EXTRACTOR_DISPATCHER[EXTRACTOR](ORIGIN, TARGET)

        for data, table, chunk in raw_data:
            upload_to_storage(
                extractor=EXTRACTOR,
                origin=ORIGIN,
                table=table,
                df=data,
                chunk_number=chunk if chunk else 0
            )
    else:
        logger.error("Missing environment variables. Cancelling dwh data extraction.")
except Exception as e:
    restore_backup_objects(extractor=EXTRACTOR, origin=ORIGIN, table=TARGET)
    raise e

end = timer()
logger.info(f"Elapsed time for {EXTRACTOR}/{TARGET} extraction was {timedelta(seconds=end-start)}")
