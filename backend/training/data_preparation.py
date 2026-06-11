import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
import json
from pathlib import Path
import random
from typing import List, Dict, Tuple
import re

class DataPreparator:
    def __init__(self, model_name: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def load_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load multiple sentiment datasets"""
        datasets = {}
        
        # You would load actual datasets here
        # For demonstration, creating structure
        
        # Example: Twitter Sentiment
        # datasets['twitter'] = pd.read_csv('path/to/twitter_sentiment.csv')
        
        # Example: Amazon Reviews
        # datasets['amazon'] = pd.read_csv('path/to/amazon_reviews.csv')
        
        # Example: IMDB Reviews
        # datasets['imdb'] = pd.read_csv('path/to/imdb_reviews.csv')
        
        return datasets
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def balance_dataset(self, df: pd.DataFrame, label_col: str, target_size: int = None) -> pd.DataFrame:
        """Balance dataset by undersampling majority classes"""
        label_counts = df[label_col].value_counts()
        min_count = label_counts.min()
        
        if target_size:
            min_count = min(min_count, target_size)
        
        balanced_dfs = []
        for label in label_counts.index:
            label_df = df[df[label_col] == label]
            if len(label_df) > min_count:
                label_df = label_df.sample(n=min_count, random_state=42)
            balanced_dfs.append(label_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return balanced_df
    
    def augment_text(self, text: str, augmentation_type: str = "random") -> str:
        """Augment text data for training"""
        if augmentation_type == "random":
            # Random synonym replacement
            # This would use NLTK or similar
            return text
        elif augmentation_type == "back_translation":
            # Back translation augmentation
            # Would use translation APIs
            return text
        else:
            return text
    
    def prepare_for_training(self, df: pd.DataFrame, text_col: str, label_col: str, 
                             test_size: float = 0.2, val_size: float = 0.1) -> Tuple:
        """Prepare data for training"""
        # Clean texts
        df['cleaned_text'] = df[text_col].apply(self.clean_text)
        
        # Remove empty texts
        df = df[df['cleaned_text'].str.len() > 0]
        
        # Balance dataset
        df = self.balance_dataset(df, label_col)
        
        # Split data
        train_val, test = train_test_split(df, test_size=test_size, random_state=42, stratify=df[label_col])
        train, val = train_test_split(train_val, test_size=val_size/(1-test_size), random_state=42, stratify=train_val[label_col])
        
        return train, val, test
    
    def save_prepared_data(self, train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, output_dir: str):
        """Save prepared datasets"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        train.to_csv(output_path / 'train.csv', index=False)
        val.to_csv(output_path / 'val.csv', index=False)
        test.to_csv(output_path / 'test.csv', index=False)
        
        # Save metadata
        metadata = {
            'train_size': len(train),
            'val_size': len(val),
            'test_size': len(test),
            'label_distribution': {
                'train': train['label'].value_counts().to_dict(),
                'val': val['label'].value_counts().to_dict(),
                'test': test['label'].value_counts().to_dict()
            }
        }
        
        with open(output_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Data saved to {output_dir}")
        print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

def main():
    preparator = DataPreparator()
    
    # Load datasets
    datasets = preparator.load_datasets()
    
    # Combine datasets
    combined_df = pd.concat(datasets.values(), ignore_index=True)
    
    # Prepare data
    train, val, test = preparator.prepare_for_training(
        combined_df,
        text_col='text',
        label_col='sentiment_label'
    )
    
    # Save prepared data
    preparator.save_prepared_data(train, val, test, '../data/processed')

if __name__ == "__main__":
    main()