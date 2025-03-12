# extractors/sharepoint_files.py
import io
import re
from typing import Generator, Optional, Tuple, Any
import pandas as pd
from interfaces.api import BaseApiExtractor
from extractors.config import SHAREPOINT_FILE_ORIGINS

class SharepointFileExtractor(BaseApiExtractor):
    def authenticate(self):
        self.config = SHAREPOINT_FILE_ORIGINS[self.origin]
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": self.config["CLIENT_ID"],
            "client_secret": self.config["CLIENT_SECRET"],
            "scope": "https://graph.microsoft.com/.default"
        }

        response = self.session.post(
            f"https://login.microsoftonline.com/{self.config['TENANT_ID']}/oauth2/v2.0/token",
            data=auth_data
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_resources(self) -> Generator[Tuple[str, Any], None, None]:
        file_info = self.config["FILE_NAMES"]
        file_path = self.config["FILE_PATH"]

        for pattern, sheets in file_info.items():
            for file in self._find_matching_files(file_path, pattern):
                if sheets:
                    for sheet in sheets:
                        yield file, sheet
                else:
                    yield file, None

    def fetch_resource(self, file_name: str, sheet: Optional[str]) -> Tuple[io.BytesIO, str]:
        file_content = self._download_file(file_name)

        if sheet:
            df = pd.read_excel(io.BytesIO(file_content), sheet_name=sheet)
            output = io.BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return output, f"{file_name}_{sheet}.csv"

        return io.BytesIO(file_content), file_name

    def _find_matching_files(self, path: str, pattern: str) -> Generator[str, None, None]:
        url = f"https://graph.microsoft.com/v1.0/sites/{self.config['SITE_ID']}/drives/{self.config['DRIVE_ID']}/root:/{path.rstrip('/')}:/children"
        response = self.session.get(url, headers=self.headers)
        pattern = re.compile(pattern)

        for file_data in response.json().get('value', []):
            if pattern.match(file_data.get('name', '')):
                yield file_data['name']

    def _download_file(self, file_name: str) -> bytes:
        url = f"https://graph.microsoft.com/v1.0/sites/{self.config['SITE_ID']}/drives/{self.config['DRIVE_ID']}/root:/{self.config['FILE_PATH']}{file_name}:/content"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content
