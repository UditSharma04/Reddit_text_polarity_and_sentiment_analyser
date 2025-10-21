import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CONFIG = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_HUB_TOKEN')
NLTK_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nltk_data') 