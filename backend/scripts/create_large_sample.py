"""
Create a large sample dataset with 1000+ Telugu sentences.
This provides enough data for meaningful learning without external downloads.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "large_sample"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Common Telugu sentences for different scenarios
sentences = [
    # Greetings and basics (50)
    {"telugu": "నమస్కారం", "english": "Hello", "difficulty": "beginner", "domains": ["general"]},
    {"telugu": "శ