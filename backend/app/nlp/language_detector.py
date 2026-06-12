from langdetect import detect, detect_langs, DetectorFactory
from typing import List, Dict, Optional
import fasttext
import pycld2 as cld2

DetectorFactory.seed = 0

class LanguageDetector:
    def __init__(self):
        # Download fasttext language detection model
        # fasttext.util.download_model('lid.176.ftz')
        self.fasttext_model = None  # Would load actual model
    
    def detect_single(self, text: str) -> str:
        """Detect language of single text"""
        try:
            return detect(text)
        except:
            return "unknown"
    
    def detect_with_confidence(self, text: str) -> List[Dict]:
        """Detect language with confidence scores"""
        try:
            predictions = detect_langs(text)
            return [{
                'language': str(pred).split(':')[0],
                'confidence': float(str(pred).split(':')[1])
            } for pred in predictions]
        except:
            return [{'language': 'unknown', 'confidence': 0.0}]
    
    def detect_cld2(self, text: str) -> Dict:
        """Detect using CLD2 (Compact Language Detector)"""
        is_reliable, text_bytes, details = cld2.detect(text)
        if details:
            return {
                'language': details[0][1],
                'code': details[0][0],
                'confidence': details[0][2] / 100
            }
        return {'language': 'unknown', 'code': 'un', 'confidence': 0.0}
    
    def batch_detect(self, texts: List[str]) -> List[str]:
        """Detect languages for multiple texts"""
        return [self.detect_single(text) for text in texts]