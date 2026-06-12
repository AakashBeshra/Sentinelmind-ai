from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import torch

class EmbeddingGenerator:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts"""
        emb1 = self.model.encode(text1)
        emb2 = self.model.encode(text2)
        
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)
    
    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[tuple]:
        """Find most similar texts to query"""
        query_emb = self.model.encode(query)
        candidate_embs = self.model.encode(candidates)
        
        similarities = np.dot(candidate_embs, query_emb) / (
            np.linalg.norm(candidate_embs, axis=1) * np.linalg.norm(query_emb)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return [(candidates[i], float(similarities[i])) for i in top_indices]