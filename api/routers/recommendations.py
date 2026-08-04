from fastapi import APIRouter, HTTPException, Request
from api.database import supabase
from api.schemas import RecommendationRequest, ColdStartRequest, RecommendationResponse
import numpy as np
import torch
import torch.nn as nn

class HybridModel(nn.Module):
    def __init__(self, n_users, n_books, embedding_dim=50, content_dim=384,
                 hidden_layers=[256, 128, 64], dropout=0.2):
        super().__init__()
        self.user_embeddings = nn.Embedding(n_users, embedding_dim)
        self.book_embeddings = nn.Embedding(n_books, embedding_dim)
        input_dim = embedding_dim * 2 + content_dim
        layers = []
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            input_dim = hidden_dim
        layers.append(nn.Linear(input_dim, 1))
        self.network = nn.Sequential(*layers)

    def forward(self, user_idx, book_idx, content_emb):
        user_emb = self.user_embeddings(user_idx)
        book_emb = self.book_embeddings(book_idx)
        concat = torch.cat([user_emb, book_emb, content_emb], dim=1)
        return self.network(concat).squeeze()

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/", response_model=list[RecommendationResponse])
def get_recommendations(request: RecommendationRequest, req: Request):
    model = req.app.state.model
    user2idx = req.app.state.user2idx
    book2idx = req.app.state.book2idx
    idx2bookid = req.app.state.idx2bookid
    book_embeddings = req.app.state.book_embeddings
    bookid2row = req.app.state.bookid2row

    if request.user_id not in user2idx:
        raise HTTPException(status_code=404, detail="User not found in model")

    user_idx = user2idx[request.user_id]
    all_book_indices = list(book2idx.values())
    user_indices = torch.tensor([user_idx] * len(all_book_indices), dtype=torch.long)
    book_indices = torch.tensor(all_book_indices, dtype=torch.long)

    content_embs = []
    for book_idx in all_book_indices:
        book_id = idx2bookid[book_idx]
        row = bookid2row.get(book_id, 0)
        content_embs.append(book_embeddings[row])
    content_embs = torch.tensor(np.array(content_embs), dtype=torch.float32)

    with torch.no_grad():
        predictions = model(user_indices, book_indices, content_embs)

    predictions = predictions.numpy()
    top_indices = np.argsort(predictions)[::-1][:request.n]

    results = []
    for i in top_indices:
        book_idx = all_book_indices[i]
        book_id = idx2bookid[book_idx]
        results.append({
            "book_id": int(book_id),
            "score": float(predictions[i])
        })
    return results

@router.post("/cold-start", response_model=list[RecommendationResponse])
def cold_start(request: ColdStartRequest, req: Request):
    bookid2row = req.app.state.bookid2row

    ratings_response = supabase.table("user_ratings").select("book_id").execute()
    popular_book_ids = [r["book_id"] for r in ratings_response.data]

    if not popular_book_ids:
        popular_book_ids = list(bookid2row.keys())[:request.n]

    scores = np.random.random(len(popular_book_ids))
    top_indices = np.argsort(scores)[::-1][:request.n]

    results = []
    for idx in top_indices:
        results.append({
            "book_id": int(popular_book_ids[idx]),
            "score": float(scores[idx])
        })
    return results