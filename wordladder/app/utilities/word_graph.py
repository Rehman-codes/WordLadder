import os
import networkx as nx

# Define folder paths (relative to `app/`)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory
DICTIONARY_DIR = os.path.join(BASE_DIR, "dictionary")  # Path to dictionary folder

# File paths for word lists
WORD_FILES = {
    "easy": os.path.join(DICTIONARY_DIR, "easy.txt"),
    "medium": os.path.join(DICTIONARY_DIR, "medium.txt"),
    "hard": os.path.join(DICTIONARY_DIR, "hard.txt"),
}

def load_words(game_mode):
    """Load words from the appropriate file based on game mode."""
    file_path = WORD_FILES.get(game_mode)
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Dictionary file for {game_mode} mode not found!")

    with open(file_path, "r") as f:
        return set(word.strip() for word in f.readlines())

def is_one_letter_different(word1, word2):
    """Check if two words differ by exactly one letter."""
    if len(word1) != len(word2):
        return False
    return sum(1 for a, b in zip(word1, word2) if a != b) == 1

def build_word_graph(game_mode):
    """Create a graph where words are nodes and edges exist between words differing by one character."""
    words = load_words(game_mode)
    graph = nx.Graph()

    for word in words:
        graph.add_node(word)

    for word1 in words:
        for word2 in words:
            if is_one_letter_different(word1, word2):
                graph.add_edge(word1, word2)

    return graph
