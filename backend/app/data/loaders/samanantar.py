"""
Loader for AI4Bharat Samanantar parallel corpus.
Contains ~150K+ Telugu-English sentence pairs.

Download from: https://indicnlp.ai4bharat.org/samanantar/
License: CC0 (Public Domain)

Expected file formats:
- en-te/train.en and en-te/train.te (parallel text files)
- Or: samanantar_te_en.tsv (TSV with english, telugu columns)
"""
import uuid
from pathlib import Path
from typing import AsyncIterator

from app.data.loaders.base import BaseLoader
from app.data.models import (
    ProcessedContent,
    ContentType,
    DifficultyLevel,
)


class SamanantatLoader(BaseLoader):
    """Loader for AI4Bharat Samanantar Telugu-English parallel corpus"""
    
    def __init__(self, data_path: Path, max_items: int = None):
        """
        Args:
            data_path: Path to samanantar data directory
            max_items: Maximum items to load (None for all)
        """
        super().__init__(data_path)
        self.max_items = max_items
    
    @property
    def source_name(self) -> str:
        return "AI4Bharat Samanantar"
    
    @property
    def license(self) -> str:
        return "CC0"
    
    def validate_source(self) -> bool:
        """Check for Samanantar data files"""
        # Check for TSV format
        tsv_file = self.data_path / "samanantar_te_en.tsv"
        if tsv_file.exists():
            return True
        
        # Check for parallel text files
        en_file = self.data_path / "train.en"
        te_file = self.data_path / "train.te"
        if en_file.exists() and te_file.exists():
            return True
        
        # Check in en-te subdirectory
        en_te_dir = self.data_path / "en-te"
        if en_te_dir.exists():
            en_file = en_te_dir / "train.en"
            te_file = en_te_dir / "train.te"
            if en_file.exists() and te_file.exists():
                return True
        
        return False
    
    async def load(self) -> AsyncIterator[ProcessedContent]:
        """Load Telugu-English sentence pairs"""
        # Try TSV format first
        tsv_file = self.data_path / "samanantar_te_en.tsv"
        if tsv_file.exists():
            async for content in self._load_tsv(tsv_file):
                yield content
            return
        
        # Try parallel text files
        en_file = self.data_path / "train.en"
        te_file = self.data_path / "train.te"
        
        if not en_file.exists():
            en_te_dir = self.data_path / "en-te"
            en_file = en_te_dir / "train.en"
            te_file = en_te_dir / "train.te"
        
        if en_file.exists() and te_file.exists():
            async for content in self._load_parallel_files(en_file, te_file):
                yield content
    
    async def _load_tsv(self, filepath: Path) -> AsyncIterator[ProcessedContent]:
        """Load from TSV file (english, telugu columns)"""
        import csv
        
        count = 0
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            
            # Skip header if present
            first_row = next(reader, None)
            if first_row and first_row[0].lower() not in ["english", "en", "eng"]:
                # First row is data, process it
                if len(first_row) >= 2:
                    content = self._create_content(first_row[0], first_row[1])
                    if content:
                        yield content
                        count += 1
            
            for row in reader:
                if self.max_items and count >= self.max_items:
                    break
                
                if len(row) >= 2:
                    english, telugu = row[0].strip(), row[1].strip()
                    content = self._create_content(english, telugu)
                    if content:
                        yield content
                        count += 1
    
    async def _load_parallel_files(
        self, en_file: Path, te_file: Path
    ) -> AsyncIterator[ProcessedContent]:
        """Load from parallel text files (one sentence per line)"""
        count = 0
        
        with open(en_file, "r", encoding="utf-8") as en_f, \
             open(te_file, "r", encoding="utf-8") as te_f:
            
            for en_line, te_line in zip(en_f, te_f):
                if self.max_items and count >= self.max_items:
                    break
                
                english = en_line.strip()
                telugu = te_line.strip()
                
                content = self._create_content(english, telugu)
                if content:
                    yield content
                    count += 1
    
    def _create_content(self, english: str, telugu: str) -> ProcessedContent | None:
        """Create ProcessedContent from a sentence pair"""
        if not english or not telugu:
            return None
        
        # Skip very short or very long sentences
        if len(telugu) < 5 or len(telugu) > 500:
            return None
        if len(english) < 3 or len(english) > 500:
            return None
        
        difficulty = self._estimate_difficulty(telugu, english)
        domains = self._detect_domains(english, telugu)
        
        return ProcessedContent(
            id=str(uuid.uuid4()),
            content_type=ContentType.SENTENCE,
            text=f"{telugu} | {english}",
            telugu_text=telugu,
            english_text=english,
            difficulty=difficulty,
            domains=domains,
            source=self.source_name,
            license=self.license,
            metadata={
                "corpus": "samanantar",
            },
        )
    
    def _estimate_difficulty(self, telugu: str, english: str) -> DifficultyLevel:
        """Estimate difficulty based on sentence complexity"""
        telugu_words = len(telugu.split())
        english_words = len(english.split())
        avg_words = (telugu_words + english_words) / 2
        
        if avg_words <= 5:
            return DifficultyLevel.BEGINNER
        elif avg_words <= 12:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.ADVANCED
    
    def _detect_domains(self, english: str, telugu: str) -> list:
        """Detect content domains from text"""
        domains = []
        text_lower = english.lower()
        
        # Office/work keywords
        office_keywords = ["office", "work", "meeting", "project", "manager", "employee", "company", "business"]
        if any(kw in text_lower for kw in office_keywords):
            domains.append("office")
        
        # Family keywords
        family_keywords = ["mother", "father", "sister", "brother", "family", "home", "house", "children"]
        if any(kw in text_lower for kw in family_keywords):
            domains.append("family")
        
        # Travel keywords
        travel_keywords = ["travel", "train", "bus", "airport", "hotel", "ticket", "station", "journey"]
        if any(kw in text_lower for kw in travel_keywords):
            domains.append("travel")
        
        # Movies/entertainment
        movie_keywords = ["movie", "film", "actor", "song", "music", "cinema", "hero"]
        if any(kw in text_lower for kw in movie_keywords):
            domains.append("movies")
        
        if not domains:
            domains.append("general")
        
        return domains
