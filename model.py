from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load once on startup
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
model.eval()

def predict_sentiment(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = outputs.logits.softmax(dim=1)
        pred = torch.argmax(probs).item()
    return "Positive" if pred == 1 else "Negative"
