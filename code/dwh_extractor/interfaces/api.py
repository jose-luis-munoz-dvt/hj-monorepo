# interfaces/api.py
from abc import ABC, abstractmethod
from typing import Generator, Any, Tuple, Optional
import requests
import pandas as pd
from extractors.logger import logger

class BaseApiExtractor(ABC):
    def __init__(self, origin: str, target: str):
        self.origin = origin
        self.target = target
        self.session = requests.Session()
        self.config = None
        self.access_token = None

    @abstractmethod
    def get_resources(self) -> Generator[Tuple[str, Any], None, None]:
        """Yield (resource_name, resource_info) tuples"""
        pass

    @abstractmethod
    def fetch_resource(self, resource_name: str, resource_info: Any) -> Tuple[pd.DataFrame, str]:
        """Fetch and process a resource"""
        pass

    @abstractmethod
    def authenticate(self) -> None:
        """Handle API authentication"""
        pass

    def __enter__(self):
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

def extract_api_data(extractor_class: BaseApiExtractor, origin: str, target: Optional[str] = None) -> Generator[Tuple[Any, str, None], None, None]:
    """Generic extraction flow for API-based sources"""
    with extractor_class(origin, target) as extractor:
        for resource_name, resource_info in extractor.get_resources():
            try:
                logger.info(f"Processing Extractor: {extractor_class.__name__}, Origin: {origin}, Target: {target}, Resource: {resource_name}, {resource_info}")
                data, processed_name = extractor.fetch_resource(resource_name, resource_info)
                yield data, processed_name, None
            except Exception as e:
                logger.error(f"Failed to process {resource_name}: {str(e)}")
                raise
