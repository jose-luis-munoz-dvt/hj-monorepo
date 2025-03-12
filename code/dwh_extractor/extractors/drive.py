# extractors/google_drive.py
from typing import Generator, Tuple, Any
import pandas as pd
from interfaces.api import BaseApiExtractor
from extractors.config import GOOGLE_DRIVE_DOCS
from extractors.logger import logger

class GoogleDriveExtractor(BaseApiExtractor):
    def authenticate(self):
        # No authentication needed for public URLs
        pass

    def get_resources(self) -> Generator[Tuple[str, str], None, None]:
        """Yield (sheet_name, sheet_id) pairs"""
        config = GOOGLE_DRIVE_DOCS[self.origin][self.target]
        for sheet in config["sheets"]:
            yield sheet[0], sheet[1]  # (sheet_name, sheet_id)

    def fetch_resource(self, sheet_name: str, sheet_id: str) -> Tuple[pd.DataFrame, str]:
        """Fetch and process a Google Sheet"""
        config = GOOGLE_DRIVE_DOCS[self.origin][self.target]
        try:
            url = f'https://docs.google.com/spreadsheets/d/e/{config["doc_id"]}/pub?gid={sheet_id}&output=csv'
            df = pd.read_csv(url, on_bad_lines='skip')
            return df, sheet_name
        except Exception as e:
            logger.error(f"Failed to download sheet '{sheet_name}': {str(e)}")
            raise
