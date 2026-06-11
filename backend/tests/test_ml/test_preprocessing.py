import pytest
from app.nlp.preprocessor import TextPreprocessor


pytestmark = pytest.mark.asyncio


async def test_text_cleaning():
    """Test text cleaning functionality"""
    preprocessor = TextPreprocessor()
    
    # Test URL removal
    text = "Check this out https://example.com"
    cleaned = await preprocessor.clean_text(text)
    assert "https://" not in cleaned
    
    # Test special character removal
    text = "Hello!!! How are you? @user #hashtag"
    cleaned = await preprocessor.clean_text(text)
    assert "!!!" not in cleaned
    assert "@" not in cleaned
    assert "#" not in cleaned
    
    # Test extra whitespace
    text = "Too    many     spaces"
    cleaned = await preprocessor.clean_text(text)
    assert "    " not in cleaned


async def test_tokenization():
    """Test text tokenization"""
    preprocessor = TextPreprocessor()
    
    text = "This is a test sentence."
    tokens = await preprocessor.tokenize(text)
    
    assert len(tokens) > 0
    assert "test" in tokens


async def test_stopword_removal():
    """Test stopword removal"""
    preprocessor = TextPreprocessor()
    
    tokens = ["this", "is", "a", "test", "sentence"]
    filtered = await preprocessor.remove_stopwords(tokens)
    
    assert "this" not in filtered
    assert "is" not in filtered
    assert "a" not in filtered
    assert "test" in filtered


async def test_lemmatization():
    """Test lemmatization"""
    preprocessor = TextPreprocessor()
    
    tokens = ["running", "better", "mice"]
    lemmatized = await preprocessor.lemmatize(tokens)
    
    assert "running" in lemmatized or "run" in lemmatized


async def test_language_detection():
    """Test language detection"""
    preprocessor = TextPreprocessor()
    
    english = "This is an English sentence"
    lang = await preprocessor.detect_language(english)
    assert lang == "en"
    
    french = "Ceci est une phrase française"
    lang = await preprocessor.detect_language(french)
    assert lang == "fr"


async def test_full_pipeline():
    """Test complete preprocessing pipeline"""
    preprocessor = TextPreprocessor()
    
    text = "I absolutely LOVE this amazing product!!! So happy with my purchase @happy_customer"
    
    result = await preprocessor.preprocess_pipeline(text)
    
    assert "original_text" in result
    assert "cleaned_text" in result
    assert "language" in result
    assert "tokens" in result
    assert "token_count" in result
    assert result["token_count"] > 0