# Telugu Learning Content Data

This directory contains Telugu learning content for the AI Tutor.

## Directory Structure

```
data/
├── sample/           # Sample content (included)
├── tatoeba/          # Tatoeba sentence pairs (download required)
├── dakshina/         # Dakshina transliteration data (download required)
├── samanantar/       # AI4Bharat parallel corpus (download required)
└── custom/           # Your custom content
```

## Sample Content

The `sample/` directory contains starter content with:
- Basic greetings and phrases
- Common vocabulary
- Office-related phrases
- Family-related vocabulary and sentences

## Adding External Data Sources

### Tatoeba (Sentence Pairs)

1. Download from: https://tatoeba.org/en/downloads
2. Get `sentences.csv` and `links.csv`
3. Place in `data/tatoeba/`
4. Or create a pre-filtered `telugu_english_pairs.tsv` file

License: CC BY 2.0 FR (some CC0)

### Dakshina (Transliteration)

1. Download from: https://github.com/google-research-datasets/dakshina
2. Extract Telugu data
3. Place in `data/dakshina/`

License: CC BY-SA 4.0

### AI4Bharat Samanantar (Parallel Corpus)

1. Download from: https://indicnlp.ai4bharat.org/samanantar/
2. Extract Telugu-English pairs
3. Place in `data/samanantar/`

License: CC0

### AI4Bharat Aksharantar (Transliteration)

1. Download from: https://github.com/AI4Bharat/IndicXlit
2. Extract Telugu transliteration pairs
3. Place in `data/aksharantar/`

License: CC BY 4.0

## Custom Content Format

### JSON Format

```json
{
  "content": [
    {
      "type": "sentence",
      "telugu": "తెలుగు వాక్యం",
      "english": "Telugu sentence",
      "transliteration": "telugu vākyaṁ",
      "difficulty": "beginner|intermediate|advanced",
      "domains": ["general", "office", "family", "movies"]
    }
  ]
}
```

### CSV Format

```csv
telugu,english,transliteration,type,difficulty,domains
తెలుగు వాక్యం,Telugu sentence,telugu vākyaṁ,sentence,beginner,"general,office"
```

## Content Types

- `sentence` - Example sentences with translations
- `vocabulary` - Word definitions
- `grammar_rule` - Grammar explanations
- `transliteration` - Script conversion pairs
- `dialogue` - Conversation examples
- `exercise` - Practice items

## Difficulty Levels

- `beginner` - Simple words and short sentences
- `intermediate` - Compound sentences, common grammar
- `advanced` - Complex sentences, formal language

## Domains

- `general` - Everyday usage
- `office` - Workplace communication
- `family` - Home and relationships
- `movies` - Entertainment, colloquial speech

## Running Ingestion

```bash
# Ingest sample data
python -m scripts.ingest_data --source custom --path ./data/sample --name "Sample Content"

# Ingest Tatoeba data
python -m scripts.ingest_data --source tatoeba --path ./data/tatoeba

# Ingest all sources
python -m scripts.ingest_data --source all --path ./data
```

## License Compliance

When using external data sources, ensure you comply with their licenses:
- CC BY 2.0 FR: Attribution required
- CC BY-SA 4.0: Attribution + ShareAlike
- CC0: Public domain, no restrictions
- GFDL: GNU Free Documentation License

Always include source attribution in your deployment.
