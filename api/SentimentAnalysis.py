import pandas as pd
import html
import re
from fastai.text.all import *
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
from fastai.data.block import DataBlock, CategoryBlock, DataLoaders
from fastai.learner import Learner  # Explicit import for Learner
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app instance
app = FastAPI()

# Allow all origins (replace with your actual frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this to your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Loads user given CSV File
def load_data(file_path):
    # Load only the first 5000 rows for testing
    df = pd.read_csv(file_path, encoding='ISO-8859-1', nrows=5000)
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
    sentence_sentiments: List[Tuple[str, str, List[float]]]
    paragraph_breaks: List[int]  # To store positions of paragraph breaks

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
def predict_sentence_sentiment(request: SentimentRequest):
    """ Predict the sentiment for each sentence in the given paragraph. """
    paragraph = request.paragraph
    
    # HTML decode the paragraph to handle any HTML entities
    decoded_paragraph = html.unescape(paragraph)
    
    # Split the paragraph into sentences using a regex pattern for common sentence delimiters
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', decoded_paragraph)
    
    # Track paragraph breaks: We will detect the position of breaks based on newline characters
    paragraph_breaks = [i for i, char in enumerate(decoded_paragraph) if char == '\n']
    
    # Create a list to store sentiment predictions
    sentence_sentiments = []
    
    # Get predictions for each sentence
    for sentence in sentences:
        # FastAI's `predict` method expects a list of text, so we pass the sentence as a list
        pred, _, probs = learn.predict(sentence)
        
        # Append the predicted sentiment and probability for each sentence
        sentence_sentiments.append((sentence, pred, probs.tolist()))  # Convert to list for JSON serialization
    
    return SentimentResponse(
        sentence_sentiments=sentence_sentiments,
        paragraph_breaks=paragraph_breaks
    )
