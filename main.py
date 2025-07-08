from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_sentiment

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def get_sentiment(request: TextRequest):
    result = predict_sentiment(request.text)
    return {"sentiment": result}
