import os
import time
import requests
from tqdm import tqdm  # Progress bar

# Define folder paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory
DICTIONARY_DIR = os.path.join(BASE_DIR, "dictionary")  # Path to dictionary folder

# File paths
FILES = {
    "easy": os.path.join(DICTIONARY_DIR, "easy.txt"),
    "medium": os.path.join(DICTIONARY_DIR, "medium.txt"),
    "hard": os.path.join(DICTIONARY_DIR, "hard.txt"),
}

# Dictionary API URL
DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"

def is_real_word(word):
    """Check if a word exists using the Dictionary API."""
    response = requests.get(DICTIONARY_API.format(word))
    
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False  # Word not found
    else:
        print(f"⚠️ API Error ({response.status_code}) for word: {word}")
        return False  # Treat as invalid if API fails

def filter_valid_words(filename, level):
    """Reads words from a file, checks validity, and writes back only valid words."""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return
    
    with open(filename, "r") as f:
        words = [word.strip() for word in f.readlines()]

    print(f"\n🔍 Checking {len(words)} words in {os.path.basename(filename)}...")

    valid_words = []
    for word in tqdm(words, desc=f"Processing {level} words", unit="word"):
        if is_real_word(word):
            valid_words.append(word)
        
        time.sleep(0.3)  # Reduced delay to 0.3s

    with open(filename, "w") as f:
        for word in valid_words:
            f.write(word + "\n")

    print(f"✅ {len(valid_words)} valid words saved in {os.path.basename(filename)}\n")

# Run filtering on all word lists
for level, filepath in FILES.items():
    filter_valid_words(filepath, level)

print("🎉 Word filtering complete!")
