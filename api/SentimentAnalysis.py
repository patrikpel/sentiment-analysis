import pandas as pd
import html

from fastai.text.all import *
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple, ClassVar
from fastai.data.block import DataBlock, CategoryBlock, DataLoaders
from fastai.learner import Learner   # Explicit import for Learner

# FastAPI app instance
app = FastAPI()

# Loads user given CSV File
def load_data(file_path):
    # Load only the first 2000 rows for testing
    df = pd.read_csv(file_path, encoding='ISO-8859-1', nrows=2000)
    print(f"Loaded data with {len(df)} records.")
    return df

# Preprocesses data for training
def preprocess_data(df):
    # Make sure the CSV has the correct columns for 'text' and 'sentiment'
    df = df[['text', 'sentiment']]
    
    # Create a DataLoader for text classification
    dls = TextDataLoaders.from_df(df, text_col='text', label_col='sentiment', valid_pct=0.2, bs=32)
    print(f"DataLoader created with {len(dls.train)} training samples and {len(dls.valid)} validation samples.")
    return dls

def learn_data(dls):
    # Define text classifier and fine-tune it
    learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
    learn.fine_tune(8, 1e-2)
    
    return learn

# Define the pydantic models for request and response schemas
class SentimentRequest(BaseModel):
    paragraph: str

class SentimentResponse(BaseModel):
    word_sentiments: List[Tuple[str, str, List[float]]]

# Load the model globally
@app.on_event("startup")
def load_model():
    """ Load the model when the server starts. """
    global dls, learn
    # Load the CSV file containing tweets and sentiments
    file_path = 'train.csv' 
    df = load_data(file_path)
    
    # Preprocess the data and create DataLoader
    dls = preprocess_data(df)

    learn = learn_data(dls)

@app.post("/predict_sentiment/")
def predict_word_sentiment(request: SentimentRequest):
    """ Predict the sentiment for each word in the given paragraph. """
    paragraph = request.paragraph
    
    # HTML decode the paragraph to handle any HTML entities
    decoded_paragraph = html.unescape(paragraph)
    
    # Tokenize the decoded paragraph into individual words
    words = decoded_paragraph.split()
    
    # Create a list to store sentiment predictions
    word_sentiments = []
    
    # Get predictions for each word
    for word in words:
        # FastAI's `predict` method expects a list of text, so we pass the word as a list
        pred, _, probs = learn.predict(word)
        
        # Append the predicted sentiment and probability for each word
        word_sentiments.append((word, pred, probs.tolist()))  # Convert to list for JSON serialization
    
    return SentimentResponse(word_sentiments=word_sentiments)
