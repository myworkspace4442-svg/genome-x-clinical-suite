import torch
from torch.utils.data import Dataset
import pandas as pd

class AMRDataset(Dataset):
    def __init__(self, csv_file, tokenizer, max_length=512):
        # 1. Pandas ဖြင့် CSV Data ဖတ်ယူခြင်း
        self.df = pd.read_csv(csv_file)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # 2. Row တစ်ခုချင်းစီမှ Sequence နှင့် Label ထုတ်ယူခြင်း
        sequence = str(self.df.iloc[idx]['sequence'])
        label = int(self.df.iloc[idx]['label'])

        # 3. Tokenize ပြုလုပ်၍ Tensor အသွင်ပြောင်းခြင်း
        encoding = self.tokenizer(
            sequence,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].squeeze(0), # (1, 512) မှ (512) သို့ ပြောင်းခြင်း
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'labels': torch.tensor(label, dtype=torch.long)
        }