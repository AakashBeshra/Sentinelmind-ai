import spacy
from typing import List, Dict

class NERExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_entities(self, text: str) -> List[Dict]:
        """Extract named entities from text"""
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'label_name': spacy.explain(ent.label_),
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def extract_entities_by_type(self, text: str, entity_type: str) -> List[str]:
        """Extract entities of specific type (PERSON, ORG, GPE, etc.)"""
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ == entity_type]
    
    def get_entity_summary(self, text: str) -> Dict:
        """Get summary of entity types found"""
        doc = self.nlp(text)
        summary = {}
        for ent in doc.ents:
            summary[ent.label_] = summary.get(ent.label_, 0) + 1
        return summary