"""
Simple Samanantar downloader without heavy dependencies.
Downloads directly from HuggingFace using requests.
"""
import requests
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "samanantar"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# HuggingFace dataset API endpoint
API_URL = "https://datasets-server.huggingface.co/rows"
DATASET = "ai4bharat/samanantar"
CONFIG = "te"
SPLIT = "train"

def download_samanantar(max_items=5000):
    """Download Samanantar data via HuggingFace API"""
    print(f"Downloading {max_items} Telugu-English sentence pairs from Samanantar...")
    
    output_file = DATA_DIR / "samanantar_te_en.tsv"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("english\ttelugu\n")
        
        offset = 0
        batch_size = 100
        total_downloaded = 0
        
        while total_downloaded < max_items:
            # Request batch from HuggingFace
            params = {
                "dataset": DATASET,
                "config": CONFIG,
                "split": SPLIT,
                "offset": offset,
                "length": batch_size
            }
            
            try:
                response = requests.get(API_URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                rows = data.get("rows", [])
                if not rows:
                    print(f"\nNo more data available. Downloaded {total_downloaded} items.")
                    break
                
                for row in rows:
                    if total_downloaded >= max_items:
                        break
                    
                    row_data = row.get("row", {})
                    english = row_data.get("tgt", "").strip()
                    telugu = row_data.get("src", "").strip()
                    
                    if english and telugu:
                        f.write(f"{english}\t{telugu}\n")
                        total_downloaded += 1
                
                offset += batch_size
                
                if total_downloaded % 500 == 0:
                    print(f"  Downloaded {total_downloaded} items...")
                
            except Exception as e:
                print(f"\nError downloading batch at offset {offset}: {e}")
                break
    
    print(f"\n✓ Successfully downloaded {total_downloaded} sentence pairs")
    print(f"✓ Saved to: {output_file}")
    return total_downloaded

if __name__ == "__main__":
    import sys
    
    max_items = 5000
    if len(sys.argv) > 1:
        max_items = int(sys.argv[1])
    
    count = download_samanantar(max_items)
    
    if count > 0:
        print("\nTo preview the data:")
        print("  python -m scripts.ingest_data --source samanantar --path ./data/samanantar --dry-run")
        print("\nTo ingest the data:")
        print("  python -m scripts.ingest_data --source samanantar --path ./data/samanantar")
