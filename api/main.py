from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from api.routers import profiles, ratings, reading_list, reviews, social, recommendations
import numpy as np
import torch
import pandas as pd
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpoint = torch.load(
        os.path.join("models", "hybrid_model.pt"),
        map_location="cpu",
        weights_only=False
    )
    from api.routers.recommendations import HybridModel
    model = HybridModel(
        n_users=checkpoint['n_users'],
        n_books=checkpoint['n_books'],
        embedding_dim=checkpoint['embedding_dim'],
        content_dim=checkpoint['content_dim'],
        hidden_layers=checkpoint['hidden_layers'],
        dropout=checkpoint['dropout']
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    app.state.model = model
    app.state.user2idx = checkpoint['user2idx']
    app.state.book2idx = checkpoint['book2idx']
    app.state.idx2bookid = {v: k for k, v in checkpoint['book2idx'].items()}
    app.state.book_embeddings = np.load(os.path.join("data", "book_embeddings.npy"))
    books = pd.read_csv(os.path.join("data", "books.csv"))
    app.state.bookid2row = {row['id']: idx for idx, row in books.iterrows()}

    print("Model and embeddings loaded at startup")
    yield
    print("Shutting down")

app = FastAPI(
    title="Book Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles.router)
app.include_router(ratings.router)
app.include_router(reading_list.router)
app.include_router(reviews.router)
app.include_router(social.router)
app.include_router(recommendations.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}