# Telugu AI Tutor - Data Setup Guide

Complete guide to downloading and using Telugu learning data for this project.

## Quick Start (Recommended)

### Step 1: Create Expanded Sample Data (No Download Needed)
```bash
cd backend
python -m scripts.download_data --source sample
```
This creates ~120 vocabulary items and sentences instantly.

### Step 2: Preview the Data
```bash
python -m scripts.ingest_data --source custom --path ./data/sample --dry-run
```

### Step 3: Start Infrastructure
```bash
cd ..
docker-compose up -d qdrant
```

### Step 4: Ingest Sample Data
```bash
cd backend
python -m scripts.ingest_data --source custom --path ./data/sample
```

---

## Option A: AI4Bharat Samanantar (~150K Sentences) ⭐ RECOMMENDED

This is the largest and best quality Telugu-English parallel corpus.

### Method 1: Automatic Download (Easiest)

```bash
cd backend

# Install datasets library
pip install datasets

# Download Samanantar (downloads ~5000 samples automatically)
python -m scripts.download_data --source samanantar
```

### Method 2: Manual Download (Full Dataset)

1. **Using Python:**
```python
pip install datasets

# Create a script to download full dataset
from datasets import load_dataset

ds = load_dataset('ai4bharat/samanantar', 'te', split='train')

# Save to TSV
with open('backend/data/samanantar/samanantar_te_en.tsv', 'w', encoding='utf-8') as f:
    f.write("english\ttelugu\n")
    for item in ds:
        english = item['tgt'].strip()
        telugu = item['src'].strip()
        if english and telugu:
            f.write(f"{english}\t{telugu}\n")
```

2. **Using Website:**
   - Go to: https://indicnlp.ai4bharat.org/samanantar/
   - Download the `en-te` (English-Telugu) files
   - Extract to `backend/data/samanantar/`

### Using Samanantar Data

```bash
cd backend

# Preview first 100 items
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --dry-run

# Ingest 10,000 items (good for testing)
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --max-items 10000

# Ingest all (~150K items, takes time)
python -m scripts.ingest_data --source samanantar --path ./data/samanantar
```

**License:** CC0 (Public Domain)

---

## Option B: Tatoeba Sentences

Community-contributed sentences with translations.

### Download Tatoeba

```bash
cd backend
python -m scripts.download_data --source tatoeba
```

This downloads Telugu and English sentences and creates pairs automatically.

### Using Tatoeba Data

```bash
# Preview
python -m scripts.ingest_data --source tatoeba --path ./data/tatoeba --dry-run

# Ingest
python -m scripts.ingest_data --source tatoeba --path ./data/tatoeba
```

**License:** CC BY 2.0 FR

---

## Option C: OPUS Corpora (Alternative)

Multiple sources including OpenSubtitles, WikiMatrix, etc.

### Download from OPUS

1. Go to: https://opus.nlpl.eu/
2. Search for "Telugu" or "te"
3. Select a corpus (recommended: WikiMatrix, CCAligned)
4. Download Telugu-English parallel files
5. Extract to `backend/data/opus/`

### Format the Data

OPUS files are usually in TMX or Moses format. Convert to TSV:

```python
# Example for Moses format (.en and .te files)
with open('corpus.en', 'r', encoding='utf-8') as en_f, \
     open('corpus.te', 'r', encoding='utf-8') as te_f, \
     open('backend/data/opus/opus_te_en.tsv', 'w', encoding='utf-8') as out_f:
    
    out_f.write("english\ttelugu\n")
    for en_line, te_line in zip(en_f, te_f):
        out_f.write(f"{en_line.strip()}\t{te_line.strip()}\n")
```

### Using OPUS Data

```bash
python -m scripts.ingest_data --source custom --path ./data/opus --name "OPUS Corpus"
```

---

## Option D: Create Your Own Custom Data

### JSON Format

Create `backend/data/custom/my_content.json`:

```json
{
  "content": [
    {
      "type": "sentence",
      "telugu": "నేను తెలుగు నేర్చుకుంటున్నాను",
      "english": "I am learning Telugu",
      "transliteration": "nēnu telugu nērcukuṇṭunnānu",
      "difficulty": "intermediate",
      "domains": ["general"]
    },
    {
      "type": "vocabulary",
      "telugu": "పుస్తకం",
      "english": "book",
      "transliteration": "pustakaṁ",
      "difficulty": "beginner",
      "domains": ["general"]
    }
  ]
}
```

### CSV Format

Create `backend/data/custom/my_vocab.csv`:

```csv
telugu,english,transliteration,type,difficulty,domains
పుస్తకం,book,pustakaṁ,vocabulary,beginner,general
నేను తెలుగు నేర్చుకుంటున్నాను,I am learning Telugu,nēnu telugu nērcukuṇṭunnānu,sentence,intermediate,general
```

### Using Custom Data

```bash
python -m scripts.ingest_data --source custom --path ./data/custom --name "My Content"
```

---

## Complete Workflow

### 1. Setup Environment

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start infrastructure
cd ..
docker-compose up -d
```

### 2. Download Data (Choose One or More)

```bash
cd backend

# Option A: Sample data (instant)
python -m scripts.download_data --source sample

# Option B: Samanantar (best quality, ~150K)
pip install datasets
python -m scripts.download_data --source samanantar

# Option C: Tatoeba
python -m scripts.download_data --source tatoeba

# Option D: All
python -m scripts.download_data --source all
```

### 3. Preview Data (Dry Run)

```bash
# Preview sample
python -m scripts.ingest_data --source custom --path ./data/sample --dry-run

# Preview Samanantar
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --dry-run
```

### 4. Ingest Data into Vector Database

```bash
# Make sure Qdrant is running
docker ps | grep qdrant

# Ingest sample data
python -m scripts.ingest_data --source custom --path ./data/sample

# Ingest Samanantar (with limit for testing)
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --max-items 10000

# Ingest all sources
python -m scripts.ingest_data --source all --path ./data
```

### 5. Verify Ingestion

The script will show statistics:
```
=== Ingestion Complete ===
Total processed: 10000
Total stored: 9987
Errors: 13

Vector DB collection 'telugu_content': 9987 items
```

---

## Data Sources Summary

| Source | Size | Quality | License | Best For |
|--------|------|---------|---------|----------|
| **Sample** | ~120 items | High | Custom | Quick start, testing |
| **Samanantar** | ~150K pairs | High | CC0 | Production, comprehensive |
| **Tatoeba** | ~1-5K pairs | Medium | CC BY 2.0 | Community content |
| **OPUS** | Varies | Medium | Varies | Specific domains |
| **Custom** | Your choice | Your control | Your choice | Specialized content |

---

## Troubleshooting

### "No module named 'qdrant_client'"
```bash
pip install qdrant-client
```

### "Could not connect to Qdrant"
```bash
docker-compose up -d qdrant
# Wait 10 seconds for startup
docker ps | grep qdrant
```

### "Embedding model download failed"
The first run downloads ~2GB bge-m3 model. Ensure good internet connection.

### "Too slow"
Use `--max-items` to limit ingestion:
```bash
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --max-items 5000
```

---

## Next Steps

After ingesting data:

1. **Start the backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Start the frontend:**
```bash
cd frontend
npm run dev
```

3. **Test RAG retrieval:**
The ingested data will be used by the chat service to provide contextual Telugu learning content.

---

## Data Usage in the Application

The ingested data is used for:

1. **RAG (Retrieval-Augmented Generation):** When learners ask questions or practice, the system searches the vector database for relevant Telugu content
2. **Example sentences:** Providing context-appropriate examples based on learner's domain preferences
3. **Vocabulary building:** Suggesting new words based on learner's level
4. **Grammar explanations:** Retrieving relevant grammar patterns and examples
5. **Domain-specific content:** Filtering content by office, family, travel, or movies domains

The more data you ingest, the better the AI tutor's responses will be!
