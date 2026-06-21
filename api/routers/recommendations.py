from fastapi import APIRouter, HTTPException
from api.database import supabase
from api.schemas import RecommendationRequest, ColdStartRequest, RecommendationResponse
import numpy as np
import torch
import pickle
import os

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

def load_model():
    models_dir = "models"

    with open(os.path.join(models_dir,"hybrid_book_embeddings.pkl"), "rb") as f:
        book_embeddings = pickle.load(f)

    with open(os.path.join(models_dir,"hybrid_user_embeddings.pkl"), "rb") as f:
        user_embeddings = pickle.load(f)

    with open(os.path.join(models_dir,"hybrid_book_ids.pkl"), "rb") as f:
        book_ids = pickle.load(f)
    
    with open(os.path.join(models_dir,"hybrid_user_ids.pkl"), "rb") as f:
        user_ids = pickle.load(f)

    return book_embeddings, user_embeddings, book_ids, user_ids

@router.post("/", response_model=list[RecommendationResponse])
def get_recommendations(request:RecommendationRequest):
    try:
        book_embeddings, user_embeddings, book_ids, user_ids = load_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load models: {str(e)}")
    
    if request.user_id not in user_ids:
        raise HTTPException(status_code=404, detail="User not found in model")
    
    user_idx = user_ids.index(request.user_id)
    user_vec = user_embeddings[user_idx]

    scores = np.dot(book_embeddings, user_vec)
    top_indices = np.argsort(scores)[::-1][:request.n]

    results = []
    for idx in top_indices:
        results.append({
            "book_id": int(book_ids[idx]),
            "score": float(scores[idx])
        })

    return results

@router.post("/cold-start", response_model=list[RecommendationResponse])
def cold_start(request: ColdStartRequest):
    try:
        book_embeddings, _, book_ids, _ = load_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load models: {str(e)}")
    
    ratings_response = supabase.table("user_ratings").select("book_id").execute()
    popular_book_ids = [r["book_id"] for r in ratings_response.data]

    genre_books = [i for i, bid in enumerate(book_ids) if bid in popular_book_ids]

    if not genre_books:
        genre_books = list(range(min(request.n, len(book_ids))))

    scores = np.random.random(len(genre_books))
    top_indices = np.argsort(scores)[::-1][:request.n]

    results = []
    for idx in top_indices:
        book_idx = genre_books[idx]
        results.append({
            "book_id": int(book_ids[book_idx]),
            "score": float(scores[idx])
        })
    return results