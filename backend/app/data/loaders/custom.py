"""
Loader for custom JSON/CSV content files.
Supports flexible formats for user-provided Telugu learning content.
"""
import csv
import json
import uuid
from pathlib import Path
from typing import AsyncIterator, List

from app.data.loaders.base import BaseLoader
from app.data.models import (
    ProcessedContent,
    ContentType,
    DifficultyLevel,
)


class CustomLoader(BaseLoader):
    """Loader for custom content files (JSON/CSV)"""
    
    def __init__(self, data_path: Path, source_name: str = "Custom", license_info: str = "Custom"):
        super().__init__(data_path)
        self._source_name = source_name
        self._license = license_info
    
    @property
    def source_name(self) -> str:
        return self._source_name
    
    @property
    def license(self) -> str:
        return self._license
    
    def validate_source(self) -> bool:
        """Check if data path exists and contains valid files"""
        if not self.data_path.exists():
            return False
        
        # Check for JSON or CSV files
        json_files = list(self.data_path.glob("*.json"))
        csv_files = list(self.data_path.glob("*.csv"))
        
        return len(json_files) > 0 or len(csv_files) > 0
    
    async def load(self) -> AsyncIterator[ProcessedContent]:
        """Load content from all JSON and CSV files in the data path"""
        # Load JSON files
        for json_file in self.data_path.glob("*.json"):
            async for content in self._load_json(json_file):
                yield content
        
        # Load CSV files
        for csv_file in self.data_path.glob("*.csv"):
            async for content in self._load_csv(csv_file):
                yield content
    
    async def _load_json(self, filepath: Path) -> AsyncIterator[ProcessedContent]:
        """
        Load from JSON file.
        
        Expected format:
        {
            "content": [
                {
                    "type": "sentence|vocabulary|grammar_rule",
                    "telugu": "తెలుగు టెక్స్ట్",
                    "english": "English text",
                    "transliteration": "telugu text" (optional),
                    "difficulty": "beginner|intermediate|advanced" (optional),
                    "domains": ["office", "family"] (optional),
                    "metadata": {} (optional)
                }
            ]
        }
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        items = data.get("content", data) if isinstance(data, dict) else data
        
        for item in items:
            if isinstance(item, dict):
                content = self._parse_item(item)
                if content:
                    yield content
    
    async def _load_csv(self, filepath: Path) -> AsyncIterator[ProcessedContent]:
        """
        Load from CSV file.
        
        Expected columns: telugu, english, transliteration (optional), 
                         type (optional), difficulty (optional), domains (optional)
        """
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                content = self._parse_csv_row(row)
                if content:
                    yield content
    
    def _parse_item(self, item: dict) -> ProcessedContent | None:
        """Parse a JSON item into ProcessedContent"""
        telugu = item.get("telugu", "").strip()
        english = item.get("english", "").strip()
        
        if not telugu or not english:
            return None
        
        content_type = self._parse_content_type(item.get("type", "sentence"))
        difficulty = self._parse_difficulty(item.get("difficulty", "intermediate"))
        domains = item.get("domains", [])
        
        return ProcessedContent(
            id=str(uuid.uuid4()),
            content_type=content_type,
            text=f"{telugu} | {english}",
            telugu_text=telugu,
            english_text=english,
            transliteration=item.get("transliteration"),
            difficulty=difficulty,
            domains=domains,
            source=self.source_name,
            license=self.license,
            metadata=item.get("metadata", {}),
        )
    
    def _parse_csv_row(self, row: dict) -> ProcessedContent | None:
        """Parse a CSV row into ProcessedContent"""
        telugu = row.get("telugu", "").strip()
        english = row.get("english", "").strip()
        
        if not telugu or not english:
            return None
        
        content_type = self._parse_content_type(row.get("type", "sentence"))
        difficulty = self._parse_difficulty(row.get("difficulty", "intermediate"))
        
        # Parse domains from comma-separated string
        domains_str = row.get("domains", "")
        domains = [d.strip() for d in domains_str.split(",") if d.strip()]
        
        return ProcessedContent(
            id=str(uuid.uuid4()),
            content_type=content_type,
            text=f"{telugu} | {english}",
            telugu_text=telugu,
            english_text=english,
            transliteration=row.get("transliteration"),
            difficulty=difficulty,
            domains=domains,
            source=self.source_name,
            license=self.license,
        )
    
    def _parse_content_type(self, type_str: str) -> ContentType:
        """Parse content type string"""
        type_map = {
            "sentence": ContentType.SENTENCE,
            "vocabulary": ContentType.VOCABULARY,
            "vocab": ContentType.VOCABULARY,
            "grammar": ContentType.GRAMMAR_RULE,
            "grammar_rule": ContentType.GRAMMAR_RULE,
            "transliteration": ContentType.TRANSLITERATION,
            "dialogue": ContentType.DIALOGUE,
            "exercise": ContentType.EXERCISE,
        }
        return type_map.get(type_str.lower(), ContentType.SENTENCE)
    
    def _parse_difficulty(self, diff_str: str) -> DifficultyLevel:
        """Parse difficulty string"""
        diff_map = {
            "beginner": DifficultyLevel.BEGINNER,
            "easy": DifficultyLevel.BEGINNER,
            "intermediate": DifficultyLevel.INTERMEDIATE,
            "medium": DifficultyLevel.INTERMEDIATE,
            "advanced": DifficultyLevel.ADVANCED,
            "hard": DifficultyLevel.ADVANCED,
        }
        return diff_map.get(diff_str.lower(), DifficultyLevel.INTERMEDIATE)
