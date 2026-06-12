import torch
from transformers import AutoModelForSequenceClassification

class ModelQuantizer:
    def __init__(self, model_path: str):
        self.model_path = model_path
    
    def quantize_dynamic(self, output_path: str):
        """Apply dynamic quantization"""
        model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        
        quantized_model = torch.quantization.quantize_dynamic(
            model, 
            {torch.nn.Linear}, 
            dtype=torch.qint8
        )
        
        torch.save(quantized_model.state_dict(), f"{output_path}/quantized_model.pt")
        return quantized_model
    
    def quantize_static(self, calibration_data, output_path: str):
        """Apply static quantization"""
        model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        model.eval()
        
        # Prepare model for quantization
        model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
        torch.quantization.prepare(model, inplace=True)
        
        # Calibrate
        for data in calibration_data:
            model(data)
        
        # Convert to quantized model
        quantized_model = torch.quantization.convert(model, inplace=False)
        
        torch.save(quantized_model.state_dict(), f"{output_path}/static_quantized_model.pt")
        return quantized_model