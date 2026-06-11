import random
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
from typing import List

class DataAugmenter:
    def __init__(self):
        self.synonym_aug = naw.SynonymAug(aug_src='wordnet')
        self.random_swap_aug = naw.RandomWordAug(action="swap")
        self.back_translation_aug = naw.BackTranslationAug(
            from_model_name='facebook/wmt19-en-de',
            to_model_name='facebook/wmt19-de-en'
        )
    
    def augment_synonym(self, text: str, n: int = 3) -> List[str]:
        """Generate synonym-augmented versions"""
        augmented = []
        for _ in range(n):
            aug_text = self.synonym_aug.augment(text)
            augmented.append(aug_text)
        return augmented
    
    def augment_swap(self, text: str, n: int = 3) -> List[str]:
        """Generate word-swapped versions"""
        augmented = []
        for _ in range(n):
            aug_text = self.random_swap_aug.augment(text)
            augmented.append(aug_text)
        return augmented
    
    def augment_back_translation(self, text: str, n: int = 2) -> List[str]:
        """Generate back-translated versions"""
        augmented = []
        for _ in range(n):
            aug_text = self.back_translation_aug.augment(text)
            augmented.append(aug_text)
        return augmented
    
    def augment_all(self, text: str) -> List[str]:
        """Apply all augmentation techniques"""
        augmented = [text]
        augmented.extend(self.augment_synonym(text, 2))
        augmented.extend(self.augment_swap(text, 2))
        return augmented[:10]  # Limit to 10 versions