# extractors/sharepoint_lists.py
import re
from typing import Generator, Tuple, Any
import pandas as pd
from interfaces.api import BaseApiExtractor
from extractors.config import SHAREPOINT_LIST_ORIGINS

class SharepointListExtractor(BaseApiExtractor):
    def authenticate(self):
        self.config = SHAREPOINT_LIST_ORIGINS[self.origin]
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
        for list_name in self.config["LISTS"]:
            yield list_name, None

    def fetch_resource(self, list_name: str, _: Any) -> Tuple[pd.DataFrame, str]:
        list_id = self._get_list_id(list_name)
        url = f'https://graph.microsoft.com/v1.0/sites/{self.config["SITE_ID"]}/lists/{list_id}/items?expand=fields'

        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()

        items = response.json().get('value', [])
        df = pd.DataFrame([item['fields'] for item in items if item.get('fields')])
        return df, list_name

    def _get_list_id(self, list_name: str) -> str:
        url = f"https://graph.microsoft.com/v1.0/sites/{self.config['SITE_ID']}/lists?$filter=displayName eq '{list_name}'"
        response = self.session.get(url, headers=self.headers)
        return response.json()['value'][0]['id']
