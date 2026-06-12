import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Dict, List, Optional
import tempfile
import os
import aiofiles

class OCRService:
    def __init__(self):
        # Configure tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        pass
    
    async def extract_text(self, image_path: str, language: str = "eng") -> Dict:
        """Extract text from image using Tesseract OCR"""
        # Load image
        image = cv2.imread(image_path)
        
        if image is None:
            return {"error": "Failed to load image", "text": ""}
        
        # Preprocess image for better OCR
        processed_image = self._preprocess_image(image)
        
        # Perform OCR
        custom_config = f'--oem 3 --psm 6 -l {language}'
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Get detailed data
        data = pytesseract.image_to_data(processed_image, config=custom_config, output_type=pytesseract.Output.DICT)
        
        # Calculate confidence
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        avg_confidence = np.mean(confidences) if confidences else 0
        
        # Detect language
        detected_language = await self._detect_language(extracted_text)
        
        # Extract words with positions
        words = []
        for i, word in enumerate(data['text']):
            if word.strip():
                words.append({
                    "word": word,
                    "confidence": int(data['conf'][i]),
                    "bbox": {
                        "x": data['left'][i],
                        "y": data['top'][i],
                        "width": data['width'][i],
                        "height": data['height'][i]
                    }
                })
        
        return {
            "text": extracted_text.strip(),
            "confidence": float(avg_confidence) / 100,
            "language": detected_language,
            "words": words[:50],  # First 50 words
            "word_count": len(words),
            "image_metadata": await self._get_image_metadata(image)
        }
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, h=30)
        
        # Dilate to connect text components
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        
        return dilated
    
    async def _detect_language(self, text: str) -> str:
        """Detect language of extracted text"""
        if not text:
            return "unknown"
        
        try:
            from langdetect import detect
            return detect(text[:200])  # Use first 200 chars
        except:
            return "unknown"
    
    async def _get_image_metadata(self, image: np.ndarray) -> Dict:
        """Extract image metadata"""
        height, width = image.shape[:2]
        
        # Calculate image quality metrics
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Sharpness (Laplacian variance)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Brightness
        brightness = np.mean(gray)
        
        # Contrast
        contrast = np.std(gray)
        
        return {
            "width": width,
            "height": height,
            "sharpness": float(sharpness),
            "brightness": float(brightness),
            "contrast": float(contrast),
            "aspect_ratio": width / height if height > 0 else 0
        }
    
    async def extract_text_batch(self, image_paths: List[str], language: str = "eng") -> List[Dict]:
        """Extract text from multiple images"""
        results = []
        
        for image_path in image_paths:
            result = await self.extract_text(image_path, language)
            results.append(result)
        
        return results
    
    async def extract_text_from_url(self, image_url: str) -> Dict:
        """Download and extract text from image URL"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(await response.read())
                        tmp_path = tmp.name
                    
                    # Process image
                    result = await self.extract_text(tmp_path)
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    return result
                else:
                    return {"error": f"Failed to download image: {response.status}"}
    
    async def extract_handwritten_text(self, image_path: str) -> Dict:
        """Extract handwritten text (using specialized model)"""
        # This would use a handwriting recognition model
        # Simplified version using Tesseract with handwritten config
        
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Failed to load image"}
        
        processed = self._preprocess_image(image)
        
        # Use different config for handwriting
        custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;: '
        text = pytesseract.image_to_string(processed, config=custom_config)
        
        return {
            "text": text.strip(),
            "type": "handwritten",
            "confidence": 0.6  # Handwriting has lower accuracy
        }