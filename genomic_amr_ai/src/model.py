import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification
from peft import get_peft_model, LoraConfig, TaskType

class AMRClassifier(nn.Module):
    """
    Genomic Language Model (DNABERT-2) with LoRA Adapter for AMR Prediction
    """
    def __init__(
        self,
        model_name: str = "bert-base-uncased",
        num_classes: int = 2,
        lora_r: int = 8,
        lora_alpha: int = 16,
        lora_dropout: float = 0.1
    ):
        super().__init__()
        
        # Pre-trained Sequence Classification Backbone ကို ခေါ်ယူခြင်း
        self.backbone = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_classes,
    
            return_dict=True
        )
        
        # LoRA Adapter Configuration သတ်မှတ်ခြင်း
        peft_config = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            target_modules=["query", "value"]
        )
        
        # Backbone ကို LoRA Adapter ဖြင့် ပေါင်းစပ်ခြင်း
        self.model = get_peft_model(self.backbone, peft_config)

    def forward(self, input_ids, attention_mask=None, labels=None,return_dict=True):
        return self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            return_dict=return_dict
        )

if __name__ == "__main__":
    print("Testing AMRClassifier Architecture...")
    
    model = AMRClassifier(num_classes=2)
    
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    all_params = sum(p.numel() for p in model.parameters())
    
    print("Model Initialized Successfully!")
    print(f"Trainable Params: {trainable_params:,} | Total Params: {all_params:,}")
    print(f"Trainable Percentage: {100 * trainable_params / all_params:.2f}%")