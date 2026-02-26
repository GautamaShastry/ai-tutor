"""
Script to download Telugu learning data from open sources.

Sources:
- Tatoeba: Telugu-English sentence pairs
- Dakshina: Transliteration data

Usage:
    python -m scripts.download_data --source tatoeba
    python -m scripts.download_data --source all
"""
import asyncio
import argparse
import httpx
import tarfile
import zipfile
import csv
import json
from pathlib import Path
import sys

DATA_DIR = Path(__file__).parent.parent / "data"


async def download_tatoeba():
    """
    Download Telugu sentences from Tatoeba.
    Creates a pre-filtered Telugu-English pairs file.
    """
    print("=== Downloading Tatoeba Telugu Data ===")
    
    tatoeba_dir = DATA_DIR / "tatoeba"
    tatoeba_dir.mkdir(parents=True, exist_ok=True)
    
    # Tatoeba download URLs
    sentences_url = "https://downloads.tatoeba.org/exports/sentences.tar.bz2"
    links_url = "https://downloads.tatoeba.org/exports/links.tar.bz2"
    
    # Alternative: Use the per-language files (smaller)
    tel_sentences_url = "https://downloads.tatoeba.org/exports/per_language/tel/tel_sentences.tsv.bz2"
    eng_sentences_url = "https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2"
    
    print("Note: Full Tatoeba download is large (~1GB compressed)")
    print("Using per-language files instead for Telugu and English...")
    
    async with httpx.AsyncClient(timeout=300.0, follow_redirects=True) as client:
        # Download Telugu sentences
        print("\nDownloading Telugu sentences...")
        tel_file = tatoeba_dir / "tel_sentences.tsv.bz2"
        
        try:
            response = await client.get(tel_sentences_url)
            response.raise_for_status()
            tel_file.write_bytes(response.content)
            print(f"  Saved: {tel_file}")
        except Exception as e:
            print(f"  Error downloading Telugu sentences: {e}")
            print("  Falling back to manual extraction instructions...")
            print_manual_instructions()
            return
        
        # Download English sentences  
        print("Downloading English sentences (this is large, ~200MB)...")
        eng_file = tatoeba_dir / "eng_sentences.tsv.bz2"
        
        try:
            response = await client.get(eng_sentences_url)
            response.raise_for_status()
            eng_file.write_bytes(response.content)
            print(f"  Saved: {eng_file}")
        except Exception as e:
            print(f"  Error downloading English sentences: {e}")
            return
        
        # Download links
        print("Downloading sentence links...")
        try:
            response = await client.get(links_url)
            response.raise_for_status()
            links_file = tatoeba_dir / "links.tar.bz2"
            links_file.write_bytes(response.content)
            print(f"  Saved: {links_file}")
        except Exception as e:
            print(f"  Error downloading links: {e}")
            return
    
    # Extract and process
    print("\nExtracting files...")
    import bz2
    
    # Extract Telugu sentences
    with bz2.open(tel_file, "rt", encoding="utf-8") as f:
        tel_sentences = {}
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                tel_sentences[parts[0]] = parts[2]
    print(f"  Telugu sentences: {len(tel_sentences)}")
    
    # Extract English sentences
    with bz2.open(eng_file, "rt", encoding="utf-8") as f:
        eng_sentences = {}
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                eng_sentences[parts[0]] = parts[2]
    print(f"  English sentences: {len(eng_sentences)}")
    
    # Extract links
    with tarfile.open(tatoeba_dir / "links.tar.bz2", "r:bz2") as tar:
        tar.extractall(tatoeba_dir)
    
    # Find Telugu-English pairs
    print("\nFinding Telugu-English pairs...")
    pairs = []
    links_file = tatoeba_dir / "links.csv"
    
    with open(links_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                id1, id2 = parts[0], parts[1]
                
                # Check if this is a Telugu-English pair
                if id1 in tel_sentences and id2 in eng_sentences:
                    pairs.append((tel_sentences[id1], eng_sentences[id2]))
                elif id2 in tel_sentences and id1 in eng_sentences:
                    pairs.append((tel_sentences[id2], eng_sentences[id1]))
    
    print(f"  Found {len(pairs)} Telugu-English pairs")
    
    # Save pairs
    output_file = tatoeba_dir / "telugu_english_pairs.tsv"
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["telugu", "english"])
        for tel, eng in pairs:
            writer.writerow([tel, eng])
    
    print(f"\nSaved to: {output_file}")
    print(f"Total pairs: {len(pairs)}")
    
    # Cleanup large files
    print("\nCleaning up temporary files...")
    (tatoeba_dir / "tel_sentences.tsv.bz2").unlink(missing_ok=True)
    (tatoeba_dir / "eng_sentences.tsv.bz2").unlink(missing_ok=True)
    (tatoeba_dir / "links.tar.bz2").unlink(missing_ok=True)
    (tatoeba_dir / "links.csv").unlink(missing_ok=True)


def print_manual_instructions():
    """Print manual download instructions"""
    print("""
=== Manual Download Instructions ===

1. Tatoeba (Telugu-English sentences):
   - Go to: https://tatoeba.org/en/downloads
   - Download: sentences.tar.bz2 and links.tar.bz2
   - Extract and filter for Telugu (tel) and English (eng)
   - Or use their sentence search: https://tatoeba.org/en/sentences/search?from=tel&to=eng

2. AI4Bharat Samanantar (Parallel corpus):
   - Go to: https://indicnlp.ai4bharat.org/samanantar/
   - Download the Telugu-English parallel data
   - Place in: backend/data/samanantar/

3. Dakshina (Transliteration):
   - Go to: https://github.com/google-research-datasets/dakshina
   - Download Telugu data
   - Place in: backend/data/dakshina/

4. Aksharantar (Transliteration pairs):
   - Go to: https://github.com/AI4Bharat/IndicXlit
   - Download Telugu transliteration data
   - Place in: backend/data/aksharantar/
""")


async def download_samanantar_sample():
    """
    Download a sample from AI4Bharat Samanantar.
    Full dataset requires manual download due to size.
    """
    print("=== AI4Bharat Samanantar ===")
    
    samanantar_dir = DATA_DIR / "samanantar"
    samanantar_dir.mkdir(parents=True, exist_ok=True)
    
    # Try to download from HuggingFace (smaller sample)
    print("Attempting to download Samanantar sample from HuggingFace...")
    
    # The full dataset is on HuggingFace: ai4bharat/samanantar
    # We'll provide instructions for manual download
    
    readme_content = """AI4Bharat Samanantar Telugu-English Parallel Corpus

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
        f.write(f\"{item['tgt']}\\t{item['src']}\\n\")
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
"""
    
    readme = samanantar_dir / "README.txt"
    readme.write_text(readme_content)
    print(f"Created: {readme}")
    
    # Try to create a small sample using HuggingFace datasets
    try:
        print("\nAttempting to download sample via HuggingFace datasets...")
        from datasets import load_dataset
        
        print("Loading dataset (this may take a few minutes)...")
        ds = load_dataset('ai4bharat/samanantar', 'te', split='train', streaming=True)
        
        # Get first 5000 samples
        sample_file = samanantar_dir / "samanantar_te_en.tsv"
        count = 0
        max_samples = 5000
        
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("english\ttelugu\n")
            for item in ds:
                if count >= max_samples:
                    break
                english = item.get('tgt', '').strip()
                telugu = item.get('src', '').strip()
                if english and telugu:
                    f.write(f"{english}\t{telugu}\n")
                    count += 1
                if count % 1000 == 0:
                    print(f"  Downloaded {count} samples...")
        
        print(f"\nSaved {count} samples to: {sample_file}")
        
    except ImportError:
        print("\nNote: Install 'datasets' package for automatic download:")
        print("  pip install datasets")
        print("\nOr follow manual download instructions in README.txt")
    except Exception as e:
        print(f"\nCould not auto-download: {e}")
        print("Please follow manual download instructions in README.txt")


async def create_expanded_sample():
    """Create an expanded sample dataset with more content"""
    print("=== Creating Expanded Sample Data ===")
    
    sample_dir = DATA_DIR / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # More comprehensive vocabulary
    vocabulary = {
        "content": [
            # Numbers
            {"type": "vocabulary", "telugu": "ఒకటి", "english": "one", "transliteration": "okaṭi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "రెండు", "english": "two", "transliteration": "reṇḍu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "మూడు", "english": "three", "transliteration": "mūḍu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "నాలుగు", "english": "four", "transliteration": "nālugu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఐదు", "english": "five", "transliteration": "aidu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఆరు", "english": "six", "transliteration": "āru", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఏడు", "english": "seven", "transliteration": "ēḍu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఎనిమిది", "english": "eight", "transliteration": "enimidi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "తొమ్మిది", "english": "nine", "transliteration": "tommidi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "పది", "english": "ten", "transliteration": "padi", "difficulty": "beginner", "domains": ["general"]},
            
            # Colors
            {"type": "vocabulary", "telugu": "ఎరుపు", "english": "red", "transliteration": "erupu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "నీలం", "english": "blue", "transliteration": "nīlaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "పచ్చ", "english": "green", "transliteration": "pacca", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "పసుపు", "english": "yellow", "transliteration": "pasupu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "తెలుపు", "english": "white", "transliteration": "telupu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "నలుపు", "english": "black", "transliteration": "nalupu", "difficulty": "beginner", "domains": ["general"]},
            
            # Body parts
            {"type": "vocabulary", "telugu": "తల", "english": "head", "transliteration": "tala", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "కన్ను", "english": "eye", "transliteration": "kannu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ముక్కు", "english": "nose", "transliteration": "mukku", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "నోరు", "english": "mouth", "transliteration": "nōru", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "చెవి", "english": "ear", "transliteration": "cevi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "చేయి", "english": "hand", "transliteration": "cēyi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "కాలు", "english": "leg/foot", "transliteration": "kālu", "difficulty": "beginner", "domains": ["general"]},
            
            # Food
            {"type": "vocabulary", "telugu": "పాలు", "english": "milk", "transliteration": "pālu", "difficulty": "beginner", "domains": ["general", "family"]},
            {"type": "vocabulary", "telugu": "పండు", "english": "fruit", "transliteration": "paṇḍu", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "కూర", "english": "vegetable/curry", "transliteration": "kūra", "difficulty": "beginner", "domains": ["general", "family"]},
            {"type": "vocabulary", "telugu": "చపాతి", "english": "chapati/roti", "transliteration": "capāti", "difficulty": "beginner", "domains": ["general", "family"]},
            {"type": "vocabulary", "telugu": "సాంబార్", "english": "sambar", "transliteration": "sāmbār", "difficulty": "beginner", "domains": ["general", "family"]},
            {"type": "vocabulary", "telugu": "పప్పు", "english": "dal/lentils", "transliteration": "pappu", "difficulty": "beginner", "domains": ["general", "family"]},
            {"type": "vocabulary", "telugu": "పెరుగు", "english": "curd/yogurt", "transliteration": "perugu", "difficulty": "beginner", "domains": ["general", "family"]},
            
            # Common verbs
            {"type": "vocabulary", "telugu": "తినడం", "english": "to eat", "transliteration": "tinaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "తాగడం", "english": "to drink", "transliteration": "tāgaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "వెళ్ళడం", "english": "to go", "transliteration": "veḷḷaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "రావడం", "english": "to come", "transliteration": "rāvaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "చూడడం", "english": "to see", "transliteration": "cūḍaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "వినడం", "english": "to hear", "transliteration": "vinaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "చెప్పడం", "english": "to say/tell", "transliteration": "ceppaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "చేయడం", "english": "to do/make", "transliteration": "cēyaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఇవ్వడం", "english": "to give", "transliteration": "ivvaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "తీసుకోవడం", "english": "to take", "transliteration": "tīsukōvaḍaṁ", "difficulty": "beginner", "domains": ["general"]},
            
            # Places
            {"type": "vocabulary", "telugu": "బడి", "english": "school", "transliteration": "baḍi", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "ఆసుపత్రి", "english": "hospital", "transliteration": "āsupatri", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "దుకాణం", "english": "shop", "transliteration": "dukāṇaṁ", "difficulty": "beginner", "domains": ["general"]},
            {"type": "vocabulary", "telugu": "బస్సు స్టాండ్", "english": "bus stand", "transliteration": "bassu sṭāṇḍ", "difficulty": "beginner", "domains": ["general", "travel"]},
            {"type": "vocabulary", "telugu": "రైల్వే స్టేషన్", "english": "railway station", "transliteration": "railwē sṭēṣan", "difficulty": "beginner", "domains": ["general", "travel"]},
        ]
    }
    
    # More sentences
    sentences = {
        "content": [
            # Daily activities
            {"type": "sentence", "telugu": "నేను ఉదయం ఆరు గంటలకు లేస్తాను", "english": "I wake up at 6 AM", "transliteration": "nēnu udayaṁ āru gaṇṭalaku lēstānu", "difficulty": "intermediate", "domains": ["general"]},
            {"type": "sentence", "telugu": "నేను రోజూ వ్యాయామం చేస్తాను", "english": "I exercise every day", "transliteration": "nēnu rōjū vyāyāmaṁ cēstānu", "difficulty": "intermediate", "domains": ["general"]},
            {"type": "sentence", "telugu": "అమ్మ టిఫిన్ చేసింది", "english": "Mother made breakfast", "transliteration": "amma ṭiphin cēsindi", "difficulty": "intermediate", "domains": ["family"]},
            {"type": "sentence", "telugu": "నేను బస్సులో ఆఫీసుకు వెళ్తాను", "english": "I go to office by bus", "transliteration": "nēnu bassulō āphīsuku veḷtānu", "difficulty": "intermediate", "domains": ["office", "travel"]},
            {"type": "sentence", "telugu": "సాయంత్రం ఇంటికి వస్తాను", "english": "I come home in the evening", "transliteration": "sāyantraṁ iṇṭiki vastānu", "difficulty": "intermediate", "domains": ["general"]},
            
            # Questions
            {"type": "sentence", "telugu": "ఇది ఎంత?", "english": "How much is this?", "transliteration": "idi enta?", "difficulty": "beginner", "domains": ["general", "travel"]},
            {"type": "sentence", "telugu": "బాత్రూమ్ ఎక్కడ ఉంది?", "english": "Where is the bathroom?", "transliteration": "bāthrūm ekkaḍa undi?", "difficulty": "beginner", "domains": ["general", "travel"]},
            {"type": "sentence", "telugu": "మీకు తెలుగు వచ్చా?", "english": "Do you know Telugu?", "transliteration": "mīku telugu vaccā?", "difficulty": "beginner", "domains": ["general"]},
            {"type": "sentence", "telugu": "ఈ రోజు ఏం చేస్తున్నావు?", "english": "What are you doing today?", "transliteration": "ī rōju ēṁ cēstunnāvu?", "difficulty": "intermediate", "domains": ["general"]},
            {"type": "sentence", "telugu": "భోజనం అయిందా?", "english": "Have you eaten?", "transliteration": "bhōjanaṁ ayindā?", "difficulty": "beginner", "domains": ["general", "family"]},
            
            # Travel
            {"type": "sentence", "telugu": "హైదరాబాద్ వెళ్ళే బస్సు ఎక్కడ?", "english": "Where is the bus to Hyderabad?", "transliteration": "haidarābād veḷḷē bassu ekkaḍa?", "difficulty": "intermediate", "domains": ["travel"]},
            {"type": "sentence", "telugu": "టికెట్ ఎంత?", "english": "How much is the ticket?", "transliteration": "ṭikeṭ enta?", "difficulty": "beginner", "domains": ["travel"]},
            {"type": "sentence", "telugu": "ఈ రైలు విజయవాడ వెళ్తుందా?", "english": "Does this train go to Vijayawada?", "transliteration": "ī railu vijayavāḍa veḷtundā?", "difficulty": "intermediate", "domains": ["travel"]},
            {"type": "sentence", "telugu": "దయచేసి నన్ను ఇక్కడ దింపండి", "english": "Please drop me here", "transliteration": "dayacēsi nannu ikkaḍa dimpaṇḍi", "difficulty": "intermediate", "domains": ["travel"]},
            
            # Movies/Entertainment
            {"type": "sentence", "telugu": "ఈ సినిమా చాలా బాగుంది", "english": "This movie is very good", "transliteration": "ī sinimā cālā bāgundi", "difficulty": "intermediate", "domains": ["movies"]},
            {"type": "sentence", "telugu": "మీకు ఏ పాట ఇష్టం?", "english": "Which song do you like?", "transliteration": "mīku ē pāṭa iṣṭaṁ?", "difficulty": "intermediate", "domains": ["movies"]},
            {"type": "sentence", "telugu": "ఈ హీరో చాలా బాగా నటించాడు", "english": "This hero acted very well", "transliteration": "ī hīrō cālā bāgā naṭincāḍu", "difficulty": "intermediate", "domains": ["movies"]},
            
            # Polite expressions
            {"type": "sentence", "telugu": "మీ సహాయం కావాలి", "english": "I need your help", "transliteration": "mī sahāyaṁ kāvāli", "difficulty": "intermediate", "domains": ["general", "office"]},
            {"type": "sentence", "telugu": "ఒక్క నిమిషం ఆగండి", "english": "Please wait a minute", "transliteration": "okka nimiṣaṁ āgaṇḍi", "difficulty": "intermediate", "domains": ["general"]},
            {"type": "sentence", "telugu": "మీతో మాట్లాడవచ్చా?", "english": "May I speak with you?", "transliteration": "mītō māṭlāḍavaccā?", "difficulty": "intermediate", "domains": ["general", "office"]},
            {"type": "sentence", "telugu": "నాకు అర్థం కాలేదు", "english": "I didn't understand", "transliteration": "nāku arthaṁ kālēdu", "difficulty": "intermediate", "domains": ["general"]},
            {"type": "sentence", "telugu": "దయచేసి మళ్ళీ చెప్పండి", "english": "Please say it again", "transliteration": "dayacēsi maḷḷī ceppaṇḍi", "difficulty": "intermediate", "domains": ["general"]},
        ]
    }
    
    # Save expanded vocabulary
    vocab_file = sample_dir / "vocabulary_expanded.json"
    with open(vocab_file, "w", encoding="utf-8") as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    print(f"Created: {vocab_file} ({len(vocabulary['content'])} items)")
    
    # Save expanded sentences
    sentences_file = sample_dir / "sentences_expanded.json"
    with open(sentences_file, "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)
    print(f"Created: {sentences_file} ({len(sentences['content'])} items)")
    
    print(f"\nTotal new items: {len(vocabulary['content']) + len(sentences['content'])}")


async def main():
    parser = argparse.ArgumentParser(description="Download Telugu learning data")
    parser.add_argument(
        "--source",
        type=str,
        default="sample",
        choices=["tatoeba", "samanantar", "sample", "all"],
        help="Data source to download",
    )
    
    args = parser.parse_args()
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.source == "tatoeba" or args.source == "all":
        await download_tatoeba()
    
    if args.source == "samanantar" or args.source == "all":
        await download_samanantar_sample()
    
    if args.source == "sample" or args.source == "all":
        await create_expanded_sample()
    
    print("\n=== Download Complete ===")
    print(f"Data directory: {DATA_DIR}")
    print("\nTo ingest data, run:")
    print("  python -m scripts.ingest_data --source custom --path ./data/sample --dry-run")


if __name__ == "__main__":
    asyncio.run(main())
