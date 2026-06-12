import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import AutoTokenizer
from typing import List, Dict
import re

class NLPTokenizer:
    def __init__(self, model_name: str = "xlm-roberta-base"):
        self.nltk_tokenizer = word_tokenize
        self.sent_tokenizer = sent_tokenize
        self.transformer_tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def word_tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        return self.nltk_tokenizer(text)
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """Split text into sentences"""
        return self.sent_tokenizer(text)
    
    def subword_tokenize(self, text: str) -> List[str]:
        """Tokenize using transformer subword tokenizer"""
        tokens = self.transformer_tokenizer.tokenize(text)
        return tokens
    
    def tokenize_with_positions(self, text: str) -> List[Dict]:
        """Tokenize and return positions"""
        tokens = []
        for match in re.finditer(r'\b\w+\b', text):
            tokens.append({
                'token': match.group(),
                'start': match.start(),
                'end': match.end()
            })
        return tokens