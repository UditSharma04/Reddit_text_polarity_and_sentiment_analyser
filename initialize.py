import nltk
import ssl
import os
from pathlib import Path
from config.config import NLTK_DATA_DIR

def initialize_nltk():
    """Initialize NLTK by downloading required data packages"""
    
    # Create NLTK data directory if it doesn't exist
    os.makedirs(NLTK_DATA_DIR, exist_ok=True)
    
    # Set NLTK data path
    nltk.data.path.insert(0, NLTK_DATA_DIR)
    
    # Handle SSL certificate verification
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # List of required NLTK packages
    required_packages = [
        'punkt',
        'stopwords',
        'averaged_perceptron_tagger',
        'maxent_ne_chunker',
        'words'
    ]

    # Download each package
    for package in required_packages:
        try:
            nltk.download(package, download_dir=NLTK_DATA_DIR)
            print(f"Successfully downloaded {package}")
        except Exception as e:
            print(f"Error downloading {package}: {e}")

if __name__ == "__main__":
    print("Initializing NLTK...")
    initialize_nltk()
    print("NLTK initialization complete!") 