import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy
from typing import List, Dict

class NLPLemmatizer:
    def __init__(self):
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.spacy_nlp = spacy.load("en_core_web_sm")
    
    def lemmatize_word(self, word: str, pos: str = 'n') -> str:
        """Lemmatize a single word"""
        pos_map = {
            'n': wordnet.NOUN,
            'v': wordnet.VERB,
            'a': wordnet.ADJ,
            'r': wordnet.ADV
        }
        wordnet_pos = pos_map.get(pos, wordnet.NOUN)
        return self.wordnet_lemmatizer.lemmatize(word, wordnet_pos)
    
    def lemmatize_text_spacy(self, text: str) -> List[Dict]:
        """Lemmatize using spaCy with POS tags"""
        doc = self.spacy_nlp(text)
        return [{
            'token': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_
        } for token in doc]
    
    def lemmatize_list(self, tokens: List[str]) -> List[str]:
        """Lemmatize a list of tokens"""
        return [self.lemmatize_word(token) for token in tokens]