AI4Bharat Samanantar Telugu-English Parallel Corpus

This is one of the largest publicly available parallel corpora for Indian languages.
Telugu-English contains ~150,000+ sentence pairs.

=== DOWNLOAD OPTIONS ===

Option 1: HuggingFace (Recommended)
-----------------------------------
pip install datasets
python -c "
from datasets import load_dataset
ds = load_dataset('ai4bharat/samanantar', 'te', split='train')
# Save to TSV
with open('samanantar_te_en.tsv', 'w', encoding='utf-8') as f:
    for item in ds:
        f.write(f"{item['tgt']}\t{item['src']}\n")
"

Option 2: Direct Download
-------------------------
1. Go to: https://indicnlp.ai4bharat.org/samanantar/
2. Download the en-te (English-Telugu) parallel data
3. Extract files here

Option 3: OPUS (Alternative source)
-----------------------------------
1. Go to: https://opus.nlpl.eu/
2. Search for Telugu-English corpora
3. Download WikiMatrix, CCAligned, or OpenSubtitles

=== EXPECTED FILE FORMATS ===

Format A: TSV file
  samanantar_te_en.tsv with columns: english<TAB>telugu

Format B: Parallel text files
  train.en (one English sentence per line)
  train.te (one Telugu sentence per line)

=== USAGE ===

# Preview data (dry run)
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --dry-run

# Ingest first 10,000 items
python -m scripts.ingest_data --source samanantar --path ./data/samanantar --max-items 10000

# Ingest all
python -m scripts.ingest_data --source samanantar --path ./data/samanantar

License: CC0 (Public Domain)
