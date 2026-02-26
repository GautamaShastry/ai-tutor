"""
Data source configurations for Telugu learning content.
Defines supported sources and their metadata.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class DataSourceType(str, Enum):
    """Types of data sources supported"""
    TATOEBA = "tatoeba"           # Sentence pairs with translations
    DAKSHINA = "dakshina"         # Transliteration data
    AKSHARANTAR = "aksharantar"   # Transliteration pairs
    SAMANANTAR = "samanantar"     # Parallel English-Telugu corpus
    WIKTIONARY = "wiktionary"     # Dictionary entries
    INDIC_CORP = "indic_corp"     # Monolingual Telugu text
    CUSTOM = "custom"             # User-provided content


@dataclass
class DataSourceConfig:
    """Configuration for a data source"""
    source_type: DataSourceType
    name: str
    license: str
    url: Optional[str] = None
    description: Optional[str] = None
    requires_download: bool = True


# Pre-configured data sources
DATA_SOURCES = {
    DataSourceType.TATOEBA: DataSourceConfig(
        source_type=DataSourceType.TATOEBA,
        name="Tatoeba Telugu Sentences",
        license="CC BY 2.0 FR / CC0",
        url="https://tatoeba.org/en/downloads",
        description="Telugu sentences with English translations",
    ),
    DataSourceType.DAKSHINA: DataSourceConfig(
        source_type=DataSourceType.DAKSHINA,
        name="Dakshina Dataset",
        license="CC BY-SA 4.0",
        url="https://github.com/google-research-datasets/dakshina",
        description="Telugu text with romanization for transliteration support",
    ),
    DataSourceType.AKSHARANTAR: DataSourceConfig(
        source_type=DataSourceType.AKSHARANTAR,
        name="AI4Bharat Aksharantar",
        license="CC BY 4.0",
        url="https://github.com/AI4Bharat/IndicXlit",
        description="Large-scale Indic-English transliteration pairs",
    ),
    DataSourceType.SAMANANTAR: DataSourceConfig(
        source_type=DataSourceType.SAMANANTAR,
        name="AI4Bharat Samanantar",
        license="CC0",
        url="https://indicnlp.ai4bharat.org/samanantar/",
        description="English-Telugu parallel corpus for translation exercises",
    ),
    DataSourceType.WIKTIONARY: DataSourceConfig(
        source_type=DataSourceType.WIKTIONARY,
        name="Telugu Wiktionary",
        license="CC BY-SA 4.0 / GFDL",
        url="https://te.wiktionary.org/",
        description="Dictionary entries with meanings and usage notes",
    ),
    DataSourceType.INDIC_CORP: DataSourceConfig(
        source_type=DataSourceType.INDIC_CORP,
        name="AI4Bharat IndicCorpV2",
        license="CC0",
        url="https://indicnlp.ai4bharat.org/corpora/",
        description="Large Telugu monolingual corpus",
    ),
}
