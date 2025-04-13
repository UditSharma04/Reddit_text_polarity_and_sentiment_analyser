from nltk.corpus import stopwords
import string
from collections import Counter
from gensim import corpora, models
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config.config import NLTK_DATA_DIR
import nltk

class TextAnalyzer:
    def __init__(self):
        # Ensure NLTK uses the correct data path
        nltk.data.path.insert(0, NLTK_DATA_DIR)
        
    @staticmethod
    def extract_keywords(query, top_n=5):
        try:
            words = query.lower().split()
            unique_words = list(set([word for word in words if len(word) > 2]))
            return unique_words[:top_n]
        except Exception as e:
            print(f"Warning: Using simple keyword extraction due to error: {e}")
            return [query]

    def extract_top_keywords(self, text, top_n=50):
        try:
            translator = str.maketrans('', '', string.punctuation)
            text = text.lower().translate(translator)
            words = text.split()
            
            # Make sure stopwords are loaded from the correct path
            try:
                stop_words = set(stopwords.words('english'))
            except LookupError:
                nltk.download('stopwords', download_dir=NLTK_DATA_DIR)
                stop_words = set(stopwords.words('english'))
            
            words = [word for word in words 
                    if word not in stop_words 
                    and len(word) > 2
                    and not word.isdigit()]
            
            word_freq = Counter(words)
            return [(count, word) for word, count in word_freq.most_common(top_n)]
        except Exception as e:
            print(f"Error extracting top keywords: {e}")
            return []

    @staticmethod
    def perform_topic_analysis(texts, num_topics=5):
        try:
            processed_texts = [
                [word.lower() for word in text.split() 
                 if word.isalnum() and len(word) > 2]
                for text in texts
            ]
            
            dictionary = corpora.Dictionary(processed_texts)
            corpus = [dictionary.doc2bow(text) for text in processed_texts]
            
            lda_model = models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=num_topics,
                random_state=42,
                passes=10
            )
            
            topics = []
            for idx, topic in lda_model.print_topics(-1):
                topics.append(f"Topic {idx+1}: {topic}")
            
            return topics
        except Exception as e:
            print(f"Error in topic analysis: {e}")
            return [] 