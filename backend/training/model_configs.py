MODEL_CONFIGS = {
    'sentiment_xlm_roberta': {
        'model_name': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
        'num_labels': 3,
        'learning_rate': 2e-5,
        'batch_size': 32,
        'epochs': 5,
        'warmup_ratio': 0.1,
        'weight_decay': 0.01,
        'max_length': 512,
        'gradient_accumulation_steps': 2,
        'use_mixed_precision': True
    },
    'sentiment_distilbert': {
        'model_name': 'distilbert-base-uncased',
        'num_labels': 3,
        'learning_rate': 3e-5,
        'batch_size': 64,
        'epochs': 3,
        'warmup_ratio': 0.1,
        'weight_decay': 0.01,
        'max_length': 512,
        'gradient_accumulation_steps': 1,
        'use_mixed_precision': True
    },
    'emotion_distilbert': {
        'model_name': 'bhadresh-savani/distilbert-base-uncased-emotion',
        'num_labels': 6,
        'learning_rate': 2e-5,
        'batch_size': 32,
        'epochs': 10,
        'warmup_ratio': 0.1,
        'weight_decay': 0.01,
        'max_length': 512,
        'gradient_accumulation_steps': 2,
        'use_mixed_precision': True
    }
}