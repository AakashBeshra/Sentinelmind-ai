import re
import unicodedata
from typing import List, Tuple, Optional, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
from langdetect import detect, DetectorFactory

from app.core.config import settings

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
DetectorFactory.seed = 0

class TextPreprocessor:
    """Advanced text preprocessing pipeline"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.nlp_spacy = spacy.load("en_core_web_sm")
    
    async def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        
        return text
    
    async def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        tokens = word_tokenize(text)
        return tokens
    
    async def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from tokens"""
        return [token for token in tokens if token not in self.stop_words]
    
    async def lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    async def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """Extract named entities using spaCy"""
        doc = self.nlp_spacy(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
    async def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            lang = detect(text)
            return lang
        except:
            return "unknown"
    
    async def preprocess_pipeline(self, text: str, do_lemmatize: bool = True, 
                                 remove_stopwords: bool = True) -> Dict[str, any]:
        """Complete preprocessing pipeline"""
        # Step 1: Clean text
        cleaned = await self.clean_text(text)
        
        # Step 2: Detect language
        language = await self.detect_language(cleaned)
        
        # Step 3: Tokenize
        tokens = await self.tokenize(cleaned)
        
        # Step 4: Remove stopwords (optional)
        if remove_stopwords:
            tokens = await self.remove_stopwords(tokens)
        
        # Step 5: Lemmatize (optional)
        if do_lemmatize:
            tokens = await self.lemmatize(tokens)
        
        # Step 6: Extract entities
        entities = await self.extract_entities(text)
        
        return {
            "original_text": text,
            "cleaned_text": cleaned,
            "language": language,
            "tokens": tokens,
            "entities": entities,
            "token_count": len(tokens)
        }