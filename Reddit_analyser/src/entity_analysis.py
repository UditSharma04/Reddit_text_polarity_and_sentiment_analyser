import spacy
import textstat

class EntityAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        try:
            doc = self.nlp(text)
            
            entities = {
                'PERSON': [],
                'ORG': [],
                'GPE': [],
                'PRODUCT': [],
                'DATE': []
            }
            
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_].append(ent.text)
                    
            return entities
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            return {}

    @staticmethod
    def analyze_readability(text):
        try:
            return {
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
                'automated_readability_index': textstat.automated_readability_index(text),
                'coleman_liau_index': textstat.coleman_liau_index(text)
            }
        except Exception as e:
            print(f"Error in readability analysis: {e}")
            return {} 