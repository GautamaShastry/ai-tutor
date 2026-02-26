"""
Base loader interface for data sources.
"""
from abc import ABC, abstractmethod
from typing import AsyncIterator, List
from pathlib import Path

from app.data.models import ProcessedContent


class BaseLoader(ABC):
    """Abstract base class for data loaders"""
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
    
    @abstractmethod
    async def load(self) -> AsyncIterator[ProcessedContent]:
        """
        Load and process content from the data source.
        Yields ProcessedContent items ready for vector storage.
        """
        pass
    
    @abstractmethod
    def validate_source(self) -> bool:
        """Check if the data source files exist and are valid"""
        pass
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the data source"""
        pass
    
    @property
    @abstractmethod
    def license(self) -> str:
        """License of the data source"""
        pass
