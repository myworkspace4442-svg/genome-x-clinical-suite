import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from dataset import AMRDataset
from model import AMRClassifier
from sklearn.metrics import accuracy_score, f1_score
import os

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    # train.py ထဲမှ Dataset ခေါ်ယူသည့် လိုင်း

    dataset = AMRDataset(csv_file="data/sample_amr_data.csv", tokenizer=tokenizer)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True) 

    model = AMRClassifier().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    model.train()
    print("Starting Training Loop Test...")

    epochs = 2
    for epoch in range(epochs):
        total_loss = 0.0
        # ၁။ Epoch တိုင်းအတွက် Prediction List များကို Reset ပြန်လုပ်ပါ
        all_preds = []
        all_labels = []

        for batch in dataloader:
            optimizer.zero_grad()

            # ၂။ Batch များကို Device ပေါ်သို့ ပို့ပေးပါ
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].long().to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # ၃။ Logits မှ အမြင့်ဆုံး Probability ရှိသော Class (0 သို့မဟုတ် 1) ကို argmax ဖြင့် ထုတ်ယူခြင်း
            preds = torch.argmax(outputs.logits, dim=-1)

            # ၄။ List ထဲသို့ CPU ထဲပြောင်း၍ ထည့်ပါ
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

        avg_loss = total_loss / len(dataloader)
        
        # ၅။ Epoch အဆုံးတွင် Metrics များ တွက်ချက်ပါ
        epoch_acc = accuracy_score(all_labels, all_preds)
        epoch_f1 = f1_score(all_labels, all_preds, average='macro')

        print(f"Epoch {epoch + 1}/{epochs} | Loss: {avg_loss:.4f} | Acc: {epoch_acc:.4f} | F1: {epoch_f1:.4f}") 
        print("Input shape:", input_ids.shape)
        print("Logits shape:", outputs.logits.shape)
   
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/amr_lora_model.pt")

    print("Training Loop Test Completed Successfully!")

if __name__ == "__main__":
    train()