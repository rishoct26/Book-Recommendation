from fastapi import APIRouter, HTTPException, Request
from api.database import supabase
from api.schemas import BookResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/{book_id}")
def get_book(book_id: int):
    response = supabase.table("books").select("*").eq("id", book_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")
    return response.data

@router.get("/search/query")
def search_books(q: str):
    response = supabase.table("books").select("*").ilike("title", f"%{q}%").limit(20).execute()
    return response.data

@router.get("/trending/top")
def get_trending():
    response = supabase.table("books").select("*").order("ratings_count", desc=True).limit(20).execute()
    return response.data