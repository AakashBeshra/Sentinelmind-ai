import aiofiles
import csv
import json
import pandas as pd
from typing import List, Dict, Any
import PyPDF2
from PIL import Image
import pytesseract
from pathlib import Path
import uuid
import os

from app.services.sentiment_service import SentimentService
from app.core.config import settings
from app.core.redis_client import redis_client

class UploadService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
    
    async def process_csv(self, file_path: str, user_id: int) -> Dict:
        """Process CSV file for batch sentiment analysis"""
        results = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Find text column
            text_column = None
            for col in reader.fieldnames:
                if 'text' in col.lower() or 'content' in col.lower() or 'review' in col.lower():
                    text_column = col
                    break
            
            if not text_column:
                text_column = reader.fieldnames[0] if reader.fieldnames else 'text'
            
            for i, row in enumerate(reader):
                text = row.get(text_column, '')
                if text:
                    analysis = await SentimentService.analyze(text)
                    results.append({
                        "row": i,
                        "text": text[:100],
                        "sentiment": analysis["sentiment"],
                        "confidence": analysis["confidence"]
                    })
        
        return {
            "total_rows": len(results),
            "results": results,
            "file_type": "csv"
        }
    
    async def process_json(self, file_path: str, user_id: int) -> Dict:
        """Process JSON file for batch sentiment analysis"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        
        # Handle different JSON structures
        if isinstance(data, list):
            texts = [item.get('text', item.get('content', str(item))) for item in data]
        elif isinstance(data, dict):
            if 'texts' in data:
                texts = data['texts']
            elif 'data' in data:
                texts = [item.get('text', '') for item in data['data']]
            else:
                texts = list(data.values())
        else:
            texts = [str(data)]
        
        for i, text in enumerate(texts[:100]):  # Limit to 100 items
            if text:
                analysis = await SentimentService.analyze(str(text))
                results.append({
                    "index": i,
                    "sentiment": analysis["sentiment"],
                    "confidence": analysis["confidence"]
                })
        
        return {
            "total_items": len(results),
            "results": results,
            "file_type": "json"
        }
    
    async def process_txt(self, file_path: str, user_id: int) -> Dict:
        """Process text file"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Split into paragraphs or lines
        texts = [t.strip() for t in content.split('\n\n') if t.strip()]
        
        if not texts:
            texts = [content]
        
        results = []
        for i, text in enumerate(texts[:50]):  # Limit to 50 paragraphs
            if text:
                analysis = await SentimentService.analyze(text)
                results.append({
                    "paragraph": i,
                    "text": text[:100],
                    "sentiment": analysis["sentiment"],
                    "confidence": analysis["confidence"]
                })
        
        return {
            "total_paragraphs": len(results),
            "results": results,
            "file_type": "txt"
        }
    
    async def process_pdf(self, file_path: str, user_id: int) -> Dict:
        """Extract and analyze text from PDF"""
        text_content = []
        
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    text_content.append({
                        "page": page_num + 1,
                        "text": text[:500]  # Limit per page
                    })
        
        # Analyze overall document
        full_text = ' '.join([t['text'] for t in text_content])
        analysis = await SentimentService.analyze(full_text[:5000])  # Limit length
        
        return {
            "total_pages": len(text_content),
            "overall_sentiment": analysis,
            "pages": text_content[:10],  # First 10 pages
            "file_type": "pdf"
        }
    
    async def process_image(self, file_path: str, user_id: int) -> Dict:
        """Extract text from image using OCR and analyze"""
        # Open image
        image = Image.open(file_path)
        
        # Extract text with OCR
        extracted_text = pytesseract.image_to_string(image)
        
        if not extracted_text.strip():
            return {
                "error": "No text detected in image",
                "file_type": "image"
            }
        
        # Analyze extracted text
        analysis = await SentimentService.analyze(extracted_text)
        
        return {
            "extracted_text": extracted_text[:500],
            "sentiment": analysis,
            "image_size": image.size,
            "image_format": image.format,
            "file_type": "image"
        }
    
    async def get_processing_status(self, file_id: str, user_id: int) -> Dict:
        """Get status of file processing"""
        status_key = f"upload_status:{file_id}:{user_id}"
        status = await redis_client.get(status_key)
        
        if status:
            return json.loads(status)
        
        return {
            "file_id": file_id,
            "status": "processing",
            "message": "File is being processed"
        }