from googletrans import Translator as GoogleTranslator
from typing import List, Optional
import asyncio

class NLPTranslator:
    def __init__(self):
        self.translator = GoogleTranslator()
    
    async def translate(self, text: str, dest_lang: str = 'en', src_lang: Optional[str] = None) -> str:
        """Translate text to target language"""
        try:
            result = await self.translator.translate(text, dest=dest_lang, src=src_lang)
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    async def translate_batch(self, texts: List[str], dest_lang: str = 'en') -> List[str]:
        """Translate multiple texts"""
        tasks = [self.translate(text, dest_lang) for text in texts]
        return await asyncio.gather(*tasks)
    
    def detect_source_language(self, text: str) -> str:
        """Detect source language"""
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except:
            return 'unknown'