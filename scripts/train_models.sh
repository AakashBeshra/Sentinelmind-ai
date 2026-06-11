#!/bin/bash

set -e

echo "Starting model training..."

# Activate virtual environment
source venv/bin/activate

# Create model directories
mkdir -p models/sentiment
mkdir -p models/emotion

# Train sentiment model
echo "Training sentiment analysis model..."
cd backend
python training/train_sentiment.py \
    --epochs 10 \
    --batch_size 32 \
    --learning_rate 2e-5 \
    --output_dir ../models/sentiment

# Train emotion model
echo "Training emotion detection model..."
python training/train_emotion.py \
    --epochs 10 \
    --batch_size 32 \
    --learning_rate 2e-5 \
    --output_dir ../models/emotion

# Evaluate models
echo "Evaluating models..."
python training/evaluator.py --model_path ../models/sentiment --test_data data/test_sentiment.csv
python training/evaluator.py --model_path ../models/emotion --test_data data/test_emotion.csv

echo "Model training complete!"