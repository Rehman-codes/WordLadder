import requests
import os
import nltk
from nltk.corpus import words

# Download NLTK words dataset (only needed once)
nltk.download("words")

# Load the standard English word list from NLTK
valid_words = set(words.words())

# URL of a large English word list (from GitHub)
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

# Define folder paths (relative to `utilities/`)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory
DICTIONARY_DIR = os.path.join(BASE_DIR, "dictionary")  # Path to dictionary folder

# Ensure the dictionary folder exists
os.makedirs(DICTIONARY_DIR, exist_ok=True)

# Define file paths
EASY_FILE = os.path.join(DICTIONARY_DIR, "easy.txt")
MEDIUM_FILE = os.path.join(DICTIONARY_DIR, "medium.txt")
HARD_FILE = os.path.join(DICTIONARY_DIR, "hard.txt")

# Download the word list
print("Downloading word list...")
response = requests.get(WORD_LIST_URL)
all_words = response.text.splitlines()  # Convert text into a list of words

# Filter valid words (only alphabetic & present in NLTK dictionary)
def is_valid(word):
    return word.isalpha() and word in valid_words

filtered_words = [word.lower() for word in all_words if is_valid(word)]

# Categorize words based on new length rules
easy_words = [word for word in filtered_words if len(word) == 3]  # Only 3-letter words
medium_words = [word for word in filtered_words if len(word) == 4]  # Only 4-letter words
hard_words = [word for word in filtered_words if len(word) == 5]  # Only 5-letter words

# Save words to respective files
def save_words(filename, word_list):
    with open(filename, "w") as f:
        for word in sorted(word_list):  # Sorting for easier debugging
            f.write(word + "\n")

save_words(EASY_FILE, easy_words)
save_words(MEDIUM_FILE, medium_words)
save_words(HARD_FILE, hard_words)

print(f"Word dictionaries updated with new rules in: {DICTIONARY_DIR}")
