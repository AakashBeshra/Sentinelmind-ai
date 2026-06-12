import re
import unicodedata
from typing import List, Optional

class TextCleaner:
    def __init__(self):
        self.contractions = {
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            "n't": " not",
            "'re": " are",
            "'s": " is",
            "'d": " would",
            "'ll": " will",
            "'ve": " have",
            "'m": " am"
        }
    
    def clean_html(self, text: str) -> str:
        """Remove HTML tags"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        url_pattern = r'http\S+|www\S+|https\S+'
        return re.sub(url_pattern, '', text)
    
    def remove_emojis(self, text: str) -> str:
        """Remove emojis and special characters"""
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    def expand_contractions(self, text: str) -> str:
        """Expand contractions"""
        for contraction, expansion in self.contractions.items():
            text = text.replace(contraction, expansion)
        return text
    
    def normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters"""
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    def remove_special_chars(self, text: str, keep_spaces: bool = True) -> str:
        """Remove special characters"""
        if keep_spaces:
            pattern = r'[^a-zA-Z0-9\s]'
        else:
            pattern = r'[^a-zA-Z0-9]'
        return re.sub(pattern, '', text)
    
    def clean_pipeline(self, text: str) -> str:
        """Complete cleaning pipeline"""
        text = self.clean_html(text)
        text = self.remove_urls(text)
        text = self.expand_contractions(text)
        text = self.remove_emojis(text)
        text = self.normalize_unicode(text)
        text = self.remove_special_chars(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text