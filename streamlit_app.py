# 📦 Import necessary libraries
import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 🚀 Load the model and tokenizer once (only on app start)
@st.cache_resource
def load_model():
    # Load tokenizer and model from Hugging Face (fine-tuned for sentiment)
    tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    
    # Set the model to evaluation mode (not training)
    model.eval()
    
    return tokenizer, model

# Load model/tokenizer
tokenizer, model = load_model()

# Function to predict sentiment from input text
def predict_sentiment(text):
    # Convert text to input tensors
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # Disable gradient tracking for faster inference
    with torch.no_grad():
        outputs = model(**inputs)  # Get raw model outputs
        probs = outputs.logits.softmax(dim=1)  # Convert to probabilities
        pred = torch.argmax(probs).item() + 1  # Convert to 1–5 star rating

    # Return simplified sentiment label
    if pred <= 2:
        return "Negative"
    elif pred == 3:
        return "Neutral"
    else:
        return "Positive"

# Set up the Streamlit page
st.set_page_config(page_title="BERT Sentiment Analyzer", page_icon="🧠")
st.title("BERT Sentiment Classifier")
st.markdown("Enter any sentence and classify it as **Positive** or **Negative** sentiment.")

# Text box for user input
user_input = st.text_area("Enter your text:", height=150)

# Button to analyze the sentiment
if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        result = predict_sentiment(user_input)
        
        # Show the result using styled message
        if result == "Positive":
            st.success("✅ Positive Sentiment")
        else:
            st.error("⚠️ Negative Sentiment")
