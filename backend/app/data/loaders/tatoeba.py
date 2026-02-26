"""
Loader for Tatoeba sentence pairs.
Tatoeba provides Telugu sentences with English translations.

Expected file format (TSV):
- sentences_detailed.csv: id, lang, text, username, date_added, date_modified
- links.csv: sentence_id, translation_id
- Or pre-filtered Telugu-English pairs

Download from: https://tatoeba.org/en/downloads
"""
import csv
import uuid
from pathlib import Path
from typing import AsyncIterator, Dict, List, Optional

from app.data.loaders.base import BaseLoader
from app.data.models import (
    ProcessedContent,
    ContentType,
    DifficultyLevel,
    SentenceContent,
)


class TatoebaLoader(BaseLoader):
    """Loader for Tatoeba Telugu-English sentence pairs"""
    
    def __init__(self, data_path: Path):
        super().__init__(data_path)
        self._telugu_sentences: Dict[str, str] = {}
        self._english_sentences: Dict[str, str] = {}
        self._links: List[tuple] = []
    
    @property
    def source_name(self) -> str:
        return "Tatoeba"
    
    @property
    def license(self) -> str:
        return "CC BY 2.0 FR"
    
    def validate_source(self) -> bool:
        """Check for required Tatoeba files"""
        # Check for pre-processed pairs file first
        pairs_file = self.data_path / "telugu_english_pairs.tsv"
        if pairs_file.exists():
            return True
        
        # Check for raw Tatoeba files
        sentences_file = self.data_path / "sentences.csv"
        links_file = self.data_path / "links.csv"
        return sentences_file.exists() and links_file.exists()
    
    async def load(self) -> AsyncIterator[ProcessedContent]:
        """Load Telugu-English sentence pairs"""
        pairs_file = self.data_path / "telugu_english_pairs.tsv"
        
        if pairs_file.exists():
            async for content in self._load_pairs_file(pairs_file):
                yield content
        else:
            async for content in self._load_raw_tatoeba():
                yield content
    
    async def _load_pairs_file(self, filepath: Path) -> AsyncIterator[ProcessedContent]:
        """Load from pre-processed pairs file (TSV: telugu, english)"""
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            next(reader, None)  # Skip header if present
            
            for row in reader:
                if len(row) >= 2:
                    telugu, english = row[0].strip(), row[1].strip()
                    
                    if telugu and english:
                        content_id = str(uuid.uuid4())
                        difficulty = self._estimate_difficulty(telugu)
                        
                        yield ProcessedContent(
                            id=content_id,
                            content_type=ContentType.SENTENCE,
                            text=f"{telugu} | {english}",
                            telugu_text=telugu,
                            english_text=english,
                            difficulty=difficulty,
                            source=self.source_name,
                            license=self.license,
                            metadata={
                                "sentence_type": "example",
                            },
                        )
    
    async def _load_raw_tatoeba(self) -> AsyncIterator[ProcessedContent]:
        """Load from raw Tatoeba dump files"""
        # Load sentences
        sentences_file = self.data_path / "sentences.csv"
        with open(sentences_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) >= 3:
                    sent_id, lang, text = row[0], row[1], row[2]
                    if lang == "tel":
                        self._telugu_sentences[sent_id] = text
                    elif lang == "eng":
                        self._english_sentences[sent_id] = text
        
        # Load links
        links_file = self.data_path / "links.csv"
        with open(links_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) >= 2:
                    self._links.append((row[0], row[1]))
        
        # Generate pairs
        for tel_id, eng_id in self._links:
            if tel_id in self._telugu_sentences and eng_id in self._english_sentences:
                telugu = self._telugu_sentences[tel_id]
                english = self._english_sentences[eng_id]
                
                content_id = str(uuid.uuid4())
                difficulty = self._estimate_difficulty(telugu)
                
                yield ProcessedContent(
                    id=content_id,
                    content_type=ContentType.SENTENCE,
                    text=f"{telugu} | {english}",
                    telugu_text=telugu,
                    english_text=english,
                    difficulty=difficulty,
                    source=self.source_name,
                    license=self.license,
                    metadata={
                        "tatoeba_tel_id": tel_id,
                        "tatoeba_eng_id": eng_id,
                    },
                )
    
    def _estimate_difficulty(self, telugu_text: str) -> DifficultyLevel:
        """Estimate difficulty based on sentence length and complexity"""
        word_count = len(telugu_text.split())
        
        if word_count <= 4:
            return DifficultyLevel.BEGINNER
        elif word_count <= 8:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.ADVANCED
