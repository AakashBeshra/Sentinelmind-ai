FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/base.txt requirements/ml.txt ./
RUN pip install --no-cache-dir -r base.txt -r ml.txt

# Copy application
COPY . .

# Download models
RUN python -m spacy download en_core_web_sm
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('cardiffnlp/twitter-xlm-roberta-base-sentiment')"

EXPOSE 8000

CMD ["python", "-m", "app.main"]