import torch
import onnx
from transformers import XLMRobertaForSequenceClassification

class ONNXExporter:
    def __init__(self, model_path: str, output_path: str):
        self.model_path = model_path
        self.output_path = output_path
    
    def export_sentiment_model(self):
        """Export sentiment model to ONNX format"""
        model = XLMRobertaForSequenceClassification.from_pretrained(self.model_path)
        model.eval()
        
        # Create dummy input
        dummy_input = torch.randint(0, 1000, (1, 128))
        dummy_attention = torch.ones((1, 128))
        
        # Export to ONNX
        torch.onnx.export(
            model,
            (dummy_input, dummy_attention),
            f"{self.output_path}/sentiment_model.onnx",
            input_names=['input_ids', 'attention_mask'],
            output_names=['logits'],
            dynamic_axes={
                'input_ids': {0: 'batch_size', 1: 'sequence_length'},
                'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
                'logits': {0: 'batch_size'}
            },
            opset_version=14
        )
        
        # Verify ONNX model
        onnx_model = onnx.load(f"{self.output_path}/sentiment_model.onnx")
        onnx.checker.check_model(onnx_model)
        
        return f"{self.output_path}/sentiment_model.onnx"